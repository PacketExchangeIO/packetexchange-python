"""The PacketExchange client: a small HTTP core plus convenience methods for the
core endpoints. Anything without a convenience method is still one call away via
:meth:`PacketExchange.request` or :meth:`PacketExchange.call_operation`."""

from __future__ import annotations

import json as _json
import time
from dataclasses import dataclass
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence, cast
from urllib.parse import quote

import httpx

from ._errors import PacketExchangeError
from ._generated import models as _m
from ._generated.operations import OPERATIONS

#: Production host. Paths are sent under /api/v1 (added automatically).
DEFAULT_BASE_URL = "https://packetexchange.io"
API_PREFIX = "/api/v1"


@dataclass
class Page:
    """One page of a cursor-paginated list: pass ``next_cursor`` as ``cursor``."""

    data: List[Any]
    next_cursor: Optional[str]
    has_more: bool
    total: Optional[int] = None


def _clean(d: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Drop None values so optional filters are simply omitted from the request."""
    return {k: v for k, v in (d or {}).items() if v is not None}


class PacketExchange:
    """Client for the PacketExchange API.

    Example::

        px = PacketExchange(api_key=os.environ["PACKETEXCHANGE_API_KEY"])
        best = px.routes.resolve(to="+447911123456")["selected"]
        print(best["price"])          # a 6-decimal USD string, e.g. "0.012500"

    Auth: ``api_key`` or a user ``access_token`` (JWT), both sent as
    ``Authorization: Bearer <credential>``; ``api_key`` wins if both are given.
    Some account-management endpoints accept only a dashboard session (JWT).
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        headers: Optional[Mapping[str, str]] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self._credential = api_key or access_token
        # Accept a base URL with or without /api/v1 so both spellings just work.
        base = base_url.rstrip("/")
        self._base = base[: -len(API_PREFIX)] if base.endswith(API_PREFIX) else base
        self._headers = dict(headers or {})
        self._owns_client = http_client is None
        self._http = http_client or httpx.Client(timeout=timeout)

        self.routes = RoutesResource(self)
        self.purchases = PurchasesResource(self)
        self.offers = OffersResource(self)
        self.comms = CommsResource(self)
        self.dids = DidsResource(self)
        self.webhooks = WebhooksResource(self)
        self.api_keys = ApiKeysResource(self)
        self.account = AccountResource(self)
        self.billing = BillingResource(self)
        self.cli_tests = CliTestsResource(self)
        self.verify = VerifyResource(self)
        self.lookup = LookupResource(self)

    # ── lifecycle ────────────────────────────────────────────────────────────────

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> "PacketExchange":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    # ── HTTP core ────────────────────────────────────────────────────────────────

    def _url(self, path: str) -> str:
        # Operation-table paths carry /api/v1 already; convenience paths do not.
        return self._base + (path if path.startswith("/api/") else API_PREFIX + path)

    def request_envelope(
        self,
        method: str,
        path: str,
        *,
        query: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        idempotency_key: Optional[str] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Dict[str, Any]:
        """Send a request and return the whole JSON envelope, raising on failure."""
        h: Dict[str, str] = {"Accept": "application/json", **self._headers}
        if self._credential:
            h["Authorization"] = f"Bearer {self._credential}"
        if idempotency_key:
            # A replay of the same key within 24 hours returns the original response.
            h["X-Idempotency-Key"] = idempotency_key
        h.update(headers or {})
        try:
            res = self._http.request(method, self._url(path), params=_clean(query), json=json, headers=h)
        except httpx.HTTPError as err:
            raise PacketExchangeError("NETWORK_ERROR", str(err) or "Network request failed", 0) from err

        request_id = res.headers.get("x-request-id")
        try:
            body: Any = res.json() if res.content else {}
        except _json.JSONDecodeError:
            body = {"success": False, "error": {"code": f"HTTP_{res.status_code}", "message": res.text or res.reason_phrase}}

        if res.status_code >= 400 or (isinstance(body, dict) and body.get("success") is False):
            raw_err = body.get("error") if isinstance(body, dict) else None
            api_err: Dict[str, Any] = raw_err if isinstance(raw_err, dict) else {}
            raise PacketExchangeError(
                api_err.get("code") or f"HTTP_{res.status_code}",
                api_err.get("message") or res.reason_phrase or "Request failed",
                res.status_code,
                api_err.get("details"),
                request_id,
            )
        return body if isinstance(body, dict) else {"success": True, "data": body}

    def request(self, method: str, path: str, **kwargs: Any) -> Any:
        """Send a request and return its ``data``.

        A few older endpoints put their fields beside ``success`` instead of under
        ``data``; for those the envelope minus ``success`` is returned, so callers
        never see an empty result because of the difference.
        """
        env = self.request_envelope(method, path, **kwargs)
        if "data" in env:
            return env["data"]
        return {k: v for k, v in env.items() if k != "success"}

    def page(self, path: str, query: Optional[Mapping[str, Any]] = None) -> Page:
        """One page of a cursor-paginated list."""
        env = self.request_envelope("GET", path, query=query)
        return Page(
            data=list(env.get("data") or []),
            next_cursor=env.get("nextCursor"),
            has_more=bool(env.get("hasMore")),
            total=env.get("total"),
        )

    def paginate(self, path: str, query: Optional[Mapping[str, Any]] = None) -> Iterator[Any]:
        """Yield every item across all pages, following ``nextCursor``."""
        q = dict(query or {})
        while True:
            p = self.page(path, q)
            yield from p.data
            if not (p.has_more and p.next_cursor):
                return
            q["cursor"] = p.next_cursor

    def call_operation(
        self,
        operation_id: str,
        path_params: Optional[Mapping[str, str]] = None,
        **kwargs: Any,
    ) -> Any:
        """Call any documented operation by its OpenAPI ``operationId``.

        Covers endpoints without a convenience method, e.g.::

            px.call_operation("getSwitchCustomers", query={"limit": 50})
        """
        try:
            op = OPERATIONS[operation_id]
        except KeyError:
            raise ValueError(f"Unknown operationId {operation_id!r}") from None
        path = op.path
        for k, v in (path_params or {}).items():
            path = path.replace("{" + k + "}", _seg(v))
        if "{" in path:
            raise ValueError(f"Missing path parameters for {operation_id}: {path}")
        return self.request(op.method, path, **kwargs)


def _seg(v: str) -> str:
    """Percent-encode one path segment (ids are UUIDs, but never trust input)."""
    return httpx.URL("/" + str(v)).raw_path.decode()[1:].replace("/", "%2F")


class _Resource:
    def __init__(self, client: PacketExchange) -> None:
        self._c = client


class RoutesResource(_Resource):
    """Marketplace routes."""

    def list(self, **filters: Any) -> Page:
        """GET /routes - browse the marketplace (filters: type, country, maxPrice, limit, cursor...)."""
        return self._c.page("/routes", filters)

    def iterate(self, **filters: Any) -> Iterator[Any]:
        return self._c.paginate("/routes", filters)

    def get(self, route_id: str) -> Any:
        """GET /routes/{id}."""
        return self._c.request("GET", f"/routes/{_seg(route_id)}")

    def resolve(self, to: str, type: str = "voice", strategy: Optional[str] = None) -> Any:
        """GET /routes/resolve - the route(s) Smart Routing would pick. Prices are strings."""
        return self._c.request("GET", "/routes/resolve", query={"to": to, "type": type, "strategy": strategy})

    def price_number(self, number: str, type: str = "voice") -> "_m.PriceNumberResult":
        """GET /routes/price-number - every marketplace route that serves ``number``, at the
        rate it would charge for that number (longest-prefix rate-sheet row, or the flat
        price), cheapest first. ``rate`` is a 6-decimal USD string; at most 100 routes."""
        return cast("_m.PriceNumberResult", self._c.request("GET", "/routes/price-number", query={"number": number, "type": type}))


class PurchasesResource(_Resource):
    def list(self, **filters: Any) -> Page:
        """GET /purchases - routes you bought."""
        return self._c.page("/purchases", filters)

    def create(self, route_id: str, idempotency_key: Optional[str] = None, **extra: Any) -> Any:
        """POST /purchases - buy access to a route."""
        return self._c.request("POST", "/purchases", json={"routeId": route_id, **extra}, idempotency_key=idempotency_key)

    # Routing order: your SIP credentials identify your ACCOUNT, not a route, so every
    # voice purchase covering a number is a candidate. Longest prefix wins; among equals
    # your routing order decides, then the cheaper rate, then the older purchase.

    def routing_order(self) -> List["_m.RoutingOrderEntry"]:
        """GET /purchases/routing-order - your voice purchases, ranked ones first."""
        return cast(List["_m.RoutingOrderEntry"], self._c.request("GET", "/purchases/routing-order"))

    def set_routing_order(self, purchase_ids: Sequence[str]) -> "_m.RoutingOrderResult":
        """PUT /purchases/routing-order - replace the whole order atomically; the first id
        becomes position 1 and every other voice purchase is unranked. ``[]`` clears it."""
        return cast("_m.RoutingOrderResult", self._c.request("PUT", "/purchases/routing-order", json={"purchaseIds": list(purchase_ids)}))

    def set_routing_priority(self, purchase_id: str, priority: Optional[int]) -> Dict[str, Any]:
        """PATCH /purchases/{id}/routing-priority - set (1 = first) or clear (None) one position."""
        return cast(Dict[str, Any], self._c.request(
            "PATCH", f"/purchases/{_seg(purchase_id)}/routing-priority", json={"priority": priority}
        ))

    def route_for(self, to: str) -> "_m.RouteForResult":
        """GET /purchases/route-for - which of your routes would carry ``to``, ranked exactly
        as the live call path ranks them, plus any refusal (embargo, empty balance)."""
        return cast("_m.RouteForResult", self._c.request("GET", "/purchases/route-for", query={"to": to}))

    def upcoming_rate_changes(self, purchase_id: str) -> "_m.PurchaseUpcomingRateChanges":
        """GET /purchases/{id}/upcoming-rate-changes - scheduled rate changes on a route you
        bought. Accept one in advance with ``accept_rate(purchase_id, change_id=...)``."""
        return cast(
            "_m.PurchaseUpcomingRateChanges",
            self._c.request("GET", f"/purchases/{_seg(purchase_id)}/upcoming-rate-changes"),
        )

    def accept_rate(self, purchase_id: str, accepted_rate: Optional[str] = None,
                    deck_version: Optional[str] = None, change_id: Optional[str] = None) -> Dict[str, Any]:
        """POST /purchases/{id}/accept-rate - accept a rate increase. With ``change_id`` it
        accepts a SCHEDULED change in advance (nothing resumes or bills now)."""
        return cast(Dict[str, Any], self._c.request(
            "POST",
            f"/purchases/{_seg(purchase_id)}/accept-rate",
            json=_clean({"acceptedRate": accepted_rate, "deckVersion": deck_version, "changeId": change_id}),
        ))


class OffersResource(_Resource):
    def list(self, **filters: Any) -> Any:
        """GET /offers - offers you made and received."""
        return self._c.request("GET", "/offers", query=filters)

    def create(self, route_id: str, proposed_price: str, message: Optional[str] = None) -> Any:
        """POST /offers - propose a price per unit (a decimal USD string) on a route."""
        return self._c.request(
            "POST", "/offers", json=_clean({"routeId": route_id, "proposedPrice": proposed_price, "message": message})
        )


class CommsResource(_Resource):
    def call(self, to: str, from_: str, idempotency_key: Optional[str] = None, **extra: Any) -> Any:
        """POST /comms/calls - place one call (scope voice:send). Blocks until it ends.

        The request returns when the call ends, so keep the client timeout above
        ``maxDuration`` (pass ``timeout=`` to the client for long calls). Pass
        ``actions=[...]`` to make the answered call speak, play, gather digits, pause or
        hang up, and ``language`` for the default ``say`` language. For a call that
        returns at once, use :meth:`call_async`.
        """
        return self._c.request("POST", "/comms/calls", json={"to": to, "from": from_, **extra}, idempotency_key=idempotency_key)

    def call_async(
        self,
        to: str,
        from_: str,
        actions: Optional[List[Dict[str, Any]]] = None,
        language: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """POST /comms/calls with ``async: true`` - returns as soon as the call is dialled.

        The result carries ``callId`` and ``status == "ringing"``; follow the call with
        :meth:`get_call`, :meth:`wait_for_call` or the ``call.ringing``, ``call.answered``,
        ``call.gathered`` and ``call.completed`` webhooks. Test keys simulate the call and
        run no actions. Example::

            call = px.comms.call_async(
                "+447700900123", "+14155550100",
                actions=[{"say": "Press 1 to confirm."}, {"gather": {"digits": 1, "timeout": 5}}],
            )
            done = px.comms.wait_for_call(call["callId"])
            print(done["status"], (done.get("gathered") or [{}])[0].get("digits"))
        """
        body = _clean({"to": to, "from": from_, "actions": actions, "language": language})
        return self._c.request(
            "POST", "/comms/calls", json={**body, **extra, "async": True}, idempotency_key=idempotency_key
        )

    def get_call(self, call_id: str) -> "_m.CommsCallStatus":
        """GET /comms/calls/{id} - live status, timestamps, cost, hangup reason and gathered digits."""
        return cast("_m.CommsCallStatus", self._c.request("GET", f"/comms/calls/{_seg(call_id)}"))

    def wait_for_call(self, call_id: str, timeout: float = 600.0, interval: float = 2.0) -> "_m.CommsCallStatus":
        """Poll :meth:`get_call` until the call is completed, no_answer, busy or failed.

        Returns the last status read, even when ``timeout`` seconds pass first. Webhooks
        suit production better; this is for scripts and notebooks.
        """
        deadline = time.monotonic() + timeout
        step = max(1.0, interval)
        while True:
            s = self.get_call(call_id)
            if s.get("status") in ("completed", "no_answer", "busy", "failed") or time.monotonic() + step > deadline:
                return s
            time.sleep(step)

    def sms(self, to: str, from_: str, message: str, idempotency_key: Optional[str] = None, **extra: Any) -> Any:
        """POST /comms/sms - send one SMS (scope sms:send)."""
        return self._c.request(
            "POST", "/comms/sms", json={"to": to, "from": from_, "message": message, **extra}, idempotency_key=idempotency_key
        )

    def voice_otp(
        self,
        to: str,
        code: Optional[str] = None,
        length: Optional[int] = None,
        language: Optional[str] = None,
        repeat: Optional[int] = None,
        from_: Optional[str] = None,
        brand: Optional[str] = None,
        return_code: Optional[bool] = None,
        idempotency_key: Optional[str] = None,
        **extra: Any,
    ) -> Any:
        """POST /comms/voice-otp - call ``to`` and speak a one-time passcode (scope voice:send).

        The code is spoken digit by digit and repeated (``repeat`` 1-3, default 2), then the
        call hangs up. Omit ``code`` to have a ``length``-digit code (4-10, default 6)
        generated; it is only returned when ``return_code=True``. ``language`` is one of
        en, es, fr, de, pt, hi. Returns as soon as the call is dialled: read the outcome
        with :meth:`get_voice_otp`. For send-and-check, prefer ``px.verify.start(channel="voice")``.
        """
        body = _clean({
            "to": to, "code": code, "length": length, "language": language, "repeat": repeat,
            "from": from_, "brand": brand, "returnCode": return_code,
        })
        return self._c.request("POST", "/comms/voice-otp", json={**body, **extra}, idempotency_key=idempotency_key)

    def get_voice_otp(self, voice_otp_id: str) -> Any:
        """GET /comms/voice-otp/{id} - status, duration and cost of a voice passcode call."""
        return self._c.request("GET", f"/comms/voice-otp/{_seg(voice_otp_id)}")

    def get_sms(self, message_id: str) -> "_m.CommsSmsStatus":
        """GET /comms/sms/{messageId} - delivery status and timeline of one message.

        ``timeline`` runs queued -> sent -> delivered | failed, each step with a timestamp;
        ``errorCode`` is set on failure. ``delivered`` only ever comes from a carrier
        delivery receipt: on a route that returns none the message stays ``sent`` with
        ``awaitingReceipt`` true (see ``routeReturnsReceipts``). An unknown id returns
        ``status == "not_found"`` rather than raising.
        """
        return cast("_m.CommsSmsStatus", self._c.request("GET", f"/comms/sms/{_seg(message_id)}"))


class DidsResource(_Resource):
    """Phone numbers (the DID Store)."""

    def search(self, **filters: Any) -> Any:
        """GET /dids/search - search the catalogue (pattern, match, countryId, typeId...)."""
        return self._c.request("GET", "/dids/search", query=filters)

    def buy(self, sku_id: str, group_id: str, idempotency_key: Optional[str] = None, **extra: Any) -> Any:
        """POST /dids/buy - buy a number."""
        return self._c.request(
            "POST", "/dids/buy", json={"skuId": sku_id, "groupId": group_id, **extra}, idempotency_key=idempotency_key
        )

    def list(self) -> Any:
        """GET /dids/mine - numbers you hold."""
        return self._c.request("GET", "/dids/mine")

    def get_ai_agent(self, did_id: str) -> "_m.DidAiAgent":
        """GET /dids/{id}/ai-agent - which AI voice agent answers this number (scope numbers:read)."""
        return cast("_m.DidAiAgent", self._c.request("GET", f"/dids/{_seg(did_id)}/ai-agent"))

    def set_ai_agent(self, did_id: str, agent_id: Optional[str]) -> "_m.DidAiAgent":
        """PUT /dids/{id}/ai-agent - have one of your AI agents answer inbound calls.

        Pass ``None`` to go back to the number's call flow. Billed per second at the AI
        voice per-minute rate; when the agent is disabled or your balance covers under 30
        seconds, the number rings its call flow as usual (scope numbers:write).
        """
        return cast("_m.DidAiAgent", self._c.request("PUT", f"/dids/{_seg(did_id)}/ai-agent", json={"agentId": agent_id}))


class WebhooksResource(_Resource):
    """Webhook endpoints and their deliveries.

    ``create``, ``update``, ``delete`` and ``rotate_secret`` need a dashboard session or
    an API key created with the ``webhooks:write`` permission; a full-access key does not
    include it. The signing secret is returned once, by ``create`` and ``rotate_secret``.
    """

    def list(self) -> Any:
        """GET /account/webhooks - endpoints (secrets redacted)."""
        return self._c.request("GET", "/account/webhooks")

    def create(self, url: str, events: Sequence[str]) -> "_m.WebhookWithSecret":
        """POST /account/webhooks - create an https endpoint; ``secret`` is returned once."""
        return cast("_m.WebhookWithSecret", self._c.request("POST", "/account/webhooks", json={"url": url, "events": list(events)}))

    def update(self, webhook_id: str, url: Optional[str] = None, events: Optional[Sequence[str]] = None,
               is_active: Optional[bool] = None) -> "_m.Webhook":
        """PATCH /account/webhooks/{id} - change url, events or isActive (secret kept)."""
        body = _clean({"url": url, "events": list(events) if events is not None else None, "isActive": is_active})
        return cast("_m.Webhook", self._c.request("PATCH", f"/account/webhooks/{_seg(webhook_id)}", json=body))

    def delete(self, webhook_id: str) -> Dict[str, Any]:
        """DELETE /account/webhooks/{id} - remove the endpoint and its delivery history."""
        return cast(Dict[str, Any], self._c.request("DELETE", f"/account/webhooks/{_seg(webhook_id)}"))

    def rotate_secret(self, webhook_id: str) -> Dict[str, Any]:
        """POST /account/webhooks/{id}/rotate-secret - new signing secret, returned once."""
        return cast(Dict[str, Any], self._c.request("POST", f"/account/webhooks/{_seg(webhook_id)}/rotate-secret"))

    def test(self, webhook_id: str) -> Dict[str, Any]:
        """POST /account/webhooks/{id}/test - queue a signed ``ping`` delivery."""
        return cast(Dict[str, Any], self._c.request("POST", f"/account/webhooks/{_seg(webhook_id)}/test"))

    def deliveries(self, webhook_id: Optional[str] = None, status: Optional[str] = None,
                   event: Optional[str] = None, cursor: Optional[str] = None, limit: Optional[int] = None) -> Page:
        """GET /account/webhooks/deliveries - deliveries across your endpoints."""
        return self._c.page(
            "/account/webhooks/deliveries",
            {"webhookId": webhook_id, "status": status, "event": event, "cursor": cursor, "limit": limit},
        )

    def get_delivery(self, delivery_id: str) -> Any:
        """GET /account/webhooks/deliveries/{deliveryId} - one delivery with its payload."""
        return self._c.request("GET", f"/account/webhooks/deliveries/{_seg(delivery_id)}")

    def resend(self, delivery_id: str) -> Any:
        """POST /account/webhooks/deliveries/{deliveryId}/resend - queue a copy with a fresh timestamp."""
        return self._c.request("POST", f"/account/webhooks/deliveries/{_seg(delivery_id)}/resend")


class LookupResource(_Resource):
    """Number lookup: prefix-based and free, limited to 60 lookups a minute."""

    def number(self, number: str) -> "_m.NumberLookup":
        """GET /lookup/{number} - validate and format ``number`` (international format).

        Returns its country, line type (mobile, fixed, toll_free, premium or unknown), the
        network where the exchange's rate decks agree, blocked and high-risk flags and the
        cheapest live voice and SMS price. No carrier HLR query is made, so porting and
        in-service status are not visible. A malformed number returns ``valid`` False
        with a ``reason`` rather than raising.
        """
        # Encode the whole segment so the leading "+" is sent as %2B, as the API documents.
        return cast("_m.NumberLookup", self._c.request("GET", f"/lookup/{quote(number.strip(), safe='')}"))


class ApiKeysResource(_Resource):
    def list(self) -> Any:
        """GET /account/api-keys - dashboard session only; an API key gets 403."""
        return self._c.request("GET", "/account/api-keys")


class AccountResource(_Resource):
    def get(self) -> Any:
        """GET /account - your profile."""
        return self._c.request("GET", "/account")

    def balance(self) -> Any:
        """GET /account/balance - balance and test credit (6-decimal strings)."""
        return self._c.request("GET", "/account/balance")

    def api_usage(self, days: int = 7, key_id: Optional[str] = None) -> Any:
        """GET /account/api-usage - volume, error rate, p95; ``key_id`` narrows to one key."""
        return self._c.request("GET", "/account/api-usage", query={"days": days, "keyId": key_id})


class BillingResource(_Resource):
    def transactions(self, **filters: Any) -> Page:
        """GET /billing/transactions - ledger entries, newest first."""
        return self._c.page("/billing/transactions", filters)

    def iterate_transactions(self, **filters: Any) -> Iterator[Any]:
        return self._c.paginate("/billing/transactions", filters)


class CliTestsResource(_Resource):
    """Caller-ID tests and route liveness tests.

    A route liveness test places one real test call per route to a handset in its
    country. Each route is charged the test price ONLY if it rang.
    """

    def preview_batch(self, route_ids: Sequence[str]) -> "_m.RouteTestPreview":
        """POST /cli-tests/batches/preview - what a route test would do and cost. Writes nothing."""
        return cast("_m.RouteTestPreview", self._c.request("POST", "/cli-tests/batches/preview", json={"routeIds": list(route_ids)}))

    def create_batch(self, route_ids: Sequence[str], search_label: str, display_cli: str) -> "_m.RouteTestBatch":
        """POST /cli-tests/batches - start a route test on 2 to 20 voice routes.
        Poll :meth:`get_batch` while ``active`` is true."""
        return cast("_m.RouteTestBatch", self._c.request(
            "POST",
            "/cli-tests/batches",
            json={"routeIds": list(route_ids), "searchLabel": search_label, "displayCli": display_cli},
        ))

    def list_batches(self, limit: Optional[int] = None) -> List["_m.RouteTestBatch"]:
        """GET /cli-tests/batches - your route tests, newest first (limit 1-50, default 20)."""
        return cast(List["_m.RouteTestBatch"], self._c.request("GET", "/cli-tests/batches", query={"limit": limit}))

    def get_batch(self, batch_id: str) -> "_m.RouteTestBatch":
        """GET /cli-tests/batches/{id} - live per-route status and results."""
        return cast("_m.RouteTestBatch", self._c.request("GET", f"/cli-tests/batches/{_seg(batch_id)}"))

    def cancel_batch(self, batch_id: str) -> "_m.RouteTestBatch":
        """POST /cli-tests/batches/{id}/cancel - cancel every route not yet called (never charged)."""
        return cast("_m.RouteTestBatch", self._c.request("POST", f"/cli-tests/batches/{_seg(batch_id)}/cancel"))


class VerifyResource(_Resource):
    """Verify API: send a one-time code by SMS or voice call, then check it (scope verify:write).

    The platform generates the code and stores only a keyed hash of it. A verification
    expires (``expiry_seconds``, default 600), allows 5 attempts and approves once.
    Sends are rate limited per number and per account; a refusal raises
    :class:`PacketExchangeError` with status 429 and code ``RATE_LIMITED``.
    """

    def start(
        self,
        to: str,
        channel: str,
        length: Optional[int] = None,
        language: Optional[str] = None,
        brand: Optional[str] = None,
        expiry_seconds: Optional[int] = None,
        from_: Optional[str] = None,
        strategy: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Any:
        """POST /verify/start - create a verification and send the code.

        ``channel`` is ``"sms"`` or ``"voice"``. On a test key nothing is sent and the
        result carries ``testCode`` so a sandbox flow can be completed end to end.
        """
        body = _clean({
            "to": to, "channel": channel, "length": length, "language": language, "brand": brand,
            "expirySeconds": expiry_seconds, "from": from_, "strategy": strategy,
        })
        return self._c.request("POST", "/verify/start", json=body, idempotency_key=idempotency_key)

    def check(self, verification_id: str, code: str) -> Any:
        """POST /verify/check - returns ``status``: approved, denied, expired or max_attempts."""
        return self._c.request("POST", "/verify/check", json={"verificationId": verification_id, "code": code})

    def get(self, verification_id: str) -> Any:
        """GET /verify/{id} - current state of a verification (never includes the code)."""
        return self._c.request("GET", f"/verify/{_seg(verification_id)}")
