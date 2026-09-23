"""PacketExchange Python SDK.

A small client for the PacketExchange voice and SMS marketplace API, with typed
models generated from the public OpenAPI spec.

    import os
    from packetexchange import PacketExchange

    px = PacketExchange(api_key=os.environ["PACKETEXCHANGE_API_KEY"])
"""

from ._client import DEFAULT_BASE_URL, Page, PacketExchange
from ._errors import PacketExchangeError
from ._generated import models
from ._generated.operations import OPERATIONS, Operation
from ._webhooks import SignatureResult, verify_webhook_signature

__version__ = "0.3.1"

__all__ = [
    "DEFAULT_BASE_URL",
    "OPERATIONS",
    "Operation",
    "Page",
    "PacketExchange",
    "PacketExchangeError",
    "SignatureResult",
    "models",
    "verify_webhook_signature",
    "__version__",
]
