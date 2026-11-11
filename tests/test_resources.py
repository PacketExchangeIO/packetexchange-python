"""Convenience methods send the documented method, path, query and body."""

from __future__ import annotations

import httpx
import pytest

from .conftest import MockApi


def test_verify_start_check_get(api: MockApi) -> None:
    px = api.client()
    px.verify.start("+447700900123", "voice", expiry_seconds=300, from_="+15551230000", idempotency_key="idem-1")
    px.verify.check("v1", "482913")
    px.verify.get("v1")
    start, check, get = api.calls
    assert (start.method, start.path) == ("POST", "/api/v1/verify/start")
    # None-valued options are omitted and Python names map to the API's camelCase fields.
    assert start.body == {"to": "+447700900123", "channel": "voice", "expirySeconds": 300, "from": "+15551230000"}
    assert start.headers["x-idempotency-key"] == "idem-1"
    assert (check.method, check.path, check.body) == ("POST", "/api/v1/verify/check", {"verificationId": "v1", "code": "482913"})
    assert (get.method, get.path) == ("GET", "/api/v1/verify/v1")


def test_voice_otp(api: MockApi) -> None:
    px = api.client()
    px.comms.voice_otp("+447700900123", code="4829", language="es", repeat=3, return_code=False, brand="Acme")
    px.comms.get_voice_otp("o1")
    send, status = api.calls
    assert (send.method, send.path) == ("POST", "/api/v1/comms/voice-otp")
    assert send.body == {"to": "+447700900123", "code": "4829", "language": "es", "repeat": 3, "brand": "Acme", "returnCode": False}
    assert (status.method, status.path) == ("GET", "/api/v1/comms/voice-otp/o1")


def test_price_number(api: MockApi) -> None:
    px = api.client()
    px.routes.price_number("+44 7700 900123")
    px.routes.price_number("+447700900123", type="sms")
    assert (api.calls[0].method, api.calls[0].path) == ("GET", "/api/v1/routes/price-number")
    assert api.calls[0].params == {"number": "+44 7700 900123", "type": "voice"}
    assert api.calls[1].params == {"number": "+447700900123", "type": "sms"}


def test_routing_order(api: MockApi) -> None:
    px = api.client()
    px.purchases.routing_order()
    px.purchases.set_routing_order(["p1", "p2"])
    px.purchases.set_routing_priority("p1", 1)
    px.purchases.set_routing_priority("p2", None)
    px.purchases.route_for("+447700900123")
    px.purchases.upcoming_rate_changes("p1")
    px.purchases.accept_rate("p1", change_id="c1")
    assert [(c.method, c.path) for c in api.calls] == [
        ("GET", "/api/v1/purchases/routing-order"),
        ("PUT", "/api/v1/purchases/routing-order"),
        ("PATCH", "/api/v1/purchases/p1/routing-priority"),
        ("PATCH", "/api/v1/purchases/p2/routing-priority"),
        ("GET", "/api/v1/purchases/route-for"),
        ("GET", "/api/v1/purchases/p1/upcoming-rate-changes"),
        ("POST", "/api/v1/purchases/p1/accept-rate"),
    ]
    assert api.calls[1].body == {"purchaseIds": ["p1", "p2"]}
    assert api.calls[2].body == {"priority": 1}
    assert api.calls[3].body == {"priority": None}
    assert api.calls[4].params == {"to": "+447700900123"}
    assert api.calls[6].body == {"changeId": "c1"}


def test_cli_test_batches(api: MockApi) -> None:
    px = api.client()
    px.cli_tests.preview_batch(["r1", "r2"])
    px.cli_tests.create_batch(["r1", "r2"], search_label="UK mobile", display_cli="+447700900123")
    px.cli_tests.list_batches(limit=5)
    px.cli_tests.get_batch("b1")
    px.cli_tests.cancel_batch("b1")
    assert [(c.method, c.path) for c in api.calls] == [
        ("POST", "/api/v1/cli-tests/batches/preview"),
        ("POST", "/api/v1/cli-tests/batches"),
        ("GET", "/api/v1/cli-tests/batches"),
        ("GET", "/api/v1/cli-tests/batches/b1"),
        ("POST", "/api/v1/cli-tests/batches/b1/cancel"),
    ]
    assert api.calls[0].body == {"routeIds": ["r1", "r2"]}
    assert api.calls[1].body == {"routeIds": ["r1", "r2"], "searchLabel": "UK mobile", "displayCli": "+447700900123"}
    assert api.calls[2].params == {"limit": "5"}


