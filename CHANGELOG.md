# Changelog

All notable changes to the `packetexchange` Python SDK are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-11-11

### Added

- Route checks, as `routes.checks`: `create(route_ids, number=, mode=)` for
  `POST /routes/check` (1 to 3 routes, network or `ring_me` mode), `get(check_id)`,
  `list(limit=)`, `coverage(route_ids, number=)` (whether a public test line exists),
  `send_sms(route_id, number)` for a test message over an SMS route, and
  `purchase(check_id)`, which buys the routes that passed and puts them at the top of
  your routing order. `create`, `send_sms` and `purchase` accept `idempotency_key`.
- Least-cost routing and failover on `purchases`: `lcr(to)` shows every route that can
  carry a number in the order a call tries them, `set_lcr_order(order)` reorders them
  for that number, `failover()` lists first-choice and backup routes per destination,
  `set_failover_price_limit(price_limit)` caps how much more a backup may cost (or turns
  failover off), and `owned(route_id)` returns your purchase of a route or `None`.
- `cli_tests.quote(route_id)` prices one caller-ID test on a route, and
  `cli_tests.test_countries(route_id)` lists the countries such a test can call.
- Call-in verification: `verify.start()` accepts `channel="call_in"`, plus `reference`
  and `route`. `verify.list(reference=, status=, channel=, limit=)` lists recent
  verifications, and `verify.simulate_call(id)` approves a test-key call-in
  verification. `verify.call_in` has `coverage()`, `list_numbers()`,
  `add_number(phone_number_id)` and `remove_number(phone_number_id)`.
- Billing reports: `billing.earnings(window=)`, `billing.hold_schedule()` and
  `billing.failure_summary(days=)`.
- A-Z price list: `billing.price_list()` and `billing.my_price_list()` return the
  workbook (`.xlsx`) as bytes, and `billing.price_list_info()` describes the current
  list. The client gains `request_bytes()` for file downloads; failures still raise
  `PacketExchangeError` from the API's error envelope.
- `account.destination_alerts` with `list()`, `create(country, traffic_type)` and
  `delete(alert_id)`.
- `notifications` resource: `preferences()` and `set_preferences(action_email)` for the
  "needs attention" digest email.
- `dids.call_capacity(did_id)` and `dids.set_call_capacity(did_id, max_calls)` for how
  many calls a number takes at once.
- Generated models include `RouteCheck`, `RouteCheckPurchase`, `LcrView`,
  `FailoverOverview`, `CallInVerification`, `CallInCoverage`, `CallInNumber`,
  `AccountDestinationAlert`, `NotificationEmailPrefs` and `DidCallCapacityOffer`.

### Removed

- Operations that are no longer part of the public API spec leave `OPERATIONS`, so
  `call_operation()` now raises `ValueError` for their ids: sign-in and account security
  under `/auth/*` (including the session list and revoke operations under
  `/auth/sessions`, which need a dashboard session and refuse every API key), two-factor
  setup, email change, account closure, KYC, payouts, card setup, onboarding progress,
  Switch plan checkout and trial applications, favourites, saved searches, listing
  claims and the Switch mode setting. The generated
  models that only they used are removed: `AuthTokens`, `AuthSession`,
  `AuthDeviceSession`, `AuthMfaChallenge`, `AccountClosurePreview`,
  `AccountFavoriteRoute`, `AccountSavedSearch`, `KycStatus`, `Payout` and `Deleted`.

### Changed

- `openapi.json` and the generated models are refreshed from the API (version 1.3.0).
- Development dependencies updated: mypy 2.4.0, librt 0.16.0, ast-serialize 0.13.1,
  pluggy 1.7.0 and iniconfig 2.3.1. The release workflow uses
  `actions/upload-artifact` v6 and `actions/download-artifact` v7.

## [0.4.0] - 2026-09-23

### Added

- Published on PyPI as `packetexchange`: `pip install packetexchange`.
- Asynchronous calls: `comms.call_async(to, from_, actions=, language=)` sends
  `POST /comms/calls` with `async: true` and returns as soon as the call is being
  dialled (HTTP 202, `status` `"ringing"`, `callId`). `comms.get_call(call_id)` reads
  `GET /comms/calls/{id}`: live status (queued, ringing, answered, then completed,
  no_answer, busy or failed), timestamps, duration, cost, a plain-words `hangupReason`
  and gathered digits. `comms.wait_for_call(call_id)` polls until a final state.
  `comms.call()` still waits for the call to end.
- Call actions: pass `actions` (`say`, `play`, `gather`, `pause`, `hangup`) and a
  default `language` (en, es, fr, de, pt or hi) to `comms.call()` or
  `comms.call_async()`. Gathered digits are reported when the call ends.
- `comms.get_sms(message_id)` for `GET /comms/sms/{messageId}`: the delivery status and
  timeline (queued, sent, delivered or failed, each with a timestamp), `errorCode`,
  `awaitingReceipt` and `routeReturnsReceipts`. A message is `delivered` only when a
  carrier delivery receipt confirms it.
- `lookup` resource: `lookup.number(number)` for `GET /lookup/{number}`. Validation and
  formatting, country, line type, the network where the marketplace's rate decks agree,
  the network of the number range, blocked and high-risk flags, and the cheapest live
  voice and SMS price. Prefix-based and free, limited to 60 lookups a minute.
