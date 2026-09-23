"""HTTP core: auth, base URL, envelope handling, errors and pagination."""

from __future__ import annotations

import httpx
import pytest

from packetexchange import DEFAULT_BASE_URL, OPERATIONS, PacketExchange, PacketExchangeError

from .conftest import MockApi


def test_sends_bearer_key_to_api_v1(api: MockApi) -> None:
    api.responder = lambda _req: httpx.Response(200, json={"success": True, "data": {"id": "u1"}})
    px = api.client()
    assert px.account.get() == {"id": "u1"}
    assert DEFAULT_BASE_URL == "https://packetexchange.io"
    assert api.calls[0].path == "/api/v1/account"
    assert api.calls[0].headers["authorization"] == "Bearer test-key"


def test_base_url_may_include_api_prefix() -> None:
    seen: list[str] = []

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(str(req.url))
        return httpx.Response(200, json={"success": True, "data": {}})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    PacketExchange(api_key="k", base_url="http://127.0.0.1:4010/api/v1/", http_client=client).account.balance()
    assert seen == ["http://127.0.0.1:4010/api/v1/account/balance"]


def test_error_envelope_raises_packetexchange_error(api: MockApi) -> None:
    api.responder = lambda _req: httpx.Response(
        400,
        headers={"x-request-id": "3f1c2a9e-0000-4000-8000-000000000000"},
        json={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input",
                "details": [{"path": "to", "message": "Invalid E.164 number"}],
            },
        },
    )
    with pytest.raises(PacketExchangeError) as info:
        api.client().comms.sms(to="x", from_="Acme", message="hi")
    err = info.value
    assert (err.status, err.code) == (400, "VALIDATION_ERROR")
    assert err.details == [{"path": "to", "message": "Invalid E.164 number"}]
    assert err.request_id == "3f1c2a9e-0000-4000-8000-000000000000"
    assert not err.is_auth_error


def test_auth_and_rate_limit_flags(api: MockApi) -> None:
    api.responder = lambda req: (
        httpx.Response(401, json={"success": False, "error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}})
        if req.url.path.endswith("/account")
        else httpx.Response(429, json={"success": False, "error": {"code": "RATE_LIMITED", "message": "Too many requests"}})
    )
    px = api.client()
    with pytest.raises(PacketExchangeError) as auth:
        px.account.get()
    assert auth.value.is_auth_error
    with pytest.raises(PacketExchangeError) as limited:
        px.account.balance()
    assert limited.value.is_rate_limited


def test_non_json_error_body_gets_synthetic_code(api: MockApi) -> None:
    api.responder = lambda _req: httpx.Response(502, text="Bad Gateway")
    with pytest.raises(PacketExchangeError) as info:
        api.client().account.get()
    assert (info.value.code, info.value.status) == ("HTTP_502", 502)


def test_transport_failure_is_network_error() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=req)

    px = PacketExchange(api_key="k", http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(PacketExchangeError) as info:
        px.account.get()
    assert (info.value.code, info.value.status) == ("NETWORK_ERROR", 0)


def test_sms_body_and_idempotency_key(api: MockApi) -> None:
    api.client().comms.sms(to="+447700900123", from_="Acme", message="Your order 1042 has shipped.", idempotency_key="o-1042")
    call = api.calls[0]
    assert (call.method, call.path) == ("POST", "/api/v1/comms/sms")
    assert call.body == {"to": "+447700900123", "from": "Acme", "message": "Your order 1042 has shipped."}
    assert call.headers["x-idempotency-key"] == "o-1042"


def test_page_and_paginate_follow_the_cursor(api: MockApi) -> None:
    def responder(req: httpx.Request) -> httpx.Response:
        if req.url.params.get("cursor") == "c2":
            return httpx.Response(200, json={"success": True, "data": [{"id": "t3"}], "nextCursor": None, "hasMore": False})
        body = {"success": True, "data": [{"id": "t1"}, {"id": "t2"}], "nextCursor": "c2", "hasMore": True, "total": 3}
        return httpx.Response(200, json=body)

    api.responder = responder
    px = api.client()
    page = px.billing.transactions(limit=2)
    assert (page.next_cursor, page.has_more, page.total) == ("c2", True, 3)
    assert [t["id"] for t in px.billing.iterate_transactions()] == ["t1", "t2", "t3"]
    assert api.calls[-1].params["cursor"] == "c2"


def test_call_operation_fills_path_parameters(api: MockApi) -> None:
    assert len(OPERATIONS) > 100
    px = api.client()
    px.call_operation("getVerifyById", path_params={"id": "v/1"})
    assert api.calls[0].raw_path == "/api/v1/verify/v%2F1"
    with pytest.raises(ValueError):
        px.call_operation("noSuchOperation")
    with pytest.raises(ValueError):
        px.call_operation("getVerifyById")