def test_webhook_deliveries_and_resend(api: MockApi) -> None:
    api.responder = None
    px = api.client()
    px.webhooks.deliveries(status="failed", limit=50)
    px.webhooks.resend("d1")
    assert api.calls[0].path == "/api/v1/account/webhooks/deliveries"
    assert api.calls[0].params == {"status": "failed", "limit": "50"}
    assert (api.calls[1].method, api.calls[1].path) == ("POST", "/api/v1/account/webhooks/deliveries/d1/resend")


def test_call_async_sends_actions_and_async_flag(api: MockApi) -> None:
    px = api.client()
    px.comms.call_async(
        "+447700900123",
        "+14155550100",
        actions=[{"say": "Press 1 to confirm."}, {"gather": {"digits": 1, "timeout": 5}}],
        language="es",
        idempotency_key="call-1",
    )
    (call,) = api.calls
    assert (call.method, call.path) == ("POST", "/api/v1/comms/calls")
    assert call.body == {
        "to": "+447700900123",
        "from": "+14155550100",
        "actions": [{"say": "Press 1 to confirm."}, {"gather": {"digits": 1, "timeout": 5}}],
        "language": "es",
        "async": True,
    }
    assert call.headers["x-idempotency-key"] == "call-1"


def test_get_call_and_wait_for_call(monkeypatch: pytest.MonkeyPatch) -> None:
    states = iter(["ringing", "answered", "completed"])

    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"success": True, "data": {"callId": "c1", "status": next(states)}})

    # Skip the real sleep between polls so the test runs instantly.
    monkeypatch.setattr("packetexchange._client.time.sleep", lambda _s: None)
    api = MockApi(responder=responder)
    px = api.client()
    done = px.comms.wait_for_call("c1", interval=1)
    assert done["status"] == "completed"
    assert [(c.method, c.path) for c in api.calls] == [("GET", "/api/v1/comms/calls/c1")] * 3


def test_get_sms_returns_the_delivery_timeline() -> None:
    timeline = [
        {"status": "queued", "at": "2026-09-23T10:00:00Z", "source": "platform"},
        {"status": "sent", "at": "2026-09-23T10:00:01Z", "source": "submit"},
        {"status": "delivered", "at": "2026-09-23T10:00:04Z", "source": "carrier_receipt"},
    ]
    api = MockApi(
        responder=lambda _r: httpx.Response(
            200, json={"success": True, "data": {"messageId": "m1", "status": "delivered", "timeline": timeline}}
        )
    )
    status = api.client().comms.get_sms("m1")
    assert (api.calls[0].method, api.calls[0].path) == ("GET", "/api/v1/comms/sms/m1")
    assert status["status"] == "delivered"
    assert [s["status"] for s in status["timeline"]] == ["queued", "sent", "delivered"]


def test_lookup_number_trims_and_encodes_the_number(api: MockApi) -> None:
    px = api.client()
    px.lookup.number(" +447700900123 ")
    px.lookup.number("+44/7700")
    first, second = api.calls
    assert (first.method, first.raw_path) == ("GET", "/api/v1/lookup/%2B447700900123")
    # A stray slash is encoded so it can never change the path.
    assert second.raw_path == "/api/v1/lookup/%2B44%2F7700"