- Webhook endpoint management: `webhooks.create(url, events)`, `update(...)`,
  `delete(id)`, `rotate_secret(id)` and `test(id)`. Creating, editing, deleting and
  rotating need an API key with the `webhooks:write` scope, which must be chosen
  explicitly (a full-access key does not include it).
- Generated models: `CallAction`, `CommsCallAccepted`, `CommsCallStatus`,
  `CommsSmsStatus`, `SmsTimelineStep`, `NumberLookup`, `PricingDestination` and
  `PricingDestinationDetail`. The `Webhook` event list now includes `call.ringing`,
  `call.answered`, `call.gathered`, `sms.delivered` and `sms.failed`.

### Changed

- `openapi.json` and the generated models are refreshed from the API (version 1.2.0).
  `DidMessage` names its message identifier `providerMessageId`. SMS send results
  and number lookups include a `network` object when a route prices SMS per destination
  network. Test keys receive 403 `TEST_KEY_NOT_ALLOWED` for Switch changes and x402
  top-ups, which have no test mode.

### Fixed

- `verify_webhook_signature` accepts only a digits-only `X-PX-Timestamp`, signs the
  header text exactly as received, and treats a non-ASCII signature header as a
  mismatch instead of raising `TypeError`.

## [0.3.1] - 2026-09-23

### Added

- `verify` resource for the Verify API: `verify.start(to, channel, ...)` with channel
  `"sms"` or `"voice"`, `verify.check(verification_id, code)` and
  `verify.get(verification_id)`. The code is generated server-side and stored only as
  a keyed hash; each verification expires (default 600 seconds), allows 5 attempts and
  approves once. Sends are rate limited per number and per account (429
  `RATE_LIMITED`). On a test key nothing is sent and `testCode` is returned.
- `comms.voice_otp(to, ...)` for `POST /comms/voice-otp`: calls a number and speaks a
  one-time passcode digit by digit, repeated, then hangs up. `comms.get_voice_otp(id)`
  returns the outcome and cost.
- Generated models for the Verify API (`VerifyStartResult`, `VerifyCheckResult`,
  `Verification`, `VoiceOtpResult`, `VoiceOtpStatus`), and the Verify operations in
  `OPERATIONS`.

### Changed

- The SDK is distributed from its own repository,
  `PacketExchangeIO/packetexchange-python`, and installs from GitHub with
  `pip install git+https://github.com/PacketExchangeIO/packetexchange-python`.

## [0.3.0] - 2026-09-23

### Added

- `routes.price_number(number, type="voice")` for `GET /routes/price-number`: every
  marketplace route that serves a number, at the rate it would charge for that number,
  cheapest first (`models.PriceNumberResult`).
- Routing order on `purchases`: `routing_order()`, `set_routing_order(purchase_ids)`,
  `set_routing_priority(purchase_id, priority)` and `route_for(to)`, which answers
  "which of my routes would carry this number" with the same ranking as the live call
  path (`models.RouteForResult`).
- `purchases.upcoming_rate_changes(purchase_id)` for scheduled rate changes on a route
  you bought, and `purchases.accept_rate(purchase_id, accepted_rate=, deck_version=,
  change_id=)`; with `change_id` it accepts a scheduled change in advance.
- `cli_tests` resource for route liveness tests: `preview_batch(route_ids)`,
  `create_batch(route_ids, search_label, display_cli)`, `list_batches(limit)`,
  `get_batch(batch_id)` and `cancel_batch(batch_id)` (`models.RouteTestPreview`,
  `models.RouteTestBatch`).
- New generated models include `ListingHealth`, `BulkEndpointResult`,
  `RoutingOrderEntry`, `PurchaseUpcomingRateChanges`, `SwitchCustomerRateNotice` and
  `SwitchCustomerRateChange`.

### Changed

- Models and `OPERATIONS` are regenerated from the refreshed spec (listing health, bulk
  SMS delivery and SIP endpoint actions, the Switch rate-change notice endpoints, route
  liveness tests and Switch Do Not Call).

## [0.2.0] - 2026-09-23

First release of the spec-driven client, replacing the earlier hand-written 0.1.0
client of the same name.

### Added

- `PacketExchange` client (httpx): Bearer auth, `/api/v1` added automatically,
  `request()` / `request_envelope()` for any endpoint, `page()` / `paginate()` for
  cursor pagination, and `call_operation(operation_id, ...)` for every operation in
  the spec.
- Convenience methods: routes (list, get, resolve), purchases (list, create), offers
  (list, create), comms (call, sms), dids (search, buy, list), webhooks (list,
  deliveries, get_delivery, resend), api_keys (list), account (get, balance,
  api_usage with `key_id`), billing (transactions).
- `PacketExchangeError` with `code`, `message`, `status`, `details` (a list of
  `{path, message}` for VALIDATION_ERROR) and `request_id` (the X-Request-Id).
- `verify_webhook_signature()`: timestamped `X-PX-Signature` (v1) with replay
  tolerance, legacy `X-Webhook-Signature` fallback only when v1 headers are absent.
- `packetexchange.models`: TypedDicts generated from the spec's component schemas;
  `OPERATIONS`: every operation's method, path and tag.

[Unreleased]: https://github.com/PacketExchangeIO/packetexchange-python/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/PacketExchangeIO/packetexchange-python/releases/tag/v0.5.0
[0.4.0]: https://github.com/PacketExchangeIO/packetexchange-python/releases/tag/v0.4.0
[0.3.1]: https://github.com/PacketExchangeIO/packetexchange-python/releases/tag/v0.3.1
