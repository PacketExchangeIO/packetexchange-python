"""Shared fixtures: a client wired to an in-memory transport that records requests."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import httpx
import pytest

from packetexchange import PacketExchange

Responder = Callable[[httpx.Request], httpx.Response]


@dataclass
class Recorded:
    """One request as the SDK sent it."""

    method: str
    path: str
    raw_path: str
    params: Dict[str, str]
    headers: httpx.Headers
    body: Any


@dataclass
class MockApi:
    """Records every request and answers with ``responder`` (default: empty success)."""

    responder: Optional[Responder] = None
    calls: List[Recorded] = field(default_factory=list)

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(
            Recorded(
                method=request.method,
                path=request.url.path,
                raw_path=request.url.raw_path.decode(),
                params=dict(request.url.params),
                headers=request.headers,
                body=json.loads(request.content) if request.content else None,
            )
        )
        if self.responder is not None:
            return self.responder(request)
        return httpx.Response(200, json={"success": True, "data": {}})

    def client(self, **kwargs: Any) -> PacketExchange:
        transport = httpx.MockTransport(self.handle)
        return PacketExchange(api_key="test-key", http_client=httpx.Client(transport=transport), **kwargs)


@pytest.fixture
def api() -> MockApi:
    return MockApi()