def test_webhook_management(api: MockApi) -> None:
    px = api.client()
    px.webhooks.create("https://example.com/hooks", ["sms.delivered", "sms.failed"])
    px.webhooks.update("w1", is_active=False)
    px.webhooks.rotate_secret("w1")
    px.webhooks.test("w1")
    px.webhooks.delete("w1")
    assert [(c.method, c.path) for c in api.calls] == [
        ("POST", "/api/v1/account/webhooks"),
        ("PATCH", "/api/v1/account/webhooks/w1"),
        ("POST", "/api/v1/account/webhooks/w1/rotate-secret"),
        ("POST", "/api/v1/account/webhooks/w1/test"),
        ("DELETE", "/api/v1/account/webhooks/w1"),
    ]
    assert api.calls[0].body == {"url": "https://example.com/hooks", "events": ["sms.delivered", "sms.failed"]}
    assert api.calls[1].body == {"isActive": False}


def test_route_checks(api: MockApi) -> None:
    px = api.client()
    px.routes.checks.create(["r1", "r2"], number="+923001234567", mode="ring_me", idempotency_key="chk-1")
    px.routes.checks.create(["r1"])
    px.routes.checks.get("c1")
    px.routes.checks.list(limit=10)
    px.routes.checks.coverage(["r1", "r2"], number="92")
    px.routes.checks.send_sms("r3", "+35056012345", idempotency_key="sms-1")
    px.routes.checks.purchase("c1", idempotency_key="buy-1")
    assert [(c.method, c.path) for c in api.calls] == [
        ("POST", "/api/v1/routes/check"),
        ("POST", "/api/v1/routes/check"),
        ("GET", "/api/v1/routes/check/c1"),
        ("GET", "/api/v1/routes/checks"),
        ("GET", "/api/v1/routes/check/coverage"),
        ("POST", "/api/v1/routes/check/sms"),
        ("POST", "/api/v1/routes/check/c1/purchase"),
    ]
    create, bare = api.calls[0], api.calls[1]
    assert create.body == {"routeIds": ["r1", "r2"], "number": "+923001234567", "mode": "ring_me"}
    assert create.headers["x-idempotency-key"] == "chk-1"
    assert bare.body == {"routeIds": ["r1"]}
    assert api.calls[3].params == {"limit": "10"}
    # The API reads routeIds as one comma-separated query value.
    assert api.calls[4].params == {"routeIds": "r1,r2", "number": "92"}
    assert api.calls[5].body == {"routeId": "r3", "number": "+35056012345"}
    assert api.calls[5].headers["x-idempotency-key"] == "sms-1"
    assert api.calls[6].body is None
    assert api.calls[6].headers["x-idempotency-key"] == "buy-1"


def test_lcr_failover_and_owned(api: MockApi) -> None:
    px = api.client()
    px.purchases.lcr("+447700900123")
    px.purchases.set_lcr_order([{"purchaseId": "p2"}, {"routeId": "r9"}])
    px.purchases.failover()
    px.purchases.set_failover_price_limit("up_to_10")
    px.purchases.owned("r1")
    assert [(c.method, c.path) for c in api.calls] == [
        ("GET", "/api/v1/purchases/lcr"),
        ("PUT", "/api/v1/purchases/lcr-order"),
        ("GET", "/api/v1/purchases/failover"),
        ("PUT", "/api/v1/purchases/failover/price-limit"),
        ("GET", "/api/v1/purchases/owned/r1"),
    ]
    assert api.calls[0].params == {"to": "+447700900123"}
    assert api.calls[1].body == {"order": [{"purchaseId": "p2"}, {"routeId": "r9"}]}
    assert api.calls[3].body == {"priceLimit": "up_to_10"}


def test_owned_returns_none_when_not_held() -> None:
    api = MockApi(responder=lambda _r: httpx.Response(200, json={"success": True, "data": None}))
    assert api.client().purchases.owned("r1") is None


def test_cli_test_quote_and_countries(api: MockApi) -> None:
    px = api.client()
    px.cli_tests.quote("r1")
    px.cli_tests.test_countries("r1")
    quote, countries = api.calls
    assert (quote.method, quote.path, quote.params) == ("GET", "/api/v1/cli-tests/quote", {"routeId": "r1"})
    assert (countries.method, countries.path) == ("GET", "/api/v1/cli-tests/routes/r1/test-countries")


