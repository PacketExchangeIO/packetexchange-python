"""Convenience methods send the documented method, path, query and body."""

from __future__ import annotations

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
