<p align="center">
  <a href="https://packetexchange.io"><img src="assets/banner.png" alt="PacketExchange Python SDK" width="100%"></a>
</p>

<p align="center">Typed Python client for the PacketExchange voice and SMS marketplace API.</p>

<p align="center">
  <a href="https://github.com/PacketExchangeIO/packetexchange-python/actions/workflows/ci.yml"><img src="https://github.com/PacketExchangeIO/packetexchange-python/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT"></a>
  <a href="https://pypi.org/project/packetexchange/"><img src="https://img.shields.io/pypi/v/packetexchange.svg" alt="PyPI version"></a>
  <img src="https://img.shields.io/badge/python-3.9%2B-blue.svg" alt="Python 3.9+">
</p>

A small, typed client for the PacketExchange REST API (`https://packetexchange.io/api/v1`),
built on [httpx](https://www.python-httpx.org/). Its models and operation table are
generated from the public OpenAPI document, so the SDK and the API reference describe the
same thing. Every documented endpoint is reachable, with or without a convenience method.

You need a PacketExchange account with prepaid credit to use the API. Sign up at
[packetexchange.io](https://packetexchange.io), add credit, then create an API key in the
dashboard under **API keys**.

## Installation

```bash
pip install packetexchange
```

Python 3.9 or later is required.

## Quick start

Keep the API key in the environment, never in source:

```bash
export PACKETEXCHANGE_API_KEY=your_api_key
```

```python
import os

from packetexchange import PacketExchange, PacketExchangeError

with PacketExchange(api_key=os.environ["PACKETEXCHANGE_API_KEY"]) as px:
    try:
        # 1. Verify a phone number: send a one-time code by SMS (or channel="voice").
        verification = px.verify.start("+447700900123", channel="sms", brand="Acme")

        # Later, check the code the user typed in.
        check = px.verify.check(verification["verificationId"], "482913")
        print(check["status"])  # "approved", "denied", "expired" or "max_attempts"

        # 2. Send a transactional SMS. The idempotency key makes a retry safe.
        sms = px.comms.sms(
            to="+447700900123",
            from_="Acme",
            message="Your order 1042 has shipped.",
            idempotency_key="order-1042-shipped",
        )
        print(sms["messageId"], sms["status"], sms["cost"])

        # 3. Price a number: every marketplace route that serves it, cheapest first.
        priced = px.routes.price_number("+447700900123", type="voice")
        for route in priced["routes"]:
            print(route["name"], route["rate"], f"USD/{priced['unit']}")
    except PacketExchangeError as e:
        print(e.status, e.code, e.message, e.details, e.request_id)
```

The `status` returned by `comms.sms()` is the send-time outcome (for example `sent` or
`failed`). Delivery is tracked afterwards: see [SMS delivery status](#sms-delivery-status).
`from` is a Python keyword, so the sender is passed as `from_`.

## SMS delivery status

`comms.get_sms()` returns a message's current status and its timeline: `queued`, `sent`,
then `delivered` or `failed`, each step with a timestamp. A message is marked `delivered`
only when a carrier delivery receipt confirms it. On a route that returns no receipts the
message stays `sent` with `awaitingReceipt` set to `True`; `routeReturnsReceipts` tells you
whether the route has returned receipts recently. `errorCode` explains a failure, and a
message that fails on its carrier receipt is refunded.

```python
status = px.comms.get_sms(sms["messageId"])
print(status["status"], status.get("awaitingReceipt"))
for step in status.get("timeline", []):
    print(step["at"], step["status"], step.get("errorCode"))
```

To be told instead of polling, subscribe a webhook endpoint to `sms.delivered` and
`sms.failed`.

## Calls with actions

`comms.call()` waits for the call to end. `comms.call_async()` returns as soon as the call
is being dialled, with a `callId` (HTTP 202, `status` `"ringing"`). Actions run in order
once the call is answered: `say` (text spoken in `en`, `es`, `fr`, `de`, `pt` or `hi`),
`play` (an https URL of an MP3 file), `gather` (collect keypad digits), `pause` and
`hangup`.

```python
call = px.comms.call_async(
    "+447700900123",
    "+14155550100",
    actions=[
        {"say": "Your delivery is booked for tomorrow."},
        {"gather": {"digits": 1, "timeout": 5, "say": "Press 1 to confirm, or 2 to rebook."}},
        {"say": "Thank you. Goodbye."},
        {"hangup": True},
    ],
)

done = px.comms.wait_for_call(call["callId"])  # polls get_call() until a final state
print(done["status"], done["hangupReason"], done["cost"])
for g in done.get("gathered") or []:
    print(g["index"], g["status"], g["digits"])
```

`comms.get_call()` reads the live status (`queued`, `ringing`, `answered`, then
`completed`, `no_answer`, `busy` or `failed`), timestamps, cost and a plain-words
`hangupReason`. Gathered digits are filled in when the call ends. In production, prefer the
`call.ringing`, `call.answered`, `call.gathered` and `call.completed` webhooks to polling.
A test key simulates the call and runs no actions.

## Number lookup

`lookup.number()` validates and formats a number and returns its country, line type
(`mobile`, `fixed`, `toll_free`, `premium` or `unknown`), the network where the
marketplace's rate decks agree, the network its number range was allocated to, blocked and
high-risk flags, and the cheapest live voice and SMS price to reach it. Lookups are free,
limited to 60 a minute, and prefix-based: no carrier query is made, so a ported number
shows its original network and the lookup cannot tell whether a number is in service.

```python
info = px.lookup.number("+447700900123")
if info["valid"]:
    print(info["e164"], info["numberType"], (info.get("country") or {}).get("name"))
    sms_price = (info.get("pricing") or {}).get("sms")
    if sms_price:
        print(sms_price["rate"], "USD per message")
else:
    print(info["reason"])
```

When a route prices SMS per network, the SMS price is for the number's network and carries
a `network` object. `comms.sms()` returns the same `network` object when the route that
carried the message prices per network.

## Verification codes

The Verify API generates a code, sends it, and checks it for you. Only a keyed hash of the
code is stored. Each verification expires (600 seconds by default, configurable with
`expiry_seconds`), allows 5 attempts and approves once. Sends are rate limited per number
and per account; a refusal raises `PacketExchangeError` with status 429 and code
`RATE_LIMITED`.

```python
v = px.verify.start("+447700900123", channel="voice", language="es")
state = px.verify.get(v["verificationId"])
```

If you already generate your own code and only need it spoken on a call, use a voice
passcode call. The call continues after the method returns; read the outcome later.

```python
otp = px.comms.voice_otp("+447700900123", code="482913", brand="Acme")
outcome = px.comms.get_voice_otp(otp["voiceOtpId"])
```

Voice codes can be spoken in `en`, `es`, `fr`, `de`, `pt` and `hi`. SMS codes also support
`ar`. Keys need the `verify:write` scope for `verify.*` and `voice:send` for
`comms.voice_otp`.

## Configuration

```python
px = PacketExchange(
    api_key=os.environ["PACKETEXCHANGE_API_KEY"],  # sent as "Authorization: Bearer <key>"
    base_url="https://packetexchange.io",           # the default; /api/v1 is added for you
    timeout=30.0,                                   # seconds
    headers={"X-Correlation-Id": "abc"},            # optional: added to every request
    http_client=None,                               # optional: your own httpx.Client
)
```

Use the client as a context manager, or call `px.close()` when you are done. When you pass
your own `http_client`, you are responsible for closing it.

`px.comms.call()` returns when the call ends, so set `timeout` above the call's
`maxDuration` (default 300 seconds) when you place calls.

### Live and test keys

API keys are environment-scoped:

- `wmmn_live_sk_...` places real calls and messages and charges your balance.
- `wmmn_test_sk_...` simulates calls, SMS and dialer runs instead of sending them, and
  charges only the account's test credit. Responses from a test key carry
  `"simulated": True`, and `verify.start` returns `testCode` so you can complete a
  verification flow end to end.

Test keys cannot make changes that have no test mode: a Switch change (any write under
`/switch`) or an x402 top-up fails with status 403 and code `TEST_KEY_NOT_ALLOWED`. Use a
live key for those.

Keys can be limited to scopes such as `voice:send`, `sms:send`, `verify:write` and
`routes:read`. A call that needs a scope the key lacks fails with status 403 and a message
naming the missing scope. Managing webhook endpoints needs the `webhooks:write` scope,
which a full-access key does not include: choose it explicitly when you create the key. A
few account-management endpoints (API keys, payouts) accept only a dashboard session,
never an API key.

## Error handling

Every failure raises `PacketExchangeError`: a non-2xx response, a `success: false`
envelope, or a network error.

| Attribute | Meaning |
| --- | --- |
| `status` | HTTP status, or `0` when no response arrived |
| `code` | The API error code (`VALIDATION_ERROR`, `INVALID_INPUT`, `FORBIDDEN`, `RATE_LIMITED`, ...), or `HTTP_<status>` / `NETWORK_ERROR` when the body had none |
| `message` | Human-readable explanation |
| `details` | For `VALIDATION_ERROR`, a list of `{"path", "message"}` dicts, one per failing field |
| `request_id` | The `X-Request-Id` response header. Quote it when you contact support |
| `is_auth_error` | `True` for 401 and 403 |
| `is_rate_limited` | `True` for 429. Wait for the `Retry-After` seconds, then retry |

The API's error envelope is:

```json
{ "success": false, "error": { "code": "VALIDATION_ERROR", "message": "Invalid input", "details": [{ "path": "to", "message": "Invalid E.164 number" }] } }
```

The full list of error codes is in the [API reference](https://packetexchange.io/api-docs).

## Pagination

List methods return a `Page` with `data`, `next_cursor`, `has_more` and `total`. Pass
`next_cursor` back as `cursor`, or iterate every item and let the SDK follow the cursor:

```python
page = px.routes.list(country="GB", type="voice", limit=50)

for tx in px.billing.iterate_transactions():
    print(tx["amount"])
```

## Money

Every amount is a US dollar string with exactly 6 decimal places (`"0.012500"`). Voice
prices are per minute and SMS prices are per message segment. Use `decimal.Decimal` for
arithmetic, never `float`.

## Webhooks

PacketExchange signs every webhook delivery. Verify each one in your receiver with
`verify_webhook_signature`, passing the request body exactly as received (bytes are best).
Parsing and re-serialising the JSON changes the bytes and breaks the signature.

```python
import os

from flask import Flask, request
from packetexchange import verify_webhook_signature

app = Flask(__name__)


@app.post("/webhooks/packetexchange")
def packetexchange_webhook():
    result = verify_webhook_signature(
        secret=os.environ["PACKETEXCHANGE_WEBHOOK_SECRET"],
        raw_body=request.get_data(),  # the raw bytes, before any JSON parsing
        headers=request.headers,
        tolerance_seconds=300,        # the default: reject deliveries older than 5 minutes
    )
    if not result:
        return result.reason or "invalid signature", 400

    event = request.get_json()
    # Deliveries can repeat (retries and manual resends), so de-duplicate on the event data.
    return "", 200
```

Each delivery carries two signatures:

| Scheme | Headers | Signed content |
| --- | --- | --- |
| v1 (current) | `X-PX-Timestamp: <unix seconds>`<br>`X-PX-Signature: v1=<hex>` | HMAC-SHA256 of `"<timestamp>.<raw body>"` |
| Legacy | `X-Webhook-Signature: sha256=<hex>` | HMAC-SHA256 of the raw body |

The helper checks v1 whenever either v1 header is present, and rejects timestamps outside
`tolerance_seconds` so a captured delivery cannot be replayed. It falls back to the legacy
signature only when both v1 headers are absent, and never when just one of them was
stripped. Pass `allow_legacy=False` to refuse the legacy scheme entirely. The result is a
`SignatureResult(valid, scheme, reason, timestamp)` named tuple that is truthy only when
the signature is valid; `scheme` is `"v1"`, `"legacy"` or `"none"`. Comparison is
constant-time.

Manage endpoints, and inspect or resend deliveries, with the `webhooks` resource. Creating,
editing, deleting and rotating the secret need a key with the `webhooks:write` scope. The
signing secret is returned once, by `create` and `rotate_secret`:

```python
hook = px.webhooks.create("https://example.com/webhooks/packetexchange", ["sms.delivered", "sms.failed"])
secret = hook["secret"]  # store it now; it is not shown again

for d in px.webhooks.deliveries(status="failed").data:
    print(d["event"], d["httpStatus"], d["lastError"])
```

## Resources

| Attribute | Covers |
| --- | --- |
| `routes` | Marketplace listing, Smart Routing preview, number pricing |
| `purchases` | Buying routes, routing order, rate changes |
| `offers` | Price proposals on routes |
| `comms` | Single calls (waiting or async, with actions), call status, SMS and delivery status, voice passcode calls |
| `verify` | One-time code verification by SMS or voice |
| `dids` | Phone number search, purchase and listing |
| `webhooks` | Webhook endpoints, delivery history and resends |
| `api_keys` | Listing API keys (dashboard session only) |
| `account` | Profile, balance, API usage |
| `billing` | The transaction ledger |
| `cli_tests` | Route liveness tests |
| `lookup` | Number lookup: type, network, risk flags and cheapest price |

Listing ASR and ACD figures are stated by the seller, not measured by PacketExchange.

### Any endpoint

Every documented operation is reachable, with or without a convenience method. Both calls
below apply the same authentication and error handling:

```python
px.request("GET", "/dids/mine")
px.call_operation("getDidsMine")
```

`packetexchange.OPERATIONS` maps each operation ID to its method, path, tag and summary.
Use `px.request_envelope()` when you need the whole response envelope, and `px.page()` or
`px.paginate()` for any cursor-paginated endpoint.

## Typed models

`packetexchange.models` contains a `TypedDict` for every schema in the OpenAPI document.
Responses are plain dicts, so the models are for type checkers and editors:

```python
from packetexchange import models

priced: models.PriceNumberResult = px.routes.price_number("+447700900123")
```

The models are generated from [`openapi.json`](openapi.json), a copy of the document served
at `https://packetexchange.io/api/v1/docs/json`. To refresh them:

```bash
curl -fsSL https://packetexchange.io/api/v1/docs/json -o openapi.json
python scripts/generate.py
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt -e .
pytest
mypy
python -m build
```

The tests use `httpx.MockTransport` and never call the live API.

## Versioning

This SDK follows [Semantic Versioning](https://semver.org/). While the major version is
`0`, a minor release may contain breaking changes; each one is listed in
[CHANGELOG.md](CHANGELOG.md). The API itself is versioned by path (`/api/v1`).

## Links

- Developer overview: [packetexchange.io/developers](https://packetexchange.io/developers)
- API reference: [packetexchange.io/api-docs](https://packetexchange.io/api-docs)
- Support: [support@packetexchange.io](mailto:support@packetexchange.io)
- Security issues: see [SECURITY.md](SECURITY.md)

## License

[MIT](LICENSE)