def test_verify_list_simulate_and_call_in(api: MockApi) -> None:
    px = api.client()
    px.verify.start("+447700900123", "call_in", reference="user-42", route="smart")
    px.verify.list(channel="call_in", status="pending", limit=10)
    px.verify.list()
    px.verify.simulate_call("v1")
    px.verify.call_in.coverage()
    px.verify.call_in.list_numbers()
    px.verify.call_in.add_number("n1")
    px.verify.call_in.remove_number("n1")
    assert [(c.method, c.path) for c in api.calls] == [
        ("POST", "/api/v1/verify/start"),
        ("GET", "/api/v1/verify"),
        ("GET", "/api/v1/verify"),
        ("POST", "/api/v1/verify/v1/simulate-call"),
        ("GET", "/api/v1/verify/call-in/coverage"),
        ("GET", "/api/v1/verify/call-in/numbers"),
        ("POST", "/api/v1/verify/call-in/numbers"),
        ("DELETE", "/api/v1/verify/call-in/numbers/n1"),
    ]
    assert api.calls[0].body == {"to": "+447700900123", "channel": "call_in", "reference": "user-42", "route": "smart"}
    assert api.calls[1].params == {"channel": "call_in", "status": "pending", "limit": "10"}
    assert api.calls[2].params == {}
    assert api.calls[6].body == {"phoneNumberId": "n1"}


def test_billing_reports(api: MockApi) -> None:
    px = api.client()
    px.billing.earnings(window=7)
    px.billing.earnings()
    px.billing.hold_schedule()
    px.billing.failure_summary(days=3)
    px.billing.price_list_info()
    assert [(c.method, c.path) for c in api.calls] == [
        ("GET", "/api/v1/billing/earnings"),
        ("GET", "/api/v1/billing/earnings"),
        ("GET", "/api/v1/billing/hold-schedule"),
        ("GET", "/api/v1/billing/cdrs/failure-summary"),
        ("GET", "/api/v1/price-list/meta"),
    ]
    assert api.calls[0].params == {"window": "7"}
    assert api.calls[1].params == {}
    assert api.calls[3].params == {"days": "3"}


def test_price_list_downloads_return_bytes() -> None:
    workbook = b"PK\x03\x04\x14\x00\x00\x00\x08\x00\xff\xfe"
    xlsx = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    api = MockApi(responder=lambda _r: httpx.Response(200, content=workbook, headers={"content-type": xlsx}))
    px = api.client()
    assert px.billing.price_list() == workbook
    assert px.billing.my_price_list() == workbook
    public, mine = api.calls
    assert (public.method, public.path) == ("GET", "/api/v1/price-list.xlsx")
    assert (mine.method, mine.path) == ("GET", "/api/v1/price-list/me.xlsx")
    assert public.headers["accept"] == xlsx
    assert public.headers["authorization"] == "Bearer test-key"


def test_destination_alerts_and_notification_preferences(api: MockApi) -> None:
    px = api.client()
    px.account.destination_alerts.list()
    px.account.destination_alerts.create("Pakistan", "voice")
    px.account.destination_alerts.delete("a1")
    px.notifications.preferences()
    px.notifications.set_preferences(action_email=False)
    assert [(c.method, c.path) for c in api.calls] == [
        ("GET", "/api/v1/account/destination-alerts"),
        ("POST", "/api/v1/account/destination-alerts"),
        ("DELETE", "/api/v1/account/destination-alerts/a1"),
        ("GET", "/api/v1/notifications/preferences"),
        ("PUT", "/api/v1/notifications/preferences"),
    ]
    assert api.calls[1].body == {"country": "Pakistan", "trafficType": "voice"}
    assert api.calls[4].body == {"actionEmail": False}


def test_did_call_capacity(api: MockApi) -> None:
    px = api.client()
    px.dids.call_capacity("d1")
    px.dids.set_call_capacity("d1", 4)
    get, put = api.calls
    assert (get.method, get.path) == ("GET", "/api/v1/dids/d1/call-capacity")
    assert (put.method, put.path, put.body) == ("PUT", "/api/v1/dids/d1/call-capacity", {"maxCalls": 4})
