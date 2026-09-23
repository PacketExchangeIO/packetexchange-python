# Do not edit by hand: produced by scripts/generate.py.
# Source: openapi.json (PacketExchange API 1.2.0).
# Regenerate with: python3 scripts/generate.py
"""Typed shapes of the API's documented schemas.

Money fields are USD decimal strings with 6 places ("0.012500"): use
decimal.Decimal for arithmetic, never float.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


Money = str  # US dollars as a decimal string with exactly 6 decimal places, e.g. "0.012500". Do money arithmetic with a decimal type, not floating point.

class _MessageRequired(TypedDict):
    message: str


class Message(_MessageRequired, total=False):
    pass


class _DeletedRequired(TypedDict):
    id: str
    deleted: Literal[True]


class Deleted(_DeletedRequired, total=False):
    pass


class _ValidationIssueRequired(TypedDict):
    path: str
    message: str


class ValidationIssue(_ValidationIssueRequired, total=False):
    pass


class _ErrorRequired(TypedDict):
    code: str
    message: str


class Error(_ErrorRequired, total=False):
    details: Union[List["ValidationIssue"], Dict[str, Any]]
    # VALIDATION_ERROR: an array of { path, message }. Some codes attach a code-specific object. Usually absent otherwise.


class _ErrorEnvelopeRequired(TypedDict):
    success: Literal[False]
    error: "Error"


class ErrorEnvelope(_ErrorEnvelopeRequired, total=False):
    pass


class _AccountProfileRequired(TypedDict):
    id: str
    email: str
    contactName: str
    companyName: Optional[str]
    jobTitle: Optional[str]
    phone: Optional[str]
    country: Optional[str]
    timezone: str
    companyLogoUrl: Optional[str]
    avatarUrl: Optional[str]
    role: Literal["user", "admin"]
    status: Literal["active", "suspended"]
    accountKind: str
    balance: "Money"
    testCredit: "Money"
    emailVerifiedAt: Optional[str]
    pendingEmail: Optional[str]
    verificationStatus: Literal["unverified", "verified"]
    kycStatus: Literal["not_started", "pending", "verified", "rejected"]
    totpEnabled: bool
    taxId: Optional[str]
    taxCountry: Optional[str]
    payoutMethod: Optional[str]
    onboardingGoal: Optional[str]
    onboardingDismissed: bool
    onboardingSeen: bool
    emailNotificationsOptOut: bool
    switchStatus: Literal["none", "active", "past_due", "canceled", "comp"]
    createdAt: str
    updatedAt: str


class AccountProfile(_AccountProfileRequired, total=False):
    pass


class _AccountBalanceRequired(TypedDict):
    balance: "Money"
    testCredit: "Money"
    total: "Money"


class AccountBalance(_AccountBalanceRequired, total=False):
    pass


class _AccountActivityEventRequired(TypedDict):
    id: str
    type: str
    ip: Optional[str]
    userAgent: Optional[str]
    meta: Optional[Dict[str, Any]]
    createdAt: str


class AccountActivityEvent(_AccountActivityEventRequired, total=False):
    pass


class _AccountClosurePreviewRequired(TypedDict):
    balanceUsd: str
    heldUsd: str
    withdrawableUsd: str
    minWithdrawalUsd: float
    pendingPayouts: int
    revshareEarningsUsd: str
    pendingRevsharePayouts: int
    canCloseNow: bool
    canWithdraw: bool
    revshareCanWithdraw: bool
    forfeitRequired: bool
    forfeitBalanceUsd: Optional[str]
    forfeitRevshareUsd: Optional[str]
    forfeitAmountUsd: Optional[str]
    message: str


class AccountClosurePreview(_AccountClosurePreviewRequired, total=False):
    pass


class _AccountSwitchEntitlementRequired(TypedDict):
    active: bool
    status: Literal["none", "active", "past_due", "canceled", "comp"]
    accessUntil: Optional[str]
    comp: bool
    nodeNft: bool
    priceUsd: float
    plan: str
    purchasablePlans: List[Literal["starter", "essentials", "standard", "growth", "carrier"]]
    onTrial: bool
    trialEndsAt: Optional[str]
    trialEligible: bool
    trialDays: int
    trialApplication: Optional[Dict[str, Any]]
    firstChargeDeferredTo: Optional[str]
    cancelAt: Optional[str]
    manageable: bool


class AccountSwitchEntitlement(_AccountSwitchEntitlementRequired, total=False):
    pass


class _AccountSpendAlertsRequired(TypedDict):
    lowBalanceThreshold: Optional[str]
    dailySpendCap: Optional[str]
    notifyEmail: bool
    updatedAt: Optional[str]


class AccountSpendAlerts(_AccountSpendAlertsRequired, total=False):
    pass


class _AccountSavedSearchRequired(TypedDict):
    id: str
    userId: str
    name: str
    filters: Dict[str, Any]
    createdAt: str


class AccountSavedSearch(_AccountSavedSearchRequired, total=False):
    pass


class _AccountFavoriteRouteRequired(TypedDict):
    favoriteId: str
    favoritedAt: str
    id: str
    type: Literal["voice", "sms"]
    country: str
    destinationName: str
    pricePerUnit: "Money"
    billingIncrement: Optional[str]
    status: str
    expectedAsr: Optional[str]
    expectedAcd: Optional[str]
    dialerCompatible: bool


class AccountFavoriteRoute(_AccountFavoriteRouteRequired, total=False):
    pass


class _AccountDedicatedIpRequired(TypedDict):
    assignmentId: str
    ipId: str
    address: str
    role: Literal["ingress", "egress"]
    boundBox: Optional[str]
    assignedAt: str
    hint: str


class AccountDedicatedIp(_AccountDedicatedIpRequired, total=False):
    pass


class _AccountActivatedIpRequired(TypedDict):
    assignmentId: str
    ipId: str
    address: str
    role: Literal["ingress", "egress"]
    boundBox: Optional[str]
    assignedAt: str
    hint: str
    created: bool
    monthlyPriceUsd: float
    charged: float


class AccountActivatedIp(_AccountActivatedIpRequired, total=False):
    pass


class _AccountInterconnectRequired(TypedDict):
    myIngressIp: Optional[str]
    myEgressIp: Optional[str]
    edgeIp: str
    egressIps: List[str]
    rtpPortRange: str
    sipPort: int
    onPlatform: bool
    onPlatformSignals: Dict[str, Any]
    autoAuthorized: bool
    manualWhitelistNeeded: bool
    authorizedIps: List[str]
    poolAvailable: int
    egressPoolAvailable: int
    egressAvailable: bool
    sipUsername: Optional[str]
    hasSipPassword: bool


class AccountInterconnect(_AccountInterconnectRequired, total=False):
    enabled: bool
    egressPendingNetwork: bool


class _AccountConnectivityBriefRequired(TypedDict):
    dedicatedIpsEnabled: bool
    myAddress: Optional[str]
    myAddressSummary: str
    sendTo: str
    sendToPort: int
    sendToSummary: str
    egressMode: Literal["dedicated", "shared"]
    egressAddresses: List[str]
    egressSummary: str
    authMethods: List[Literal["ip", "digest"]]
    authSummary: str
    authorizedSourceIps: List[str]
    purchasedRoutes: List[Dict[str, Any]]
    rtpPortRange: str
    codecs: List[str]
    autoAuthorized: bool
    manualWhitelistNeeded: bool


class AccountConnectivityBrief(_AccountConnectivityBriefRequired, total=False):
    pass


class _AuthTokensRequired(TypedDict):
    accessToken: str
    refreshToken: str
    expiresIn: int


class AuthTokens(_AuthTokensRequired, total=False):
    pass


class _AuthSessionRequired(TypedDict):
    accessToken: str
    refreshToken: str
    expiresIn: int
    user: "AccountProfile"


class AuthSession(_AuthSessionRequired, total=False):
    pass


class _AuthMfaChallengeRequired(TypedDict):
    mfaRequired: Literal[True]
    mfaToken: str


class AuthMfaChallenge(_AuthMfaChallengeRequired, total=False):
    pass


class _AuthDeviceSessionRequired(TypedDict):
    id: str
    ip: Optional[str]
    userAgent: Optional[str]
    createdAt: str
    lastSeenAt: Optional[str]
    current: bool


class AuthDeviceSession(_AuthDeviceSessionRequired, total=False):
    pass


class _ApiKeyRequired(TypedDict):
    id: str
    keyPrefix: str
    label: str
    scopes: Optional[List[Literal["voice:send", "sms:send", "dialer:write", "routes:read", "account:read", "purchases:write", "offers:write", "billing:write", "numbers:read", "numbers:write", "account:write", "routes:write", "cdr:numbers", "application:write", "switch:manage", "verify:write", "webhooks:write"]]]
    environment: Literal["live", "test"]
    lastUsedAt: Optional[str]
    createdAt: str
    expiresAt: Optional[str]


class ApiKey(_ApiKeyRequired, total=False):
    pass


class _CreatedApiKeyRequired(TypedDict):
    id: str
    key: str
    keyPrefix: str
    prefix: str
    label: str
    scopes: Optional[List[Literal["voice:send", "sms:send", "dialer:write", "routes:read", "account:read", "purchases:write", "offers:write", "billing:write", "numbers:read", "numbers:write", "account:write", "routes:write", "cdr:numbers", "application:write", "switch:manage", "verify:write", "webhooks:write"]]]
    environment: Literal["live", "test"]
    expiresAt: Optional[str]


class CreatedApiKey(_CreatedApiKeyRequired, total=False):
    pass


class _WebhookRequired(TypedDict):
    id: str
    url: str
    secretLast4: str
    events: List[Literal["call.completed", "call.ringing", "call.answered", "call.gathered", "sms.sent", "sms.dlr", "sms.delivered", "sms.failed", "campaign.started", "campaign.completed", "topup.confirmed", "balance.low", "offer.received", "route.purchased", "sub_account.balance_low", "sub_account.suspended", "sub_account.resumed", "sub_account.topup_requested", "number.call.received", "number.sms.received", "number.voicemail.received", "invoice.created", "invoice.issued", "invoice.sent", "invoice.voided", "invoice.reissued", "invoice.payment", "credit_note.issued", "payable.created", "netting.run", "sell_rate.changed", "cost_rate.scheduled", "cost_rate.activated", "cost_rate.rolled_back", "sub_account.margin_below_floor", "ping"]]
    isActive: bool
    failureCount: int
    lastDeliveryAt: Optional[str]
    createdAt: str
    updatedAt: str


class Webhook(_WebhookRequired, total=False):
    pass


class _WebhookWithSecretRequired(TypedDict):
    id: str
    url: str
    secretLast4: str
    events: List[Literal["call.completed", "call.ringing", "call.answered", "call.gathered", "sms.sent", "sms.dlr", "sms.delivered", "sms.failed", "campaign.started", "campaign.completed", "topup.confirmed", "balance.low", "offer.received", "route.purchased", "sub_account.balance_low", "sub_account.suspended", "sub_account.resumed", "sub_account.topup_requested", "number.call.received", "number.sms.received", "number.voicemail.received", "invoice.created", "invoice.issued", "invoice.sent", "invoice.voided", "invoice.reissued", "invoice.payment", "credit_note.issued", "payable.created", "netting.run", "sell_rate.changed", "cost_rate.scheduled", "cost_rate.activated", "cost_rate.rolled_back", "sub_account.margin_below_floor", "ping"]]
    isActive: bool
    failureCount: int
    lastDeliveryAt: Optional[str]
    createdAt: str
    updatedAt: str
    secret: str


class WebhookWithSecret(_WebhookWithSecretRequired, total=False):
    pass


class _WebhookDeliveryRequired(TypedDict):
    id: str
    event: str
    status: Literal["pending", "sending", "delivered", "failed"]
    httpStatus: Optional[int]
    attempts: int
    lastError: Optional[str]
    nextRetryAt: Optional[str]
    createdAt: str
    deliveredAt: Optional[str]


class WebhookDelivery(_WebhookDeliveryRequired, total=False):
    webhookId: str
    # Present on the account-wide list
    url: str
    # The endpoint URL, on the account-wide list


class _ApiUsageRequired(TypedDict):
    totalRequests: int
    errorRate: float
    p95LatencyMs: int
    byDay: List[Dict[str, Any]]
    topEndpoints: List[Dict[str, Any]]
    keyId: Optional[str]


class ApiUsage(_ApiUsageRequired, total=False):
    pass


class _MarketplaceSellerProfileRequired(TypedDict):
    verified: bool
    sellerScore: Optional[int]


class MarketplaceSellerProfile(_MarketplaceSellerProfileRequired, total=False):
    """Trust signals only. The marketplace never names the seller behind a listing."""


class _MarketplaceRouteRequired(TypedDict):
    id: str
    kind: Literal["single", "blend"]
    type: Literal["voice", "sms"]
    country: str
    countryCode: str
    prefix: List[str]
    destinationName: str
    cliType: Literal["full_cli", "ncli", "partial_cli", "local_cli", "mixed_cli"]
    routeType: Literal["direct", "premium", "standard", "ncli"]
    pricePerUnit: "Money"
    billingIncrement: Optional[str]
    capacity: int
    expectedAsr: Optional[str]
    expectedAcd: Optional[str]
    expectedPdd: Optional[str]
    minAcd: Optional[int]
    minAsr: Optional[str]
    visibility: Literal["public", "private"]
    status: Literal["active", "paused", "suspended", "pending_review"]
    wholesaleCompatible: bool
    callcenterCompatible: bool
    dialerCompatible: bool
    retailCompatible: bool
    otpCompatible: bool
    notes: Optional[str]
    exchangeScore: Optional[int]
    lastQcAt: Optional[str]
    createdAt: str
    updatedAt: str
    isOwn: bool
    sellerProfile: Optional["MarketplaceSellerProfile"]
    rateCount: int


class MarketplaceRoute(_MarketplaceRouteRequired, total=False):
    """A route as a buyer sees it: no seller identity, endpoints or credentials."""
    smsType: Optional[Literal["a2p", "p2p", "both"]]
    priceTrend: Optional[Dict[str, Any]]
    # Real 24h price movement from the price history; null when the route has not repriced


class _OwnRouteRequired(TypedDict):
    id: str
    kind: Literal["single", "blend"]
    type: Literal["voice", "sms"]
    country: str
    countryCode: str
    prefix: List[str]
    destinationName: str
    cliType: Literal["full_cli", "ncli", "partial_cli", "local_cli", "mixed_cli"]
    routeType: Literal["direct", "premium", "standard", "ncli"]
    pricePerUnit: "Money"
    billingIncrement: Optional[str]
    capacity: int
    expectedAsr: Optional[str]
    expectedAcd: Optional[str]
    expectedPdd: Optional[str]
    minAcd: Optional[int]
    minAsr: Optional[str]
    visibility: Literal["public", "private"]
    status: Literal["active", "paused", "suspended", "pending_review"]
    wholesaleCompatible: bool
    callcenterCompatible: bool
    dialerCompatible: bool
    retailCompatible: bool
    otpCompatible: bool
    notes: Optional[str]
    exchangeScore: Optional[int]
    lastQcAt: Optional[str]
    createdAt: str
    updatedAt: str
    sellerId: str
    parentRouteId: Optional[str]
    isBundle: bool
    jingleSipIp: Optional[str]
    sipPort: Optional[int]
    techPrefix: Optional[str]
    sipAuthUsername: Optional[str]
    sipAuthPasswordSet: bool
    smsDeliveryUrl: Optional[str]
    smppHost: Optional[str]
    smppPort: Optional[int]
    smppSystemId: Optional[str]
    smppPasswordSet: bool
    endpointReachable: Optional[bool]
    endpointCheckedAt: Optional[str]


class OwnRoute(_OwnRouteRequired, total=False):
    """A route you listed, as only you (the seller) see it. Passwords are never returned."""
    smsType: Optional[Literal["a2p", "p2p", "both"]]
    isOwner: Literal[True]
    smsDeliveryMethod: Optional[Literal["http", "smpp"]]
    sellerProfile: Optional["MarketplaceSellerProfile"]
    # Trust signals only. The marketplace never names the seller behind a listing.
    rateCount: int


class _MarketplaceStatsRequired(TypedDict):
    total: int
    voiceCount: int
    smsCount: int
    destinations: int


class MarketplaceStats(_MarketplaceStatsRequired, total=False):
    avgPrice: Optional[float]
    # Signed-in callers only. Average list price (display figure)
    avgAsr: Optional[float]
    # Signed-in only. Average seller-stated ASR %
    measuredAsr: Optional[float]
    # Signed-in only. Measured ASR % over 30 days of real calls
    avgScore: Optional[int]
    # Signed-in only
    totalCapacity: int
    # Signed-in only


ConnectivityTestResult = TypedDict("ConnectivityTestResult", {"pass": bool, "barred": bool, "degraded": bool, "checks": List[Dict[str, Any]], "egressAddresses": str, "gatewayIp": str, "diagnostics": Dict[str, Any], "message": str}, total=False)

class _ResolvedRouteRequired(TypedDict):
    id: str
    destinationName: str
    country: str
    countryCode: str
    type: Literal["voice", "sms"]
    cliType: Optional[str]
    price: "Money"
    asr: Optional[float]
    acd: Optional[float]
    matchedPrefix: Optional[str]


class ResolvedRoute(_ResolvedRouteRequired, total=False):
    pass


class _PricedRouteRequired(TypedDict):
    id: str
    type: Literal["voice", "sms"]
    name: str
    country: str
    countryCode: str
    matchedPrefix: str
    destination: str
    rate: "Money"
    billingIncrement: Optional[str]
    pricedBy: Literal["deck", "flat"]
    expectedAsr: Optional[str]
    expectedAcd: Optional[str]
    cliType: str
    routeType: str
    capacity: int
    exchangeScore: Optional[int]
    isOwn: bool


class PricedRoute(_PricedRouteRequired, total=False):
    """One route that serves the number, at the rate it would charge for it. Never names the seller."""
    network: Optional[Dict[str, Any]]
    # SMS routes that price the country per mobile network: which network `rate` is for. Absent otherwise
    countryRate: Optional["Money"]
    # SMS routes that price per network: the price for other or unknown networks


class _RouteRateRequired(TypedDict):
    id: str
    routeId: str
    destinationName: str
    operator: Optional[str]
    prefix: str
    ratePerUnit: "Money"
    billingIncrement: Optional[str]
    minDuration: Optional[int]
    effectiveDate: Optional[str]
    status: str


class RouteRate(_RouteRateRequired, total=False):
    mccMnc: Optional[str]
    # SMS sheets priced by network code: the network the row price came from ("214" = whole country)
    operatorRates: Optional[List[Dict[str, Any]]]
    # SMS sheets priced by network: the price per destination network (charged per network when `networkPriced` is true). A message is charged its network's rate (networks not listed pay the All Operators rate when there is one); `ratePerUnit` is the price for other or unknown networks. The network is determined from the number's range (ported numbers may be priced at the network the range belongs to)
    networkPriced: bool
    # True when each SMS on this row is charged its destination network's rate from `operatorRates`; `ratePerUnit` then applies to other or unknown networks


class _RateSheetImportRequired(TypedDict):
    id: str
    routeId: str
    filename: str
    fileType: str
    status: str
    rowCount: Optional[int]
    currency: Optional[str]
    fxRate: Optional[str]
    errorMessage: Optional[str]
    createdAt: str
    appliedAt: Optional[str]


class RateSheetImport(_RateSheetImportRequired, total=False):
    columnMapping: Any
    previewRows: Any
    warnings: Any


class _ListingHealthRequired(TypedDict):
    listed: int
    live: int
    hidden: int
    reasons: List[Dict[str, Any]]


class ListingHealth(_ListingHealthRequired, total=False):
    pass


class _BulkEndpointResultRequired(TypedDict):
    updated: int
    skipped: List[Dict[str, Any]]


class BulkEndpointResult(_BulkEndpointResultRequired, total=False):
    wouldUpdate: int
    # Dry run (or nothing eligible): how many routes the call would change
    check: Dict[str, Any]
    # The one endpoint check run for the whole batch (an SMPP bind, a URL check or a SIP probe). pass is false only when confirmUnreachable applied a SIP endpoint anyway.
    dryRun: bool


class _PriceNumberResultRequired(TypedDict):
    number: str
    type: Literal["voice", "sms"]
    unit: Literal["min", "msg"]
    total: int
    routes: List["PricedRoute"]
    notice: Optional[Literal["sanctioned"]]


class PriceNumberResult(_PriceNumberResultRequired, total=False):
    pass


class _RouteAccessGrantRequired(TypedDict):
    id: str
    routeId: str
    userId: Optional[str]
    customPrice: Optional["Money"]
    inviteCode: Optional[str]
    status: Union[Literal["pending", "active", "revoked"], str]
    message: Optional[str]
    requestedAt: Optional[str]
    createdAt: str


class RouteAccessGrant(_RouteAccessGrantRequired, total=False):
    pass


class _RouteReportRequired(TypedDict):
    id: str
    routeId: str
    routeName: Optional[str]
    role: Literal["buyer", "seller"]
    buyerId: Optional[str]
    buyerLabel: str
    category: Literal["call_failure", "connectivity", "quality", "other"]
    subject: Optional[str]
    status: Literal["open", "acknowledged", "resolved", "confirmed", "reopened", "escalated", "closed"]
    escalated: bool
    unread: bool
    lastActivityAt: str
    createdAt: str
    resolvedAt: Optional[str]
    closedAt: Optional[str]


class RouteReport(_RouteReportRequired, total=False):
    evidence: Any
    # Call evidence; seller addresses are masked for the buyer
    verifyResult: Any


class _RouteReportThreadRequired(TypedDict):
    id: str
    routeId: str
    routeName: Optional[str]
    role: Literal["buyer", "seller"]
    buyerId: Optional[str]
    buyerLabel: str
    category: Literal["call_failure", "connectivity", "quality", "other"]
    subject: Optional[str]
    status: Literal["open", "acknowledged", "resolved", "confirmed", "reopened", "escalated", "closed"]
    escalated: bool
    unread: bool
    lastActivityAt: str
    createdAt: str
    resolvedAt: Optional[str]
    closedAt: Optional[str]
    messages: List[Dict[str, Any]]


class RouteReportThread(_RouteReportThreadRequired, total=False):
    evidence: Any
    # Call evidence; seller addresses are masked for the buyer
    verifyResult: Any


class _PurchaseRequired(TypedDict):
    id: str
    buyerId: str
    routeId: str
    status: Literal["active", "paused", "cancelled", "pending_review"]
    sipUsername: Optional[str]
    createdAt: str
    cancelledAt: Optional[str]
    agreedPrice: Optional["Money"]
    heldOldRate: Optional["Money"]
    heldNewRate: Optional["Money"]
    routingPriority: Optional[int]
    sipPassword: Optional[str]
    heldDeckVersion: Optional[str]
    route: Dict[str, Any]


class Purchase(_PurchaseRequired, total=False):
    pass


class _PurchaseDetailRequired(TypedDict):
    id: str
    buyerId: str
    routeId: str
    status: Literal["active", "paused", "cancelled", "pending_review"]
    sipUsername: Optional[str]
    createdAt: str
    cancelledAt: Optional[str]
    agreedPrice: Optional["Money"]
    heldOldRate: Optional["Money"]
    heldNewRate: Optional["Money"]
    routingPriority: Optional[int]
    requiresUsCompliance: bool
    reviewedAt: Optional[str]
    reviewNote: Optional[str]
    sipPasswordSet: bool
    smppSystemId: Optional[str]
    offerId: Optional[str]
    route: Optional[Dict[str, Any]]
    sipPublicIp: str


class PurchaseDetail(_PurchaseDetailRequired, total=False):
    pass


class _PurchaseRowRequired(TypedDict):
    id: str
    buyerId: str
    routeId: str
    status: Literal["active", "paused", "cancelled", "pending_review"]
    sipUsername: Optional[str]
    createdAt: str
    cancelledAt: Optional[str]
    agreedPrice: Optional["Money"]
    heldOldRate: Optional["Money"]
    heldNewRate: Optional["Money"]
    routingPriority: Optional[int]
    requiresUsCompliance: bool
    reviewedAt: Optional[str]
    reviewNote: Optional[str]
    sipPasswordSet: bool
    smppSystemId: Optional[str]
    offerId: Optional[str]


class PurchaseRow(_PurchaseRowRequired, total=False):
    pass


class _RoutingOrderEntryRequired(TypedDict):
    purchaseId: str
    routeId: str
    status: Literal["active", "paused", "cancelled", "pending_review"]
    routingPriority: Optional[int]
    createdAt: str
    destinationName: str
    country: str
    countryCode: str
    prefix: List[str]
    rateSheet: bool


class RoutingOrderEntry(_RoutingOrderEntryRequired, total=False):
    pass


class _RouteForCandidateRequired(TypedDict):
    position: int
    carries: bool
    purchaseId: Optional[str]
    routeId: str
    ownRoute: bool
    destinationName: str
    country: str
    matchedPrefix: Optional[str]
    matchedDigits: int
    routingPriority: Optional[int]
    rate: Optional["Money"]
    rateSheet: bool
    purchasedAt: Optional[str]
    behindBecause: Optional[Literal["prefix", "routing_order", "rate", "age", "route_id"]]


class RouteForCandidate(_RouteForCandidateRequired, total=False):
    pass


class _RoutingOrderResultRequired(TypedDict):
    order: List[Dict[str, Any]]


class RoutingOrderResult(_RoutingOrderResultRequired, total=False):
    pass


class _RouteForResultRequired(TypedDict):
    number: str
    carriedBy: Optional["RouteForCandidate"]
    reason: str
    decidedBy: Optional[Literal["prefix", "routing_order", "rate", "age", "route_id"]]
    candidates: List["RouteForCandidate"]
    refused: Optional[Dict[str, Any]]


class RouteForResult(_RouteForResultRequired, total=False):
    pass


class _PurchaseUpcomingRateChangesRequired(TypedDict):
    purchaseId: str
    affectsYou: bool
    changes: List[Dict[str, Any]]


class PurchaseUpcomingRateChanges(_PurchaseUpcomingRateChangesRequired, total=False):
    pass


class _OfferRequired(TypedDict):
    id: str
    routeId: str
    groupId: Optional[str]
    listPrice: Optional["Money"]
    proposedPrice: "Money"
    agreedPrice: Optional["Money"]
    status: Literal["pending", "countered", "accepted", "rejected", "withdrawn", "expired"]
    lastActor: Literal["buyer", "seller"]
    message: Optional[str]
    expiresAt: Optional[str]
    createdAt: str
    updatedAt: str
    role: Literal["buyer", "seller"]
    yourTurn: bool
    counterparty: str
    route: Optional[Dict[str, Any]]


class Offer(_OfferRequired, total=False):
    pass


CallAction = Union[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]

CommsCallAccepted = TypedDict("CommsCallAccepted", {"callId": str, "status": Literal["ringing"], "mode": Literal["async"], "to": str, "from": str, "actions": int, "statusUrl": str}, total=False)

CommsCallStatus = TypedDict("CommsCallStatus", {"callId": str, "status": Literal["queued", "ringing", "answered", "completed", "no_answer", "busy", "failed"], "mode": Literal["sync", "async"], "to": str, "from": str, "simulated": bool, "createdAt": str, "ringingAt": Optional[str], "answeredAt": Optional[str], "endedAt": Optional[str], "durationSeconds": Optional[int], "billableSeconds": Optional[int], "cost": Optional["Money"], "billingIncrement": Optional[str], "sipResponseCode": Optional[int], "hangupCause": Optional[str], "hangupReason": Optional[str], "error": Optional[str], "actions": Optional[List[Any]], "gathered": Optional[List[Dict[str, Any]]]}, total=False)

CommsCall = TypedDict("CommsCall", {"callId": str, "to": str, "from": str, "status": Literal["answered", "no_answer", "busy", "failed", "accepted"], "sipResponseCode": Optional[int], "hangupCause": Optional[str], "durationSeconds": int, "billableSeconds": int, "cost": "Money", "billingIncrement": str, "startedAt": str, "completedAt": str, "simulated": bool, "routeId": Optional[str], "attempts": List[Dict[str, Any]]}, total=False)

CommsSms = TypedDict("CommsSms", {"messageId": str, "to": str, "from": str, "status": Literal["sent", "delivered", "failed", "pending", "accepted"], "segments": int, "cost": "Money", "submittedAt": str, "simulated": bool, "network": Optional[Dict[str, Any]]}, total=False)

class _CommsHistoryEntryRequired(TypedDict):
    id: str
    userId: str
    type: str
    amount: "Money"
    balanceAfter: "Money"
    reference: Optional[str]
    relatedEntityType: Optional[str]
    relatedEntityId: Optional[str]
    callId: Optional[str]
    createdAt: str


class CommsHistoryEntry(_CommsHistoryEntryRequired, total=False):
    pass


class _SmsTimelineStepRequired(TypedDict):
    status: Literal["queued", "sent", "accepted", "delivered", "failed"]
    at: str
    source: Literal["platform", "submit", "carrier_receipt", "simulated"]


class SmsTimelineStep(_SmsTimelineStepRequired, total=False):
    errorCode: Optional[str]
    # On failed: SELLER_REJECTED, NO_ENDPOINT, UNDELIVERABLE, EXPIRED or REJECTED
    carrierStatus: Optional[str]
    # The carrier receipt's own status value, e.g. DELIVRD or UNDELIV
    carrierError: Optional[str]
    # The carrier receipt's own error value, when it sent one


CommsSmsStatus = TypedDict("CommsSmsStatus", {"messageId": str, "status": str, "to": Optional[str], "from": Optional[str], "segments": Optional[int], "errorCode": Optional[str], "timeline": List["SmsTimelineStep"], "awaitingReceipt": bool, "routeReturnsReceipts": Optional[bool], "dlrSupported": bool, "simulated": bool, "cost": "Money", "reference": Optional[str], "sentAt": str, "message": str}, total=False)

class _CommsBulkSmsResultRequired(TypedDict):
    total: int
    sent: int
    failed: int
    totalCost: "Money"
    results: List[Dict[str, Any]]


class CommsBulkSmsResult(_CommsBulkSmsResultRequired, total=False):
    pass


VoiceOtpResult = TypedDict("VoiceOtpResult", {"voiceOtpId": str, "callId": str, "status": Literal["initiated", "accepted"], "to": str, "from": str, "language": str, "codeLength": int, "repeat": int, "code": str, "cost": Optional["Money"], "simulated": bool, "createdAt": str}, total=False)

class _VoiceOtpStatusRequired(TypedDict):
    voiceOtpId: str
    callId: Optional[str]
    status: Literal["initiated", "answered", "no_answer", "busy", "failed", "accepted"]
    to: str
    language: str
    codeLength: int
    cost: Optional["Money"]
    durationSeconds: Optional[int]
    createdAt: str
    completedAt: Optional[str]


class VoiceOtpStatus(_VoiceOtpStatusRequired, total=False):
    simulated: bool


class _VerifyStartResultRequired(TypedDict):
    verificationId: str
    to: str
    channel: Literal["sms", "voice"]
    status: Literal["pending"]
    expiresAt: str
    maxAttempts: int
    sendRef: str
    sendStatus: str
    createdAt: str


class VerifyStartResult(_VerifyStartResultRequired, total=False):
    simulated: bool
    # Present and true for test keys: nothing was sent
    testCode: str
    # Test keys ONLY: the code, so a sandbox can complete the check. Never present on a live key


class _VerifyCheckResultRequired(TypedDict):
    verificationId: str
    status: Literal["approved", "denied", "expired", "max_attempts"]
    attemptsRemaining: int


class VerifyCheckResult(_VerifyCheckResultRequired, total=False):
    reason: Literal["wrong_code", "already_used", "not_pending"]
    # Why a check was not approved, when it is not obvious from `status`


class _VerificationRequired(TypedDict):
    verificationId: str
    to: str
    channel: Literal["sms", "voice"]
    status: Literal["pending", "approved", "expired", "max_attempts", "failed"]
    attempts: int
    maxAttempts: int
    expiresAt: str
    createdAt: str
    approvedAt: Optional[str]
    sendRef: Optional[str]
    sendStatus: Optional[str]


class Verification(_VerificationRequired, total=False):
    simulated: bool


class _DidCatalogSkuRequired(TypedDict):
    skuId: str
    channels: int
    setupPrice: float
    monthlyPrice: float


class DidCatalogSku(_DidCatalogSkuRequired, total=False):
    pass


class _DidCatalogGroupRequired(TypedDict):
    groupId: str
    country: str
    countryId: str
    countryPrefix: str
    city: Optional[str]
    areaPrefix: Optional[str]
    typeId: Optional[str]
    typeName: Optional[str]
    skus: List["DidCatalogSku"]


class DidCatalogGroup(_DidCatalogGroupRequired, total=False):
    pass


class _DidCatalogCountryRequired(TypedDict):
    countryId: str
    country: str
    countryPrefix: str


class DidCatalogCountry(_DidCatalogCountryRequired, total=False):
    pass


class _DidCatalogTypeRequired(TypedDict):
    id: str
    name: str


class DidCatalogType(_DidCatalogTypeRequired, total=False):
    pass


class _DidRequired(TypedDict):
    id: str
    number: Optional[str]
    country: Optional[str]
    countryCode: Optional[str]
    city: Optional[str]
    areaPrefix: Optional[str]
    didType: Optional[str]
    channelsIncluded: int
    status: Literal["pending", "active", "suspended", "released", "failed"]
    pointMode: Literal["unrouted", "sip", "forward"]
    pointsTo: Optional[str]
    pointsToBackup: Optional[str]
    autoRenew: bool
    setupPrice: "Money"
    monthlyPrice: "Money"
    orderedAt: Optional[str]
    activatedAt: Optional[str]
    nextRenewalAt: Optional[str]
    suspendedAt: Optional[str]
    releasedAt: Optional[str]
    endpointReachable: Optional[bool]
    endpointCause: Optional[str]
    endpointCheckedAt: Optional[str]
    aiAgentId: Optional[str]
    graceDays: int


class Did(_DidRequired, total=False):
    pass


class _DidBulkBuyResultRequired(TypedDict):
    requested: int
    succeeded: int
    failed: int
    skipped: int
    items: List[Dict[str, Any]]


class DidBulkBuyResult(_DidBulkBuyResultRequired, total=False):
    pass


class _DidCallFlowRequired(TypedDict):
    strategy: Literal["failover", "simultaneous"]
    timeoutSec: int
    endpoints: List[Dict[str, Any]]


class DidCallFlow(_DidCallFlowRequired, total=False):
    pass


class _DidSipLineLoginRequired(TypedDict):
    id: str
    sipUsername: str
    sipPassword: str
    server: str
    port: str


class DidSipLineLogin(_DidSipLineLoginRequired, total=False):
    pass


class _DidSipLineRequired(TypedDict):
    id: str
    sipUsername: str
    label: Optional[str]
    priority: int
    enabled: bool
    createdAt: str


class DidSipLine(_DidSipLineRequired, total=False):
    pass


class _DidCallsRequired(TypedDict):
    calls: List[Dict[str, Any]]
    summary: Dict[str, Any]


class DidCalls(_DidCallsRequired, total=False):
    pass


class _DidFeaturesRequired(TypedDict):
    voicemail: Dict[str, Any]
    recording: Dict[str, Any]
    ivr: Dict[str, Any]
    schedule: Dict[str, Any]
    assets: List[Dict[str, Any]]
    mediaLive: bool


class DidFeatures(_DidFeaturesRequired, total=False):
    pass


class _DidGreetingRequired(TypedDict):
    id: str
    kind: Literal["voicemail_greeting", "ivr_greeting"]
    name: Optional[str]
    mime: str
    createdAt: str


class DidGreeting(_DidGreetingRequired, total=False):
    pass


class _DidRecordingRequired(TypedDict):
    id: str
    kind: Literal["call", "voicemail"]
    fromNumber: Optional[str]
    toNumber: Optional[str]
    durationSec: int
    mime: Optional[str]
    byteSize: int
    heard: bool
    transcript: Optional[str]
    hasAudio: bool
    expiresAt: Optional[str]
    createdAt: str


class DidRecording(_DidRecordingRequired, total=False):
    pass


DidMessage = TypedDict("DidMessage", {"id": str, "direction": Literal["in", "out"], "from": str, "to": str, "peer": str, "body": str, "segments": int, "status": Literal["received", "queued", "sent", "delivered", "failed"], "error": Optional[str], "providerMessageId": Optional[str], "readAt": Optional[str], "createdAt": str}, total=False)

class _DidSmsSettingsRequired(TypedDict):
    smsEnabled: bool
    forwardWebhookUrl: Optional[str]
    notifyEmail: Optional[str]


class DidSmsSettings(_DidSmsSettingsRequired, total=False):
    pass


class _DidConversationRequired(TypedDict):
    peer: str
    lastBody: str
    lastDirection: Literal["in", "out"]
    lastStatus: Literal["received", "queued", "sent", "delivered", "failed"]
    lastAt: str
    unread: int
    total: int


class DidConversation(_DidConversationRequired, total=False):
    pass


class _DidAnalyticsRequired(TypedDict):
    number: Optional[str]
    status: str
    price: Dict[str, Any]
    spend: Dict[str, Any]
    usage: Dict[str, Any]
    window: Dict[str, Any]
    series: List[Dict[str, Any]]


class DidAnalytics(_DidAnalyticsRequired, total=False):
    pass


class _DidNumbersOverviewRequired(TypedDict):
    counts: Dict[str, Any]
    monthlyRecurring: float
    lifetimeSpend: float
    usage: Dict[str, Any]


class DidNumbersOverview(_DidNumbersOverviewRequired, total=False):
    pass


class _DidListingRequestViewRequired(TypedDict):
    ownedActiveDids: int
    request: Optional[Dict[str, Any]]
    prefill: Dict[str, Any]


class DidListingRequestView(_DidListingRequestViewRequired, total=False):
    pass


class _DidCliEligibleRequired(TypedDict):
    id: str
    cli: str
    number: str
    country: Optional[str]
    countryCode: Optional[str]
    city: Optional[str]
    didType: Optional[str]
    channels: int
    label: Optional[str]


class DidCliEligible(_DidCliEligibleRequired, total=False):
    pass


class _DidAiAgentRequired(TypedDict):
    didId: str
    agentId: Optional[str]
    agentName: Optional[str]
    agentEnabled: Optional[bool]
    live: bool
    ratePerMin: str


class DidAiAgent(_DidAiAgentRequired, total=False):
    pass


class _NumberLookupRequired(TypedDict):
    input: str
    valid: bool
    reason: Optional[str]
    e164: Optional[str]
    internationalFormat: Optional[str]
    country: Optional[Dict[str, Any]]
    numberType: Literal["mobile", "fixed", "toll_free", "premium", "unknown"]
    numberTypeConfidence: float
    operator: Optional[str]
    network: Optional[Dict[str, Any]]
    matchedPrefix: Optional[str]
    risk: Dict[str, Any]
    pricing: Dict[str, Any]
    method: Literal["prefix"]
    cachedAt: str


class NumberLookup(_NumberLookupRequired, total=False):
    pass


class _LedgerTransactionRequired(TypedDict):
    id: str
    userId: str
    type: Literal["topup", "charge", "credit", "payout", "platform_fee", "test_credit", "chargeback", "refund_reversal", "refund", "transfer"]
    amount: "Money"
    balanceAfter: "Money"
    reference: Optional[str]
    relatedEntityType: Optional[str]
    relatedEntityId: Optional[str]
    createdAt: str


class LedgerTransaction(_LedgerTransactionRequired, total=False):
    callId: Optional[str]
    # The call or message this line bills; equals the CDR callUuid


class _BillingCdrRequired(TypedDict):
    id: str
    callUuid: Optional[str]
    callGroupId: Optional[str]
    direction: Literal["outbound", "inbound"]
    kind: Literal["voice", "sms"]
    routeId: Optional[str]
    fromNumber: Optional[str]
    toNumber: Optional[str]
    cli: Optional[str]
    status: Optional[str]
    sipCode: Optional[int]
    hangupCause: Optional[str]
    durationSeconds: Optional[int]
    billedSeconds: Optional[int]
    segments: Optional[int]
    pddMs: Optional[int]
    buyerCost: Optional["Money"]
    sellerCredit: Optional["Money"]
    ratePerUnit: Optional["Money"]
    answeredAt: Optional[str]
    endedAt: Optional[str]
    createdAt: str


class BillingCdr(_BillingCdrRequired, total=False):
    """Supplier-side identity and network fields are nulled unless you are the seller on the record."""


class _BillingExportJobRequired(TypedDict):
    id: str
    type: Literal["cdr"]
    params: Dict[str, Any]
    status: Literal["pending", "running", "done", "failed"]
    rowCount: Optional[int]
    error: Optional[str]
    createdAt: str
    completedAt: Optional[str]
    downloadable: bool
    downloadUrl: Optional[str]


class BillingExportJob(_BillingExportJobRequired, total=False):
    pass


class _BillingDocumentRequired(TypedDict):
    id: str
    number: int
    type: Literal["topup_receipt", "statement"]
    amount: "Money"
    currency: str
    periodStart: Optional[str]
    periodEnd: Optional[str]
    createdAt: str


class BillingDocument(_BillingDocumentRequired, total=False):
    pass


class _TaxInvoiceSummaryRequired(TypedDict):
    id: str
    seq: int
    number: str
    period: str
    periodStart: str
    periodEnd: str
    currency: str
    subtotal: str
    taxAmount: str
    total: str
    createdAt: str


class TaxInvoiceSummary(_TaxInvoiceSummaryRequired, total=False):
    pass


class _TaxInvoiceRequired(TypedDict):
    id: str
    seq: int
    number: str
    period: str
    periodStart: str
    periodEnd: str
    currency: str
    subtotal: str
    taxAmount: str
    total: str
    createdAt: str
    dataJson: Optional[Dict[str, Any]]


class TaxInvoice(_TaxInvoiceRequired, total=False):
    pass


class _TopupRequired(TypedDict):
    id: str
    method: Literal["crypto", "wire", "stripe", "x402"]
    amountUsd: "Money"
    status: Literal["pending", "confirmed", "rejected"]
    cryptoToken: Optional[str]
    cryptoNetwork: Optional[str]
    cryptoTxHash: Optional[str]
    wireReference: Optional[str]
    depositAddress: Optional[str]
    depositMemo: Optional[str]
    createdAt: str
    confirmedAt: Optional[str]


class Topup(_TopupRequired, total=False):
    pass


class _PayoutRequired(TypedDict):
    id: str
    method: Literal["crypto", "wire"]
    amountUsd: "Money"
    status: Literal["pending", "processing", "completed", "rejected"]
    cryptoToken: Optional[str]
    cryptoNetwork: Optional[str]
    cryptoAddress: Optional[str]
    cryptoTxHash: Optional[str]
    wireBankDetails: Optional[Dict[str, Any]]
    adminNote: Optional[str]
    createdAt: str
    processedAt: Optional[str]


class Payout(_PayoutRequired, total=False):
    pass


class _AutoRechargeRequired(TypedDict):
    enabled: bool
    threshold: Optional[str]
    amount: Optional[str]
    dailyCap: Optional[str]
    hasDefaultCard: bool


class AutoRecharge(_AutoRechargeRequired, total=False):
    pass


class _DialerCampaignRequired(TypedDict):
    id: str
    userId: str
    routeId: Optional[str]
    name: str
    kind: Literal["voice", "sms"]
    environment: Literal["live", "test"]
    status: Literal["draft", "ready", "running", "paused", "completed", "failed"]
    messageBody: Optional[str]
    senderId: Optional[str]
    aiAgentId: Optional[str]
    concurrency: int
    maxCallDuration: int
    callInterval: int
    platformFeePerCall: "Money"
    totalNumbers: int
    totalClis: int
    cliSetId: Optional[str]
    cliStrategy: Optional[Dict[str, Any]]
    numbersDialed: int
    numbersAnswered: int
    numbersFailed: int
    totalDurationSeconds: int
    windowStartHour: Optional[int]
    windowEndHour: Optional[int]
    windowTz: Optional[str]
    maxAttempts: int
    retryDelayMinutes: int
    maxSpend: Optional["Money"]
    scheduleAt: Optional[str]
    startedAt: Optional[str]
    completedAt: Optional[str]
    createdAt: str
    updatedAt: str


class DialerCampaign(_DialerCampaignRequired, total=False):
    pass


class _DialerCampaignStatsRequired(TypedDict):
    totalNumbers: int
    numbersDialed: int
    numbersAnswered: int
    numbersFailed: int
    numbersPending: int
    totalDurationSeconds: int
    asr: float
    acd: float
    progress: float
    activeCalls: int
    totalSpend: float
    maxSpend: Optional[float]
    budgetProgress: Optional[float]


class DialerCampaignStats(_DialerCampaignStatsRequired, total=False):
    pass


class _DialerNumberRequired(TypedDict):
    id: str
    campaignId: str
    number: str
    status: Literal["pending", "dialing", "answered", "no_answer", "busy", "failed", "skipped"]
    sipResponseCode: Optional[int]
    durationSeconds: Optional[int]
    attempt: int
    nextAttemptAt: Optional[str]
    dialedAt: Optional[str]
    answeredAt: Optional[str]
    completedAt: Optional[str]
    createdAt: str
    cost: Optional["Money"]
    cli: Optional[str]
    sipCause: Optional[str]


class DialerNumber(_DialerNumberRequired, total=False):
    pass


class _DialerNumbersUploadResultRequired(TypedDict):
    count: int
    inserted: int
    skipped: int
    rejects: List[Dict[str, Any]]
    totalNumbers: int
    campaign: "DialerCampaign"


class DialerNumbersUploadResult(_DialerNumbersUploadResultRequired, total=False):
    pass


class _DialerCampaignCliRequired(TypedDict):
    id: str
    campaignId: str
    cli: str
    status: Literal["pending", "verified", "failed"]
    verified: bool
    verifiedAt: Optional[str]
    createdAt: str


class DialerCampaignCli(_DialerCampaignCliRequired, total=False):
    pass


class _DialerContactMappingRequired(TypedDict):
    headerRowIndex: int
    columns: Dict[str, Any]
    extraColumns: List[int]


class DialerContactMapping(_DialerContactMappingRequired, total=False):
    notes: str


class _DialerCallerIdSetRequired(TypedDict):
    id: str
    userId: str
    name: str
    description: Optional[str]
    createdAt: str
    updatedAt: str


class DialerCallerIdSet(_DialerCallerIdSetRequired, total=False):
    pass


class _DialerCallerIdNumberRequired(TypedDict):
    id: str
    setId: str
    cli: str
    label: Optional[str]
    country: Optional[str]
    countryCode: Optional[str]
    areaCode: Optional[str]
    source: Literal["upload", "paste", "manual", "revshare", "did"]
    enabled: bool
    weight: int
    dailyCap: Optional[int]
    campaignCap: Optional[int]
    hourlyCap: Optional[int]
    cooldownSec: Optional[int]
    status: Literal["active", "resting", "retired"]
    tags: List[str]
    notes: Optional[str]
    createdAt: str


class DialerCallerIdNumber(_DialerCallerIdNumberRequired, total=False):
    pass


class _DialerCallerIdAddResultRequired(TypedDict):
    inserted: int
    skipped: int
    rejects: List[Dict[str, Any]]


class DialerCallerIdAddResult(_DialerCallerIdAddResultRequired, total=False):
    pass


class _DialerRevshareCallerRequired(TypedDict):
    prefix: str
    fromCarrier: Optional[str]
    originIso: Optional[str]
    originCountry: Optional[str]
    originDialCode: Optional[str]
    callCount: int
    lastCallAt: Optional[str]
    dialable: bool


class DialerRevshareCaller(_DialerRevshareCallerRequired, total=False):
    pass


class _DialerContactListRequired(TypedDict):
    id: str
    userId: str
    name: str
    count: int
    createdAt: str


class DialerContactList(_DialerContactListRequired, total=False):
    pass


class _DialerCompatibleTargetsRequired(TypedDict):
    setId: str
    setName: str
    groups: List[Dict[str, Any]]
    saved: Optional[Dict[str, Any]]
    limitation: Optional[str]


class DialerCompatibleTargets(_DialerCompatibleTargetsRequired, total=False):
    pass


class _DialerSmsTemplateRequired(TypedDict):
    id: str
    userId: str
    name: str
    body: str
    createdAt: str


class DialerSmsTemplate(_DialerSmsTemplateRequired, total=False):
    pass


class _DialerCliSetRequired(TypedDict):
    id: str
    userId: str
    name: str
    clis: str
    createdAt: str


class DialerCliSet(_DialerCliSetRequired, total=False):
    pass


class _DialerContactParseResultRequired(TypedDict):
    hasHeader: bool
    columns: List[Dict[str, Any]]
    sampleRows: List[List[str]]
    dataRows: List[List[str]]
    suggestedMapping: "DialerContactMapping"
    rowCount: int
    truncated: bool


class DialerContactParseResult(_DialerContactParseResultRequired, total=False):
    pass


class _CliTestRequired(TypedDict):
    id: str
    routeId: Optional[str]
    blendRouteId: Optional[str]
    displayCli: str
    testCountry: str
    testNumber: Optional[str]
    status: Literal["scheduled", "pending", "dispatching", "in_progress", "completed", "failed", "not_tested", "cancelled"]
    recurrence: str
    scheduledAt: Optional[str]
    reportedCli: Optional[str]
    displayedCorrectly: Optional[bool]
    resultNotes: Optional[str]
    dispatchedAt: Optional[str]
    completedAt: Optional[str]
    createdAt: str


class CliTest(_CliTestRequired, total=False):
    pass


class _RouteTestItemRequired(TypedDict):
    testId: str
    routeId: str
    routeName: str
    country: str
    position: int
    attempts: int
    charged: float
    state: Literal["queued", "waiting_handset", "calling", "retrying", "rang", "no_ring", "not_tested", "cancelled"]
    label: str
    detail: Optional[str]
    ringReason: Optional[str]
    callerId: Dict[str, Any]
    updatedAt: str


class RouteTestItem(_RouteTestItemRequired, total=False):
    pass


class _RouteTestBatchRequired(TypedDict):
    id: str
    searchLabel: str
    status: Literal["running", "finished", "cancelled"]
    displayCli: str
    routeCount: int
    costPerTest: float
    costCeiling: float
    chargedTotal: float
    createdAt: str
    finishedAt: Optional[str]
    cancelledAt: Optional[str]
    active: bool
    callerIdPending: int
    summary: Dict[str, Any]
    items: List["RouteTestItem"]


class RouteTestBatch(_RouteTestBatchRequired, total=False):
    pass


class _RouteTestPreviewRequired(TypedDict):
    enabled: bool
    routes: List[Dict[str, Any]]
    testableCount: int
    minRoutes: int
    maxRoutes: int
    costPerTest: float
    maxCost: float
    balance: Optional[float]
    quota: Dict[str, Any]
    countries: List[Dict[str, Any]]
    estimatedSeconds: Optional[int]
    noHandsetCountries: List[str]
    handsetWaitMinutes: int
    gapSeconds: int
    maxParallel: int
    runningBatchId: Optional[str]


class RouteTestPreview(_RouteTestPreviewRequired, total=False):
    pass


class _DncEntryRequired(TypedDict):
    id: str
    userId: Optional[str]
    phoneNumber: str
    reason: Optional[str]
    source: Literal["manual", "sms_stop", "upload", "callguard_optout"]
    createdAt: str


class DncEntry(_DncEntryRequired, total=False):
    pass


class _AiAgentRequired(TypedDict):
    id: str
    userId: str
    name: str
    voiceId: Optional[str]
    voiceProvider: str
    language: str
    firstMessage: Optional[str]
    systemPrompt: str
    model: str
    guardrails: Optional[str]
    tools: List[str]
    maxCallSeconds: int
    enabled: bool
    createdAt: str
    updatedAt: str


class AiAgent(_AiAgentRequired, total=False):
    pass


class _AiVoiceRequired(TypedDict):
    id: str
    name: str
    description: str
    gender: str
    language: str
    is_pro: bool


class AiVoice(_AiVoiceRequired, total=False):
    pass


class _AiAgentDraftRequired(TypedDict):
    name: str
    firstMessage: str
    systemPrompt: str
    guardrails: str
    suggestedTools: List[str]


class AiAgentDraft(_AiAgentDraftRequired, total=False):
    pass


class _AiAgentTurnRequired(TypedDict):
    reply: str
    action: Literal["continue", "end", "transfer"]


class AiAgentTurn(_AiAgentTurnRequired, total=False):
    captured: Dict[str, Any]
    # Structured details captured this turn (name, email, intent...)


class _SwitchCustomerRequired(TypedDict):
    id: str
    label: str
    source: Literal["marketplace", "external"]
    status: Literal["draft", "active", "suspended", "closed"]
    externalRef: Optional[str]
    balance: "Money"
    creditLimit: str
    currency: Optional[str]
    markupPct: Optional[str]
    billingIncrement: Optional[str]
    minMarginPct: Optional[str]
    marginFloorAction: Optional[Literal["block", "alert"]]
    dailySpendCap: Optional[str]
    maxConcurrentCalls: Optional[int]
    maxCps: Optional[int]
    blockedPrefixes: Optional[List[str]]
    sipUsername: Optional[str]
    sipPasswordSet: bool
    portalEmail: Optional[str]
    taxCountry: Optional[str]
    taxId: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchCustomer(_SwitchCustomerRequired, total=False):
    pass


class _SwitchCustomerListRowRequired(TypedDict):
    id: str
    label: str
    source: Literal["marketplace", "external"]
    status: Literal["draft", "active", "suspended", "closed"]
    externalRef: Optional[str]
    balance: "Money"
    creditLimit: str
    currency: Optional[str]
    sipUsername: Optional[str]
    portalEmail: Optional[str]
    createdAt: str
    trunkCount: int
    trunksUp: int
    trunksDown: int
    liveCalls: int
    calls24h: int
    answered24h: int
    asr24h: Optional[float]
    revenue24h: float
    margin24h: float
    marginPct24h: Optional[float]
    pddMs24h: Optional[float]
    creditUsedPct: Optional[float]
    contact: Optional[Dict[str, Any]]
    attention: Optional[Dict[str, Any]]
    setup: Dict[str, Any]
    refused24h: Dict[str, Any]
    flags: List[str]


class SwitchCustomerListRow(_SwitchCustomerListRowRequired, total=False):
    pass


class _SwitchCustomerCreatedRequired(TypedDict):
    id: str
    label: str
    source: Literal["marketplace", "external"]
    status: Literal["draft", "active", "suspended", "closed"]
    externalRef: Optional[str]
    balance: "Money"
    creditLimit: str
    currency: Optional[str]
    markupPct: Optional[str]
    billingIncrement: Optional[str]
    minMarginPct: Optional[str]
    marginFloorAction: Optional[Literal["block", "alert"]]
    dailySpendCap: Optional[str]
    maxConcurrentCalls: Optional[int]
    maxCps: Optional[int]
    blockedPrefixes: Optional[List[str]]
    sipUsername: Optional[str]
    portalEmail: Optional[str]
    taxCountry: Optional[str]
    taxId: Optional[str]
    createdAt: str
    updatedAt: str
    sipPassword: str
    defaultTrunkId: str
    apiKey: str
    apiKeyPrefix: str


class SwitchCustomerCreated(_SwitchCustomerCreatedRequired, total=False):
    pass


class _SwitchCustomerSipCredentialsRequired(TypedDict):
    sipUsername: Optional[str]
    sipPassword: Optional[str]


class SwitchCustomerSipCredentials(_SwitchCustomerSipCredentialsRequired, total=False):
    pass


SwitchCustomerLifecycleEntry = TypedDict("SwitchCustomerLifecycleEntry", {"id": str, "at": str, "action": str, "from": Optional[str], "to": Optional[str], "reason": Optional[str], "actor": Optional[str], "detail": Dict[str, Any]}, total=False)

class _SwitchCustomerLifecycleRequired(TypedDict):
    customer: Dict[str, Any]
    available: List[Literal["activate", "suspend", "reactivate", "close", "reopen"]]
    liveCalls: int
    trunks: Dict[str, Any]
    history: List["SwitchCustomerLifecycleEntry"]
    financials: Dict[str, Any]
    canDelete: bool
    deleteBlockers: List[str]


class SwitchCustomerLifecycle(_SwitchCustomerLifecycleRequired, total=False):
    pass


class _SwitchCustomerOverviewRequired(TypedDict):
    customer: Dict[str, Any]
    kpis: Dict[str, Any]
    commercial: Dict[str, Any]
    activity: List[Dict[str, Any]]
    topDestinationsToday: List[Dict[str, Any]]


class SwitchCustomerOverview(_SwitchCustomerOverviewRequired, total=False):
    health: Any
    setup: Any
    reconciliation: Any
    freshness: Any


class _SwitchCustomerQualityRequired(TypedDict):
    windowHours: float
    window: Dict[str, Any]
    destinationDigits: int
    kpis: Dict[str, Any]
    destinations: List[Dict[str, Any]]
    minJudgeableSessions: int
    supports: List[str]
    unsupported: List[Any]


class SwitchCustomerQuality(_SwitchCustomerQualityRequired, total=False):
    thresholds: Any


class _SwitchCustomerContactRequired(TypedDict):
    id: str
    subAccountId: str
    name: str
    role: Literal["technical", "noc", "billing", "escalation", "commercial"]
    email: Optional[str]
    phone: Optional[str]
    priority: int
    isPrimary: bool
    preferredMethod: Literal["email", "phone", "either"]
    availability: Optional[Literal["24x7", "business_hours", "on_call"]]
    timezone: Optional[str]
    notes: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchCustomerContact(_SwitchCustomerContactRequired, total=False):
    pass


class _SwitchCustomerNoteRequired(TypedDict):
    id: str
    subAccountId: str
    body: str
    type: Literal["general", "technical", "billing", "warning"]
    pinned: bool
    followUpAt: Optional[str]
    createdBy: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchCustomerNote(_SwitchCustomerNoteRequired, total=False):
    pass


class _SwitchCustomerAttentionItemRequired(TypedDict):
    kind: Literal["quality", "commercial", "credit", "config", "setup"]
    title: str
    detail: str
    at: str
    actionable: bool


class SwitchCustomerAttentionItem(_SwitchCustomerAttentionItemRequired, total=False):
    pass


class _SwitchCustomerIssueRequired(TypedDict):
    ref: str
    detector: str
    severity: str
    status: str
    title: str
    summary: str
    trigger: str
    recovery: str
    sampleSize: float
    evidence: List[Dict[str, Any]]
    firstDetectedAt: str
    lastDetectedAt: str
    acknowledgedAt: Optional[str]
    resolvedAt: Optional[str]


class SwitchCustomerIssue(_SwitchCustomerIssueRequired, total=False):
    pass


class _SwitchCustomerBillingSummaryRequired(TypedDict):
    balanceOwed: float
    grossBalanceOwed: float
    creditNotesOpen: float
    paymentsRecorded: float
    creditLimit: float
    unbilledRated: float
    unbilledSinceLastInvoice: float
    unratedUsage: Dict[str, Any]
    overdueIsSubsetOfOpenInvoices: Literal[True]
    disputed: Optional[Literal["null"]]
    avgDaysToPay: Optional[float]
    lastInvoicePeriodEnd: Optional[str]
    currency: str
    aging: Dict[str, Any]


class SwitchCustomerBillingSummary(_SwitchCustomerBillingSummaryRequired, total=False):
    pass


class _SwitchCustomerCreditPositionRequired(TypedDict):
    customerId: str
    label: str
    currency: str
    mode: str
    creditLimit: Dict[str, Any]
    exposure: float
    balance: float
    reservations: Dict[str, Any]
    availableCredit: float
    availableAfterReservations: float
    admitsNextCall: bool
    usedPct: Optional[float]
    overCommitted: bool


class SwitchCustomerCreditPosition(_SwitchCustomerCreditPositionRequired, total=False):
    pass


class _SwitchCustomerPaymentRequired(TypedDict):
    kind: Literal["payment"]
    transactionId: str
    amount: float
    currency: str
    postedAt: str
    externalReference: Optional[str]
    method: Optional[str]
    operatorLabel: Optional[str]
    billingMode: str
    allocations: List[Dict[str, Any]]
    unapplied: float
    positionAfter: Dict[str, Any]


class SwitchCustomerPayment(_SwitchCustomerPaymentRequired, total=False):
    pass


class _SwitchCustomerInvoicePreviewRequired(TypedDict):
    customer: Dict[str, Any]
    period: Dict[str, Any]
    dueDate: str
    paymentTermsDays: int
    currency: str
    usage: Dict[str, Any]
    unrated: Dict[str, Any]
    reviewToken: str
    reviewDigest: str


class SwitchCustomerInvoicePreview(_SwitchCustomerInvoicePreviewRequired, total=False):
    pass


class _SwitchCustomerIssuedInvoiceRequired(TypedDict):
    id: str
    invoiceNumber: str
    customerId: str
    status: str
    subtotal: "Money"
    total: "Money"
    currency: str
    periodStart: str
    periodEnd: str
    issueDate: Optional[str]
    dueDate: Optional[str]
    lines: List[Dict[str, Any]]
    reviewDigest: Optional[str]


class SwitchCustomerIssuedInvoice(_SwitchCustomerIssuedInvoiceRequired, total=False):
    pass


class _SwitchCustomerBillingProfileRequired(TypedDict):
    id: str
    legalName: str
    version: int
    updatedAt: str


class SwitchCustomerBillingProfile(_SwitchCustomerBillingProfileRequired, total=False):
    pass


class _SwitchCustomerSellDeckRefRequired(TypedDict):
    id: str
    name: str
    version: int
    status: str
    currency: str
    isSystemDefault: bool
    defaultRatePerUnit: Optional[float]
    charging: Dict[str, Any]


class SwitchCustomerSellDeckRef(_SwitchCustomerSellDeckRefRequired, total=False):
    pass


class _SwitchTrunkEffectiveSellDeckRequired(TypedDict):
    deck: Optional["SwitchCustomerSellDeckRef"]
    mode: str
    choice: str
    bypassesCustomerDefault: bool
    customerDefault: Optional["SwitchCustomerSellDeckRef"]
    systemDefault: Optional["SwitchCustomerSellDeckRef"]
    liveRowCount: int
    explanation: str
    problem: Optional[str]


class SwitchTrunkEffectiveSellDeck(_SwitchTrunkEffectiveSellDeckRequired, total=False):
    pass


class _SwitchCustomerSellRateRequired(TypedDict):
    id: str
    subAccountId: str
    customerTrunkId: Optional[str]
    prefix: str
    originPrefix: str
    ratePerUnit: "Money"
    billingIncrement: Optional[str]
    status: str
    effectiveFrom: str
    endDate: Optional[str]


class SwitchCustomerSellRate(_SwitchCustomerSellRateRequired, total=False):
    pass


class _SwitchCustomerSellRatePageRequired(TypedDict):
    rows: List[Dict[str, Any]]
    total: int
    totalIsPageScoped: bool
    limit: int
    offset: int
    view: str
    summary: Dict[str, Any]


class SwitchCustomerSellRatePage(_SwitchCustomerSellRatePageRequired, total=False):
    basis: Any


class _SwitchCustomerTrunkRequired(TypedDict):
    id: str
    subAccountId: str
    label: str
    status: Literal["active", "disabled", "archived"]
    sipUsername: Optional[str]
    sipPasswordSet: bool
    maxConcurrentCalls: Optional[int]
    maxCps: Optional[int]
    markupPct: Optional[str]
    billingIncrement: Optional[str]
    techPrefix: Optional[str]
    cliRewrite: Optional[Dict[str, Any]]
    allowedPrefixes: Optional[List[str]]
    allowedCountries: Optional[List[str]]
    blockedCountries: Optional[List[str]]
    createdAt: str
    updatedAt: str


class SwitchCustomerTrunk(_SwitchCustomerTrunkRequired, total=False):
    authMode: Literal["ip", "credentials", "ip_and_credentials", "registration", "certificate"]
    mediaMode: Literal["proxy", "direct"]


class _SwitchCustomerTrunkListRowRequired(TypedDict):
    id: str
    subAccountId: str
    label: str
    status: Literal["active", "disabled", "archived"]
    sipUsername: Optional[str]
    sipPasswordSet: bool
    maxConcurrentCalls: Optional[int]
    maxCps: Optional[int]
    markupPct: Optional[str]
    billingIncrement: Optional[str]
    techPrefix: Optional[str]
    cliRewrite: Optional[Dict[str, Any]]
    allowedPrefixes: Optional[List[str]]
    allowedCountries: Optional[List[str]]
    blockedCountries: Optional[List[str]]
    createdAt: str
    updatedAt: str
    authentication: Dict[str, Any]
    identification: Dict[str, Any]
    allowedIps: List[str]
    allowedAddresses: List[Dict[str, Any]]
    routing: Optional[Dict[str, Any]]
    inherited: Dict[str, Any]
    last24h: Dict[str, Any]
    traffic: Dict[str, Any]
    refused: Dict[str, Any]


class SwitchCustomerTrunkListRow(_SwitchCustomerTrunkListRowRequired, total=False):
    authMode: Literal["ip", "credentials", "ip_and_credentials", "registration", "certificate"]
    mediaMode: Literal["proxy", "direct"]
    period: Any
    # The window the traffic figures cover


class _SwitchTrunkAddressPanelRequired(TypedDict):
    trunkId: str
    trunkLabel: str
    customerId: str
    entries: List[Dict[str, Any]]
    customerLevel: List[Dict[str, Any]]
    ambiguousCount: int
    activation: Dict[str, Any]


class SwitchTrunkAddressPanel(_SwitchTrunkAddressPanelRequired, total=False):
    pass


class _SwitchCustomerRoutingAssignmentRequired(TypedDict):
    subAccountId: str
    dialplanId: Optional[str]
    routePlanId: Optional[str]
    failoverRoutePlanId: Optional[str]
    strategyOverride: Optional[str]
    directRouteId: Optional[str]
    directVendorTrunkId: Optional[str]


class SwitchCustomerRoutingAssignment(_SwitchCustomerRoutingAssignmentRequired, total=False):
    customerTrunkId: Optional[str]


class _SwitchTrunkCredentialStatusRequired(TypedDict):
    trunkId: str
    trunkLabel: str
    customerId: str
    customerLabel: Optional[str]
    username: Optional[str]
    passwordSet: bool
    storage: Dict[str, Any]
    createdAt: str
    historyAvailable: bool
    lastSuccessfulAuth: Optional[Dict[str, Any]]


class SwitchTrunkCredentialStatus(_SwitchTrunkCredentialStatusRequired, total=False):
    lastChange: Any
    lastReveal: Any


class _SwitchTrunkEffectiveConfigRequired(TypedDict):
    trunk: Dict[str, Any]
    sections: List[Dict[str, Any]]
    capacity: Dict[str, Any]
    readOnly: Literal[True]


class SwitchTrunkEffectiveConfig(_SwitchTrunkEffectiveConfigRequired, total=False):
    pass


class _SwitchCustomerRateNoticeRequired(TypedDict):
    rateNoticeDays: int
    queued: int
    increases: int
    nextEffectiveFrom: Optional[str]
    defaultRecipients: List[str]


class SwitchCustomerRateNotice(_SwitchCustomerRateNoticeRequired, total=False):
    pass


class _SwitchCustomerRateChangeRequired(TypedDict):
    trunk: str
    prefix: str
    origin: str
    currentRate: Optional["Money"]
    newRate: "Money"
    changePct: Optional[float]
    currentIncrement: Optional[str]
    newIncrement: Optional[str]
    effectiveFrom: str


class SwitchCustomerRateChange(_SwitchCustomerRateChangeRequired, total=False):
    pass


class _SwitchSupplierTrunkRequired(TypedDict):
    id: str
    supplierId: Optional[str]
    label: str
    source: str
    status: Literal["active", "disabled", "draft", "testing", "draining", "fault"]
    sipHost: Optional[str]
    sipPort: Optional[int]
    transport: Optional[Literal["udp", "tcp", "tls"]]
    techPrefix: Optional[str]
    sipAuthUsername: Optional[str]
    sipAuthPasswordSet: bool
    smppPasswordSet: bool
    mediaMode: Literal["proxy", "direct"]
    defaultRatePerUnit: Optional["Money"]
    billingIncrement: Optional[str]
    currency: Optional[str]
    capacity: Optional[int]
    maxCps: Optional[int]
    settlementMode: Literal["ap", "prepaid"]
    balance: "Money"
    smsDeliveryMethod: Optional[Literal["http", "smpp"]]
    reachable: Optional[bool]
    reachCheckedAt: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchSupplierTrunk(_SwitchSupplierTrunkRequired, total=False):
    """A supplier (vendor) trunk. Carries every spec section-4 policy field accepted on create/update; secrets are replaced by *Set booleans."""


class _SwitchSupplierTrunkDetailRequired(TypedDict):
    id: str
    supplierId: Optional[str]
    label: str
    source: str
    status: Literal["active", "disabled", "draft", "testing", "draining", "fault"]
    sipHost: Optional[str]
    sipPort: Optional[int]
    transport: Optional[Literal["udp", "tcp", "tls"]]
    techPrefix: Optional[str]
    sipAuthUsername: Optional[str]
    sipAuthPasswordSet: bool
    smppPasswordSet: bool
    mediaMode: Literal["proxy", "direct"]
    defaultRatePerUnit: Optional["Money"]
    billingIncrement: Optional[str]
    currency: Optional[str]
    capacity: Optional[int]
    maxCps: Optional[int]
    settlementMode: Literal["ap", "prepaid"]
    balance: "Money"
    smsDeliveryMethod: Optional[Literal["http", "smpp"]]
    reachable: Optional[bool]
    reachCheckedAt: Optional[str]
    createdAt: str
    updatedAt: str
    ipAcls: List["SwitchIpAcl"]
    hairpin: Optional[Dict[str, Any]]
    health: Dict[str, Any]


class SwitchSupplierTrunkDetail(_SwitchSupplierTrunkDetailRequired, total=False):
    """A supplier (vendor) trunk. Carries every spec section-4 policy field accepted on create/update; secrets are replaced by *Set booleans."""


class _SwitchTrunkEndpointRequired(TypedDict):
    id: str
    vendorTrunkId: str
    role: Literal["primary", "backup"]
    host: Optional[str]
    port: Optional[int]
    transport: Literal["udp", "tcp", "tls"]
    priority: int
    weightPct: Optional[int]
    enabled: bool
    optionsIntervalSeconds: Optional[int]
    failureThreshold: int
    recoveryThreshold: int
    autoDisable: bool
    reachable: Optional[bool]
    reachLatencyMs: Optional[int]
    reachCheckedAt: Optional[str]
    healthDisabledAt: Optional[str]
    health: Dict[str, Any]
    createdAt: str
    updatedAt: str


class SwitchTrunkEndpoint(_SwitchTrunkEndpointRequired, total=False):
    flap: Optional[Dict[str, Any]]


SwitchSmsEndpointTest = TypedDict("SwitchSmsEndpointTest", {"pass": bool, "via": Literal["http", "smpp"], "checks": List[Dict[str, Any]], "message": str}, total=False)

class _SwitchTrunkRateRequired(TypedDict):
    id: str
    vendorTrunkId: str
    prefix: str
    originPrefix: str
    ratePerUnit: "Money"
    destinationName: Optional[str]
    billingIncrement: Optional[str]
    status: Union[Literal["active", "pending", "superseded", "archived"], str]
    effectiveFrom: Optional[str]


class SwitchTrunkRate(_SwitchTrunkRateRequired, total=False):
    pass


class _SwitchTrunkChangeRequestRequired(TypedDict):
    id: str
    vendorTrunkId: str
    trunkLabel: Optional[str]
    status: Union[Literal["pending", "approved", "rejected", "withdrawn", "applied"], str]
    fields: List[str]
    changes: List[Dict[str, Any]]
    patch: Dict[str, Any]
    beforeValues: Dict[str, Any]
    note: Optional[str]
    requestedBy: str
    requestedByEmail: Optional[str]
    requestedAt: str
    reviewedBy: Optional[str]
    reviewedAt: Optional[str]
    reviewNote: Optional[str]
    appliedAt: Optional[str]


class SwitchTrunkChangeRequest(_SwitchTrunkChangeRequestRequired, total=False):
    pass


class _SwitchTrunkReadinessRequired(TypedDict):
    trunkId: str
    exempt: bool
    exemptReason: Optional[str]
    state: Literal["ready", "not_ready", "exempt"]
    checks: List[Dict[str, Any]]
    failing: int
    warning: int
    grandfathered: bool
    blockingEnabled: bool


class SwitchTrunkReadiness(_SwitchTrunkReadinessRequired, total=False):
    pass


class _SwitchTrunkConfigVersionRequired(TypedDict):
    id: str
    version: int
    source: str
    changedFields: List[str]
    diff: Optional[Dict[str, Any]]
    note: Optional[str]
    checksum: Optional[str]
    changeRequestId: Optional[str]
    actorUserId: Optional[str]
    createdAt: str


class SwitchTrunkConfigVersion(_SwitchTrunkConfigVersionRequired, total=False):
    actorEmail: Optional[str]


class _SwitchIpAclRequired(TypedDict):
    id: str
    entityType: Literal["customer", "trunk"]
    entityId: str
    cidr: str
    description: Optional[str]
    createdAt: str


class SwitchIpAcl(_SwitchIpAclRequired, total=False):
    pass


class _SwitchProviderRequired(TypedDict):
    id: str
    name: str
    accountCode: Optional[str]
    legalName: Optional[str]
    tradingName: Optional[str]
    providerType: Optional[Literal["carrier", "aggregator", "mno", "mvno", "sip_provider"]]
    country: Optional[str]
    services: Optional[List[str]]
    portalEmail: Optional[str]
    currency: str
    status: Literal["draft", "pending_approval", "testing", "active", "suspended", "terminated"]
    statusNote: Optional[str]
    statusChangedAt: Optional[str]
    routable: bool
    contractStart: Optional[str]
    contractEnd: Optional[str]
    autoRenew: bool
    rateNoticeDays: Optional[int]
    disputeDays: Optional[int]
    billingMode: Literal["prepaid", "postpaid"]
    creditLimit: Optional[str]
    balance: "Money"
    paymentTermsDays: Optional[int]
    invoiceCycle: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchProvider(_SwitchProviderRequired, total=False):
    pass


class _SwitchProviderListRequired(TypedDict):
    accounts: List[Dict[str, Any]]
    ungrouped: List[Dict[str, Any]]


class SwitchProviderList(_SwitchProviderListRequired, total=False):
    pass


class _SwitchProviderContactRequired(TypedDict):
    id: str
    supplierId: str
    role: Literal["noc", "rates", "billing", "finance", "fraud", "account", "emergency"]
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    timezone: Optional[str]
    notify: bool
    notes: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchProviderContact(_SwitchProviderContactRequired, total=False):
    pass


class _SwitchProviderDetailRequired(TypedDict):
    id: str
    name: str
    accountCode: Optional[str]
    legalName: Optional[str]
    tradingName: Optional[str]
    providerType: Optional[Literal["carrier", "aggregator", "mno", "mvno", "sip_provider"]]
    country: Optional[str]
    services: Optional[List[str]]
    portalEmail: Optional[str]
    currency: str
    status: Literal["draft", "pending_approval", "testing", "active", "suspended", "terminated"]
    statusNote: Optional[str]
    statusChangedAt: Optional[str]
    routable: bool
    contractStart: Optional[str]
    contractEnd: Optional[str]
    autoRenew: bool
    rateNoticeDays: Optional[int]
    disputeDays: Optional[int]
    billingMode: Literal["prepaid", "postpaid"]
    creditLimit: Optional[str]
    balance: "Money"
    paymentTermsDays: Optional[int]
    invoiceCycle: Optional[str]
    createdAt: str
    updatedAt: str
    contacts: List["SwitchProviderContact"]
    trunks: List[Dict[str, Any]]


class SwitchProviderDetail(_SwitchProviderDetailRequired, total=False):
    pass


class _SwitchProviderDisputeRequired(TypedDict):
    id: str
    supplierId: str
    periodStart: Optional[str]
    periodEnd: Optional[str]
    ourAmount: Optional[str]
    theirAmount: Optional[str]
    currency: str
    status: Literal["open", "submitted", "accepted", "rejected", "settled", "withdrawn"]
    reason: Optional[str]
    resolution: Optional[str]
    invoiceRef: Optional[str]
    openedAt: str
    respondBy: Optional[str]
    closedAt: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchProviderDispute(_SwitchProviderDisputeRequired, total=False):
    daysLeft: Optional[int]
    # Days left to respond (list only); negative = the window has passed


class _SwitchSbcProfileRequired(TypedDict):
    trunkId: str
    trunkLabel: str
    profileLevel: List[Dict[str, Any]]
    xml: str
    applyNote: str


class SwitchSbcProfile(_SwitchSbcProfileRequired, total=False):
    pass


class _SwitchCounterpartyRequired(TypedDict):
    id: str
    name: str
    customerId: Optional[str]
    vendorTrunkId: Optional[str]
    currency: str
    nettingEnabled: bool
    notes: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchCounterparty(_SwitchCounterpartyRequired, total=False):
    customerLabel: Optional[str]
    trunkLabel: Optional[str]


class _SwitchRatingOutcomeRequired(TypedDict):
    kind: Literal["rated", "no_matching_rate", "not_yet_effective", "expired", "forbidden", "rating_failed", "not_billable"]


class SwitchRatingOutcome(_SwitchRatingOutcomeRequired, total=False):
    """A price, or the reason there is none. Only kind = rated carries a rate."""
    rate: float
    # Present when kind = rated. May legitimately be 0.
    matchedPrefix: str
    deckVersion: Optional[int]
    source: str
    destination: str
    effectiveFrom: str
    expiredAt: str
    reason: str
    # Why it is forbidden or failed


class _SwitchRateDeckDiffRequired(TypedDict):
    removalMode: Literal["merge", "replace"]
    changeMode: Literal["amendment", "full_replacement"]
    live: int
    incoming: int
    added: int
    changed: int
    rateChanged: int
    incrementOnly: int
    unchanged: int
    removed: int


class SwitchRateDeckDiff(_SwitchRateDeckDiffRequired, total=False):
    """What a change does to live pricing, with the biggest movers"""


class _SwitchRateDeckRequired(TypedDict):
    id: str
    supplierId: Optional[str]
    name: str
    currency: str
    version: int
    status: Literal["draft", "uploaded", "invalid", "validated", "pending_approval", "scheduled", "active", "expired", "rolled_back"]
    effectiveFrom: Optional[str]
    expiresAt: Optional[str]
    source: Optional[Literal["portal", "csv", "api", "email", "sftp"]]
    sourceRef: Optional[str]
    approvedAt: Optional[str]
    validation: Optional[Dict[str, Any]]
    supersedesId: Optional[str]
    rolledBackAt: Optional[str]
    notes: Optional[str]
    createdAt: str
    updatedAt: str
    rowCount: int
    trunks: List[Dict[str, Any]]
    mutable: bool


class SwitchRateDeck(_SwitchRateDeckRequired, total=False):
    pass


class _SwitchDeckSheetResultRequired(TypedDict):
    targetLabel: str
    currency: str
    warnings: List[Dict[str, Any]]


class SwitchDeckSheetResult(_SwitchDeckSheetResultRequired, total=False):
    rowCount: int
    diff: "SwitchRateDeckDiff"
    # What a change does to live pricing, with the biggest movers
    applied: int
    # Rows written (apply) or queued (scheduled apply)
    replaced: bool
    scheduled: Literal[True]
    # Present when a future effectiveFrom queued the sheet
    effectiveFrom: str
    originScoped: int
    # Origin-scoped live rows a sheet cannot express, counted not changed
    overLimit: bool
    maxRows: int


class _SwitchSellDeckRequired(TypedDict):
    id: str
    name: str
    version: int
    status: Literal["draft", "active", "superseded", "archived"]
    currency: str
    isSystemDefault: bool
    defaultRatePerUnit: Optional[float]
    charging: Dict[str, Any]


class SwitchSellDeck(_SwitchSellDeckRequired, total=False):
    pass


class _SwitchSellDeckRowRequired(TypedDict):
    id: str
    deckId: str
    prefix: str
    originPrefix: str
    ratePerUnit: "Money"
    billingIncrement: Optional[str]
    destinationName: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchSellDeckRow(_SwitchSellDeckRowRequired, total=False):
    pass


class _SwitchSellRateRequired(TypedDict):
    id: str
    prefix: str
    originPrefix: str
    ratePerUnit: "Money"
    billingIncrement: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchSellRate(_SwitchSellRateRequired, total=False):
    pass


class _SwitchEligibleSupplierRequired(TypedDict):
    vendorTrunkId: str
    label: str
    status: str
    via: List[Dict[str, Any]]
    defaultRatePerUnit: Optional["Money"]
    activeRateRows: int
    unpriced: bool
    billingIncrement: str


class SwitchEligibleSupplier(_SwitchEligibleSupplierRequired, total=False):
    pass


class _SwitchCostAnalysisRequired(TypedDict):
    at: str
    input: Dict[str, Any]
    basis: Dict[str, Any]
    sell: Dict[str, Any]
    suppliers: List[Dict[str, Any]]
    selected: Optional[Dict[str, Any]]
    configuredMargin: Dict[str, Any]
    traceId: str
    verdict: Dict[str, Any]
    sideEffects: Dict[str, Any]


class SwitchCostAnalysis(_SwitchCostAnalysisRequired, total=False):
    pass


class _SwitchSessionMarginRequired(TypedDict):
    sessionKey: str
    callUuid: Optional[str]
    at: str
    destination: Optional[str]
    destinationName: Optional[str]
    customerTrunkId: Optional[str]
    status: Optional[str]
    durationSeconds: int
    billedSeconds: Optional[int]
    billingIncrement: Optional[str]
    sellRate: Optional[float]
    charge: float
    bookedCost: float
    attempts: List[Dict[str, Any]]
    attemptCost: float
    margin: float
    flags: List[str]


class SwitchSessionMargin(_SwitchSessionMarginRequired, total=False):
    pass


class _SwitchRouteGroupRequired(TypedDict):
    id: str
    operatorId: str
    name: str
    description: Optional[str]
    enabled: bool
    failoverSipCodes: List[int]
    maxAttempts: int
    selectionMode: Literal["priority", "least_cost", "weighted"]
    failoverTimeoutSeconds: Optional[int]
    createdAt: str
    updatedAt: str


class SwitchRouteGroup(_SwitchRouteGroupRequired, total=False):
    pass


class _SwitchDialplanRequired(TypedDict):
    id: str
    operatorId: str
    name: str
    description: Optional[str]
    enabled: bool
    createdAt: str
    updatedAt: str


class SwitchDialplan(_SwitchDialplanRequired, total=False):
    pass


class _SwitchRouteTraceRequired(TypedDict):
    traceId: str
    at: str
    saved: bool
    savedNote: Optional[str]
    input: Dict[str, Any]
    verdict: Dict[str, Any]
    steps: List[Dict[str, Any]]
    number: Dict[str, Any]
    outCli: Optional[str]
    sell: Optional["SwitchRatingOutcome"]
    sellBillingRate: Optional[float]
    candidates: List[Dict[str, Any]]
    excluded: List[Dict[str, Any]]
    selected: Optional[Dict[str, Any]]
    duration: Optional[Dict[str, Any]]
    sideEffects: Dict[str, Any]


class SwitchRouteTrace(_SwitchRouteTraceRequired, total=False):
    pass


class _SwitchPaymentRequired(TypedDict):
    id: str
    amount: "Money"
    method: Optional[str]
    reference: Optional[str]
    paidAt: str
    createdAt: str


class SwitchPayment(_SwitchPaymentRequired, total=False):
    pass


class _SwitchInvoiceRequired(TypedDict):
    id: str
    customerId: str
    invoiceNumber: str
    periodStart: Optional[str]
    periodEnd: Optional[str]
    issueDate: str
    dueDate: Optional[str]
    currency: str
    subtotal: "Money"
    tax: "Money"
    total: "Money"
    amountPaid: "Money"
    status: Literal["draft", "open", "partial", "paid", "overdue", "void"]
    overdue: bool
    notes: Optional[str]


class SwitchInvoice(_SwitchInvoiceRequired, total=False):
    replacesInvoiceId: Optional[str]
    sentAt: Optional[str]
    # ISO-8601 timestamp (UTC)
    sendCount: int
    customerLabel: Optional[str]
    # On list rows


class _SwitchInvoiceDetailRequired(TypedDict):
    id: str
    customerId: str
    invoiceNumber: str
    periodStart: Optional[str]
    periodEnd: Optional[str]
    issueDate: str
    dueDate: Optional[str]
    currency: str
    subtotal: "Money"
    tax: "Money"
    total: "Money"
    amountPaid: "Money"
    status: Literal["draft", "open", "partial", "paid", "overdue", "void"]
    overdue: bool
    notes: Optional[str]
    lines: List[Dict[str, Any]]
    payments: List["SwitchPayment"]
    customer: Optional[Dict[str, Any]]
    countryBreakdown: Dict[str, Any]
    billingProfile: Optional[Dict[str, Any]]
    identityFrozen: bool
    exclusions: List[Dict[str, Any]]
    replaces: Optional[Dict[str, Any]]
    replacedBy: Optional[Dict[str, Any]]


class SwitchInvoiceDetail(_SwitchInvoiceDetailRequired, total=False):
    replacesInvoiceId: Optional[str]
    sentAt: Optional[str]
    # ISO-8601 timestamp (UTC)
    sendCount: int
    customerLabel: Optional[str]
    # On list rows


class _SwitchInvoicePreviewRequired(TypedDict):
    customer: Dict[str, Any]
    period: Dict[str, Any]
    dueDate: str
    paymentTermsDays: int
    currency: str
    usage: Dict[str, Any]
    broughtForward: Dict[str, Any]
    unrated: Dict[str, Any]
    lines: List[Dict[str, Any]]
    charges: float
    credits: Dict[str, Any]
    tax: Dict[str, Any]
    total: float
    provenance: Dict[str, Any]


class SwitchInvoicePreview(_SwitchInvoicePreviewRequired, total=False):
    reviewToken: str
    # Pass to POST /switch/invoices to issue exactly what was reviewed


class _SwitchCreditNoteRequired(TypedDict):
    id: str
    customerId: str
    creditNoteNumber: str
    invoiceId: Optional[str]
    amount: "Money"
    reason: Optional[str]
    status: str
    createdAt: str


class SwitchCreditNote(_SwitchCreditNoteRequired, total=False):
    customerLabel: Optional[str]


class _SwitchPayableRequired(TypedDict):
    id: str
    vendorTrunkId: str
    payableNumber: str
    periodStart: Optional[str]
    periodEnd: Optional[str]
    issueDate: str
    dueDate: Optional[str]
    currency: str
    subtotal: "Money"
    total: "Money"
    amountPaid: "Money"
    status: Literal["draft", "open", "partial", "paid", "overdue", "void"]
    notes: Optional[str]
    createdAt: str
    updatedAt: str


class SwitchPayable(_SwitchPayableRequired, total=False):
    overdue: bool
    trunkLabel: Optional[str]
    # On list rows


SwitchCdr = TypedDict("SwitchCdr", {"id": str, "createdAt": str, "kind": Literal["voice", "sms"], "direction": str, "from": Optional[str], "to": Optional[str], "cli": Optional[str], "status": str, "sipCode": Optional[int], "hangupCause": Optional[str], "durationSeconds": Optional[int], "billedSeconds": Optional[int], "segments": Optional[int], "pddMs": Optional[int], "callGroupId": Optional[str], "customer": Optional[str], "supplier": Optional[str], "revenue": float, "cost": float, "margin": float, "sellRatePerUnit": Optional[float], "buyRatePerUnit": Optional[float], "ratingState": Optional[str], "mos": Optional[float], "jitterMs": Optional[float], "packetLossPct": Optional[float], "mediaMode": Optional[str], "codec": Optional[str], "q850Cause": Optional[int], "destinationName": Optional[str], "riskScore": Optional[float], "attestation": Optional[str], "customerTrunkId": Optional[str], "attemptCount": int, "invoiceId": Optional[str]}, total=False)

class _SwitchCdrExportRequired(TypedDict):
    id: str
    phase: str
    status: str
    requestedScope: Optional[str]
    requestedAt: str
    recordCount: Optional[int]
    numbersMasked: bool
    addressesMasked: bool


class SwitchCdrExport(_SwitchCdrExportRequired, total=False):
    truncated: bool
    error: Optional[str]
    completedAt: Optional[str]
    # ISO-8601 timestamp (UTC)
    downloadable: bool
    downloadUrl: Optional[str]
    # GET /billing/exports/{id}/download once completed. No server path is ever returned.
    rowCount: Optional[int]
    createdAt: str
    # ISO-8601 timestamp (UTC)
    queryId: Optional[str]


class _SwitchCdrViewRequired(TypedDict):
    id: str
    name: str
    service: Literal["voice", "sms"]
    filters: Dict[str, Any]
    columns: List[str]
    sort: List[Dict[str, Any]]
    isDefault: bool
    createdAt: str
    updatedAt: str


class SwitchCdrView(_SwitchCdrViewRequired, total=False):
    pass


class _SwitchFraudSettingsRequired(TypedDict):
    fraudEnabled: bool
    fraudBlockScore: int
    fraudAlertScore: int
    highRiskPrefixes: List[str]


class SwitchFraudSettings(_SwitchFraudSettingsRequired, total=False):
    pass


class _SwitchIssueRequired(TypedDict):
    key: str
    ref: str
    detector: str
    severity: Literal["critical", "warning", "review"]
    actionable: bool
    status: Literal["open_unacknowledged", "open_acknowledged", "resolved"]
    title: str
    summary: str
    reason: str
    trigger: str
    recovery: str
    objectName: Optional[str]
    subjects: Dict[str, Any]
    evidence: List[Dict[str, Any]]
    firstDetectedAt: str
    lastDetectedAt: str
    detections: int
    acknowledgedAt: Optional[str]
    resolvedAt: Optional[str]
    resolvedVia: Optional[Literal["operator", "recovery", "dismissed"]]
    dismissRule: Optional[str]


class SwitchIssue(_SwitchIssueRequired, total=False):
    pass


class _SwitchTeamMemberRequired(TypedDict):
    id: str
    userId: str
    email: str
    contactName: Optional[str]
    role: str
    roleLabel: str
    status: Union[Literal["active", "suspended"], str]
    customerIds: Optional[List[str]]
    trunkIds: Optional[List[str]]
    note: Optional[str]
    permissions: List[str]
    scopeSummary: Dict[str, Any]
    createdAt: str
    updatedAt: str


class SwitchTeamMember(_SwitchTeamMemberRequired, total=False):
    pass


class _SwitchApprovalRequired(TypedDict):
    id: str
    status: str
    requestedAt: str


class SwitchApproval(_SwitchApprovalRequired, total=False):
    permission: str


class _SwitchDncHonorSettingRequired(TypedDict):
    scope: Literal["customer", "trunk"]
    id: str
    label: str
    value: Optional[bool]
    inherited: Optional[bool]
    customerLabel: Optional[str]
    effective: bool
    decidedBy: Literal["customer", "trunk"]
    mode: Literal["off", "warn", "enforce"]


class SwitchDncHonorSetting(_SwitchDncHonorSettingRequired, total=False):
    trunkOverrides: Dict[str, Any]
    # Customer only: trunks that set their own value instead of inheriting


class _PricingDestinationRequired(TypedDict):
    slug: str
    country: str
    countryCode: str
    routes: int
    lowest: str
    lowestBand: Literal["mobile", "fixed", "countryWide"]
    unit: Literal["min", "msg"]


class PricingDestination(_PricingDestinationRequired, total=False):
    pass


class _PricingDestinationDetailRequired(TypedDict):
    slug: str
    country: str
    countryCode: str
    routes: int
    lowest: str
    lowestBand: Literal["mobile", "fixed", "countryWide"]
    unit: Literal["min", "msg"]
    type: Literal["voice", "sms"]
    highest: str
    bands: List[Dict[str, Any]]
    operators: List[Dict[str, Any]]
    cliTypes: List[Dict[str, Any]]
    increments: List[Dict[str, Any]]
    routesWithStatedAsr: int
    otherBreakouts: int
    topRoutes: List[Dict[str, Any]]
    related: List["PricingDestination"]
    updatedAt: str


class PricingDestinationDetail(_PricingDestinationDetailRequired, total=False):
    pass


class _SystemHealthRequired(TypedDict):
    components: List[Dict[str, Any]]
    updatedAt: str


class SystemHealth(_SystemHealthRequired, total=False):
    pass


class _KycStatusRequired(TypedDict):
    kycStatus: Literal["not_started", "pending", "verified", "rejected"]
    accountType: Optional[Literal["individual", "business"]]
    kycExempt: bool
    depositGate: bool
    configured: bool


class KycStatus(_KycStatusRequired, total=False):
    pass


class _UsComplianceProfileRequired(TypedDict):
    userId: str
    legalBusinessName: str
    contactName: str
    contactEmail: str
    contactPhone: Optional[str]
    frn: str
    filer499Id: str
    ocn: str
    rmdRegistered: bool
    rmdReference: Optional[str]
    signsOwnTraffic: bool
    stirShakenCert: Optional[str]
    attestationLevel: Optional[Literal["A", "B", "C"]]
    termsAcceptedAt: Optional[str]
    submittedAt: str
    updatedAt: str


class UsComplianceProfile(_UsComplianceProfileRequired, total=False):
    pass


class _NotificationRequired(TypedDict):
    id: str
    userId: str
    type: str
    title: str
    message: str
    read: bool
    data: Optional[Dict[str, Any]]
    createdAt: str


class Notification(_NotificationRequired, total=False):
    pass


class _SupportTicketRequired(TypedDict):
    id: str
    userId: Optional[str]
    guestEmail: Optional[str]
    category: str
    subject: str
    status: Literal["open", "in_progress", "resolved", "closed"]
    relatedRouteId: Optional[str]
    relatedPurchaseId: Optional[str]
    assignedTo: Optional[str]
    createdAt: str
    resolvedAt: Optional[str]


class SupportTicket(_SupportTicketRequired, total=False):
    pass


class _SupportTicketMessageRequired(TypedDict):
    id: str
    authorId: Optional[str]
    message: str
    createdAt: str


class SupportTicketMessage(_SupportTicketMessageRequired, total=False):
    authorName: Optional[str]


class _StatusIncidentRequired(TypedDict):
    id: str
    title: str
    impact: Literal["none", "minor", "major", "critical"]
    status: Literal["investigating", "identified", "monitoring", "resolved"]
    componentIds: List[str]
    startedAt: str
    resolvedAt: Optional[str]
    updates: List[Dict[str, Any]]


class StatusIncident(_StatusIncidentRequired, total=False):
    pass


class _StatusPageRequired(TypedDict):
    generatedAt: str
    overall: Dict[str, Any]
    groups: List[Dict[str, Any]]
    activeIncidents: List["StatusIncident"]
    scheduledMaintenance: List[Dict[str, Any]]
    pastIncidents: List["StatusIncident"]


class StatusPage(_StatusPageRequired, total=False):
    pass


class _WhitelistedIpRequired(TypedDict):
    id: str
    userId: str
    ipAddress: str
    label: Optional[str]
    createdAt: str


class WhitelistedIp(_WhitelistedIpRequired, total=False):
    pass


class _InterconnectionRequired(TypedDict):
    id: str
    purchaseId: str
    type: Literal["sip", "smpp", "api"]
    buyerEndpoint: Optional[Dict[str, Any]]
    sellerEndpoint: Optional[Literal["null"]]
    status: Literal["active", "inactive"]
    createdAt: str
    updatedAt: str


class Interconnection(_InterconnectionRequired, total=False):
    pass


class _ConnectionProfileRequired(TypedDict):
    id: str
    contactName: Optional[str]
    companyName: Optional[str]
    country: Optional[str]
    verified: bool


class ConnectionProfile(_ConnectionProfileRequired, total=False):
    jobTitle: Optional[str]
    avatarUrl: Optional[str]
    logoUrl: Optional[str]
    memberSince: str
    # ISO-8601 timestamp (UTC)


class _SubAccountRequired(TypedDict):
    id: str
    label: str
    externalRef: Optional[str]
    balance: "Money"
    status: Literal["draft", "active", "suspended", "closed"]
    markupPct: Optional[str]
    dailySpendCap: Optional[str]
    maxConcurrentCalls: Optional[int]
    creditLimit: str
    currency: str
    portalEmail: Optional[str]
    autoSuspended: bool
    sipUsername: Optional[str]
    createdAt: str
    updatedAt: str


class SubAccount(_SubAccountRequired, total=False):
    pass


class _SubAccountCreatedRequired(TypedDict):
    id: str
    label: str
    externalRef: Optional[str]
    balance: "Money"
    status: Literal["draft", "active", "suspended", "closed"]
    markupPct: Optional[str]
    dailySpendCap: Optional[str]
    maxConcurrentCalls: Optional[int]
    creditLimit: str
    currency: str
    portalEmail: Optional[str]
    autoSuspended: bool
    sipUsername: Optional[str]
    createdAt: str
    updatedAt: str
    apiKey: str
    apiKeyPrefix: str
    sipPassword: str


class SubAccountCreated(_SubAccountCreatedRequired, total=False):
    pass


class _ApplicationSettingsRequired(TypedDict):
    operatorId: str
    defaultMarkupPct: str
    defaultBillingIncrement: str
    minMarginPct: str
    subLowBalanceThreshold: str
    defaultDailySpendCap: Optional[str]
    defaultMaxConcurrentCalls: Optional[int]
    brandName: Optional[str]
    brandColor: Optional[str]
    brandLogoUrl: Optional[str]
    requireTrunkApproval: bool
    requireTrunkReadiness: bool


class ApplicationSettings(_ApplicationSettingsRequired, total=False):
    pass


class _RevshareNumberRequired(TypedDict):
    id: str
    number: str
    country: Optional[str]
    countryCode: Optional[str]
    carrier: Optional[str]
    rangeLabel: Optional[str]
    groupKey: str
    status: Literal["available", "taken", "retired"]
    ratePerMin: "Money"
    createdAt: str


class RevshareNumber(_RevshareNumberRequired, total=False):
    pass


class _RevshareTakingRequired(TypedDict):
    id: str
    numberId: str
    userId: str
    paymentTerm: Literal["1_1", "7_1", "15_15"]
    effectiveRate: "Money"
    ivrConfigId: Optional[str]
    ivrMode: Literal["single", "split", "geo"]
    status: Literal["active", "released"]
    callsCount: int
    minutesTotal: str
    earningsTotal: "Money"
    lastCallAt: Optional[str]
    takenAt: str
    releasedAt: Optional[str]


class RevshareTaking(_RevshareTakingRequired, total=False):
    pass


class _RevsharePayoutRequired(TypedDict):
    id: str
    amount: "Money"
    cryptoAsset: Optional[str]
    network: Optional[str]
    address: Optional[str]
    term: Literal["1_1", "7_1", "15_15"]
    status: Literal["requested", "approved", "paid", "rejected"]
    txRef: Optional[str]
    createdAt: str
    paidAt: Optional[str]


class RevsharePayout(_RevsharePayoutRequired, total=False):
    pass


class _RevshareIvrConfigRequired(TypedDict):
    id: str
    userId: str
    takingId: Optional[str]
    kind: Literal["default_music", "upload", "tts"]
    name: Optional[str]
    assetPath: Optional[str]
    assetMime: Optional[str]
    ttsText: Optional[str]
    ttsVoiceId: Optional[str]
    status: Literal["draft", "active"]
    createdAt: str


class RevshareIvrConfig(_RevshareIvrConfigRequired, total=False):
    pass


class _RevshareIvrSetRequired(TypedDict):
    mode: Literal["single", "split", "geo"]
    variants: List[Dict[str, Any]]


class RevshareIvrSet(_RevshareIvrSetRequired, total=False):
    pass


__all__ = ["Money", "Message", "Deleted", "ValidationIssue", "Error", "ErrorEnvelope", "AccountProfile", "AccountBalance", "AccountActivityEvent", "AccountClosurePreview", "AccountSwitchEntitlement", "AccountSpendAlerts", "AccountSavedSearch", "AccountFavoriteRoute", "AccountDedicatedIp", "AccountActivatedIp", "AccountInterconnect", "AccountConnectivityBrief", "AuthTokens", "AuthSession", "AuthMfaChallenge", "AuthDeviceSession", "ApiKey", "CreatedApiKey", "Webhook", "WebhookWithSecret", "WebhookDelivery", "ApiUsage", "MarketplaceSellerProfile", "MarketplaceRoute", "OwnRoute", "MarketplaceStats", "ConnectivityTestResult", "ResolvedRoute", "PricedRoute", "RouteRate", "RateSheetImport", "ListingHealth", "BulkEndpointResult", "PriceNumberResult", "RouteAccessGrant", "RouteReport", "RouteReportThread", "Purchase", "PurchaseDetail", "PurchaseRow", "RoutingOrderEntry", "RouteForCandidate", "RoutingOrderResult", "RouteForResult", "PurchaseUpcomingRateChanges", "Offer", "CallAction", "CommsCallAccepted", "CommsCallStatus", "CommsCall", "CommsSms", "CommsHistoryEntry", "SmsTimelineStep", "CommsSmsStatus", "CommsBulkSmsResult", "VoiceOtpResult", "VoiceOtpStatus", "VerifyStartResult", "VerifyCheckResult", "Verification", "DidCatalogSku", "DidCatalogGroup", "DidCatalogCountry", "DidCatalogType", "Did", "DidBulkBuyResult", "DidCallFlow", "DidSipLineLogin", "DidSipLine", "DidCalls", "DidFeatures", "DidGreeting", "DidRecording", "DidMessage", "DidSmsSettings", "DidConversation", "DidAnalytics", "DidNumbersOverview", "DidListingRequestView", "DidCliEligible", "DidAiAgent", "NumberLookup", "LedgerTransaction", "BillingCdr", "BillingExportJob", "BillingDocument", "TaxInvoiceSummary", "TaxInvoice", "Topup", "Payout", "AutoRecharge", "DialerCampaign", "DialerCampaignStats", "DialerNumber", "DialerNumbersUploadResult", "DialerCampaignCli", "DialerContactMapping", "DialerCallerIdSet", "DialerCallerIdNumber", "DialerCallerIdAddResult", "DialerRevshareCaller", "DialerContactList", "DialerCompatibleTargets", "DialerSmsTemplate", "DialerCliSet", "DialerContactParseResult", "CliTest", "RouteTestItem", "RouteTestBatch", "RouteTestPreview", "DncEntry", "AiAgent", "AiVoice", "AiAgentDraft", "AiAgentTurn", "SwitchCustomer", "SwitchCustomerListRow", "SwitchCustomerCreated", "SwitchCustomerSipCredentials", "SwitchCustomerLifecycleEntry", "SwitchCustomerLifecycle", "SwitchCustomerOverview", "SwitchCustomerQuality", "SwitchCustomerContact", "SwitchCustomerNote", "SwitchCustomerAttentionItem", "SwitchCustomerIssue", "SwitchCustomerBillingSummary", "SwitchCustomerCreditPosition", "SwitchCustomerPayment", "SwitchCustomerInvoicePreview", "SwitchCustomerIssuedInvoice", "SwitchCustomerBillingProfile", "SwitchCustomerSellDeckRef", "SwitchTrunkEffectiveSellDeck", "SwitchCustomerSellRate", "SwitchCustomerSellRatePage", "SwitchCustomerTrunk", "SwitchCustomerTrunkListRow", "SwitchTrunkAddressPanel", "SwitchCustomerRoutingAssignment", "SwitchTrunkCredentialStatus", "SwitchTrunkEffectiveConfig", "SwitchCustomerRateNotice", "SwitchCustomerRateChange", "SwitchSupplierTrunk", "SwitchSupplierTrunkDetail", "SwitchTrunkEndpoint", "SwitchSmsEndpointTest", "SwitchTrunkRate", "SwitchTrunkChangeRequest", "SwitchTrunkReadiness", "SwitchTrunkConfigVersion", "SwitchIpAcl", "SwitchProvider", "SwitchProviderList", "SwitchProviderContact", "SwitchProviderDetail", "SwitchProviderDispute", "SwitchSbcProfile", "SwitchCounterparty", "SwitchRatingOutcome", "SwitchRateDeckDiff", "SwitchRateDeck", "SwitchDeckSheetResult", "SwitchSellDeck", "SwitchSellDeckRow", "SwitchSellRate", "SwitchEligibleSupplier", "SwitchCostAnalysis", "SwitchSessionMargin", "SwitchRouteGroup", "SwitchDialplan", "SwitchRouteTrace", "SwitchPayment", "SwitchInvoice", "SwitchInvoiceDetail", "SwitchInvoicePreview", "SwitchCreditNote", "SwitchPayable", "SwitchCdr", "SwitchCdrExport", "SwitchCdrView", "SwitchFraudSettings", "SwitchIssue", "SwitchTeamMember", "SwitchApproval", "SwitchDncHonorSetting", "PricingDestination", "PricingDestinationDetail", "SystemHealth", "KycStatus", "UsComplianceProfile", "Notification", "SupportTicket", "SupportTicketMessage", "StatusIncident", "StatusPage", "WhitelistedIp", "Interconnection", "ConnectionProfile", "SubAccount", "SubAccountCreated", "ApplicationSettings", "RevshareNumber", "RevshareTaking", "RevsharePayout", "RevshareIvrConfig", "RevshareIvrSet"]
