"""Webhook signature verification.

Every delivery carries two signatures:

    X-PX-Timestamp:      <unix seconds at send time>
    X-PX-Signature:      v1=<hex HMAC-SHA256(secret, "<timestamp>.<raw body>")>   (current)
    X-Webhook-Signature: sha256=<hex HMAC-SHA256(secret, "<raw body>")>           (legacy)

The v1 signature covers the timestamp, so a captured delivery cannot be replayed
later. The legacy one has no timestamp and so cannot stop replays: it is checked
only when both v1 headers are absent, and can be refused outright with
``allow_legacy=False``.
"""

from __future__ import annotations

import hashlib
import hmac
import time
from typing import Mapping, NamedTuple, Optional, Union

Body = Union[str, bytes, bytearray]


class SignatureResult(NamedTuple):
    """Outcome of :func:`verify_webhook_signature`. Truthy when valid."""

    valid: bool
    scheme: str  # "v1", "legacy" or "none"
    reason: Optional[str] = None  # missing_signature | stale_timestamp | bad_timestamp | mismatch | legacy_disallowed
    timestamp: Optional[int] = None

    def __bool__(self) -> bool:  # lets callers write ``if verify_webhook_signature(...):``
        return self.valid


def _header(headers: Mapping[str, str], name: str) -> Optional[str]:
    # Frameworks differ on header casing; match case-insensitively.
    lname = name.lower()
    for k, v in headers.items():
        if k.lower() == lname:
            return v
    return None


def _hmac_hex(secret: str, data: bytes) -> str:
    return hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()


def _matches(given: str, expected: str) -> bool:
    # Compare as bytes: compare_digest refuses non-ASCII str, and a header is attacker input.
    return hmac.compare_digest(given.lower().encode(), expected.encode())


def verify_webhook_signature(
    secret: str,
    raw_body: Body,
    headers: Mapping[str, str],
    tolerance_seconds: int = 300,
    allow_legacy: bool = True,
    now: Optional[int] = None,
) -> SignatureResult:
    """Verify a PacketExchange webhook delivery.

    Pass the body EXACTLY as received (bytes are best). Re-serialising parsed JSON
    changes key order or whitespace and breaks the HMAC. Comparison is constant-time.
    """
    body = raw_body.encode() if isinstance(raw_body, str) else bytes(raw_body)
    ts_header = _header(headers, "X-PX-Timestamp")
    v1_header = _header(headers, "X-PX-Signature")

    if ts_header is not None or v1_header is not None:
        # A v1 delivery: never fall back to legacy here, or stripping the v1 headers
        # would dodge the replay check.
        if not ts_header or not v1_header:
            return SignatureResult(False, "v1", "missing_signature")
        # Digits only: the signature covers the header text exactly as sent.
        if not (ts_header.isascii() and ts_header.isdigit()):
            return SignatureResult(False, "v1", "bad_timestamp")
        ts = int(ts_header)
        current = int(time.time()) if now is None else now
        if abs(current - ts) > tolerance_seconds:
            return SignatureResult(False, "v1", "stale_timestamp", ts)
        expected = _hmac_hex(secret, f"{ts_header}.".encode() + body)
        candidates = [p.strip()[3:] for p in v1_header.split(",") if p.strip().startswith("v1=")]
        if any(_matches(c, expected) for c in candidates):
            return SignatureResult(True, "v1", None, ts)
        return SignatureResult(False, "v1", "mismatch", ts)

    legacy = _header(headers, "X-Webhook-Signature")
    if not legacy:
        return SignatureResult(False, "none", "missing_signature")
    if not allow_legacy:
        return SignatureResult(False, "legacy", "legacy_disallowed")
    given = legacy[7:] if legacy.startswith("sha256=") else legacy
    if _matches(given, _hmac_hex(secret, body)):
        return SignatureResult(True, "legacy")
    return SignatureResult(False, "legacy", "mismatch")
