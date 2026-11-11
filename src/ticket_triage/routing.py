from src.ticket_triage.models import RiskTier, RoutingDecision, VerificationResult


def decide_route(
    verification: VerificationResult,
    risk: RiskTier,
    auto_resolve_confidence: float,
    draft_review_confidence: float,
) -> RoutingDecision:
    """Pure routing policy: high risk or a failed verdict always escalates."""
    if risk == RiskTier.HIGH or not verification.verdict:
        return RoutingDecision.ESCALATE

    if risk == RiskTier.LOW and verification.confidence >= auto_resolve_confidence:
        return RoutingDecision.AUTO_RESOLVE

    if verification.confidence >= draft_review_confidence:
        return RoutingDecision.DRAFT_REVIEW

    return RoutingDecision.ESCALATE
