"""The single exception type the SDK raises for any failed request."""

from __future__ import annotations

from typing import Any, Optional


class PacketExchangeError(Exception):
    """Raised for any failed PacketExchange request.

    One exception type (rather than the raw envelope) so callers can branch on a
    stable ``code`` and ``status`` instead of matching message text.

    Attributes:
        code: The API's symbolic code (``VALIDATION_ERROR``, ``INVALID_INPUT``,
            ``RATE_LIMITED``...), or a synthetic ``HTTP_<status>`` /
            ``NETWORK_ERROR`` when the body carried none.
        message: Human-readable explanation.
        status: HTTP status; 0 for a transport failure before any response.
        details: For ``VALIDATION_ERROR``, a list of ``{"path", "message"}``;
            some codes attach an object; usually ``None`` otherwise.
        request_id: The ``X-Request-Id`` response header (a UUID). Quote it to
            support: it matches the server log for this exact request.
    """

    def __init__(
        self,
        code: str,
        message: str,
        status: int,
        details: Optional[Any] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details
        self.request_id = request_id

    @property
    def is_auth_error(self) -> bool:
        """True for 401/403: a bad, missing or under-scoped credential."""
        return self.status in (401, 403)

    @property
    def is_rate_limited(self) -> bool:
        """True for 429: back off for the Retry-After seconds, then retry."""
        return self.status == 429

    def __repr__(self) -> str:
        return (
            f"PacketExchangeError(code={self.code!r}, status={self.status}, "
            f"message={self.message!r}, request_id={self.request_id!r})"
        )
