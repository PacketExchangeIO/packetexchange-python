"""verify_webhook_signature: the v1 scheme and the legacy fallback."""

from __future__ import annotations

import hashlib
import hmac

from packetexchange import verify_webhook_signature

SECRET = "whsec_example"
BODY = b'{"event":"call.completed","data":{"callId":"c1"}}'
NOW = 1_760_000_000


def _sig(data: bytes) -> str:
    return hmac.new(SECRET.encode(), data, hashlib.sha256).hexdigest()


def _v1(ts: int = NOW) -> dict[str, str]:
    return {"X-PX-Timestamp": str(ts), "X-PX-Signature": f"v1={_sig(f'{ts}.'.encode() + BODY)}"}


def test_valid_v1_signature() -> None:
    result = verify_webhook_signature(SECRET, BODY, _v1(), now=NOW)
    assert result and (result.scheme, result.timestamp) == ("v1", NOW)


def test_header_names_are_case_insensitive_and_str_body_works() -> None:
    headers = {k.lower(): v for k, v in _v1().items()}
    assert verify_webhook_signature(SECRET, BODY.decode(), headers, now=NOW)


def test_rejects_stale_bad_and_tampered() -> None:
    assert verify_webhook_signature(SECRET, BODY, _v1(NOW - 301), now=NOW).reason == "stale_timestamp"
    bad = {"X-PX-Timestamp": "soon", "X-PX-Signature": "v1=00"}
    assert verify_webhook_signature(SECRET, BODY, bad, now=NOW).reason == "bad_timestamp"
    assert verify_webhook_signature(SECRET, BODY + b" ", _v1(), now=NOW).reason == "mismatch"


def test_no_legacy_fallback_when_one_v1_header_is_present() -> None:
    headers = {"X-PX-Timestamp": str(NOW), "X-Webhook-Signature": f"sha256={_sig(BODY)}"}
    result = verify_webhook_signature(SECRET, BODY, headers, now=NOW)
    assert (result.valid, result.scheme, result.reason) == (False, "v1", "missing_signature")


def test_legacy_signature_when_allowed() -> None:
    headers = {"X-Webhook-Signature": f"sha256={_sig(BODY)}"}
    assert verify_webhook_signature(SECRET, BODY, headers).scheme == "legacy"
    assert verify_webhook_signature(SECRET, BODY, headers)
    refused = verify_webhook_signature(SECRET, BODY, headers, allow_legacy=False)
    assert not refused and refused.reason == "legacy_disallowed"


def test_missing_signature() -> None:
    result = verify_webhook_signature(SECRET, BODY, {})
    assert (result.valid, result.scheme, result.reason) == (False, "none", "missing_signature")


def test_malformed_headers_are_rejected_without_raising() -> None:
    padded = {"X-PX-Timestamp": f" {NOW}", "X-PX-Signature": "v1=00"}
    assert verify_webhook_signature(SECRET, BODY, padded, now=NOW).reason == "bad_timestamp"
    non_ascii = {"X-PX-Timestamp": str(NOW), "X-PX-Signature": "v1=é"}
    assert verify_webhook_signature(SECRET, BODY, non_ascii, now=NOW).reason == "mismatch"
