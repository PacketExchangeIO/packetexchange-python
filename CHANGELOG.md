# Changelog

All notable changes to the `packetexchange` Python SDK are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: [github.com/PacketExchangeIO/packetexchange-python/compare/v0.3.1...HEAD](https://github.com/PacketExchangeIO/packetexchange-python/compare/v0.3.1...HEAD)
[0.3.1]: [github.com/PacketExchangeIO/packetexchange-python/releases/tag/v0.3.1](https://github.com/PacketExchangeIO/packetexchange-python/releases/tag/v0.3.1)
