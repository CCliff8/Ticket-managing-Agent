import pytest

from src.ticket_triage.models import RiskTier, RoutingDecision, VerificationResult
from src.ticket_triage.routing import decide_route

AUTO, DRAFT = 0.8, 0.5


def _v(verdict: bool, confidence: float) -> VerificationResult:
    return VerificationResult(verdict=verdict, confidence=confidence, reasoning="test")


@pytest.mark.parametrize(
    "risk, verdict, confidence, expected",
    [
        (RiskTier.LOW, True, 0.95, RoutingDecision.AUTO_RESOLVE),
        (RiskTier.LOW, True, 0.80, RoutingDecision.AUTO_RESOLVE),
        (RiskTier.LOW, True, 0.65, RoutingDecision.DRAFT_REVIEW),
        (RiskTier.LOW, True, 0.30, RoutingDecision.ESCALATE),
        (RiskTier.MEDIUM, True, 0.99, RoutingDecision.DRAFT_REVIEW),
        (RiskTier.MEDIUM, True, 0.40, RoutingDecision.ESCALATE),
        (RiskTier.HIGH, True, 0.99, RoutingDecision.ESCALATE),
        (RiskTier.LOW, False, 0.99, RoutingDecision.ESCALATE),
        (RiskTier.MEDIUM, False, 0.99, RoutingDecision.ESCALATE),
    ],
)
def test_decide_route(risk, verdict, confidence, expected):
    assert decide_route(_v(verdict, confidence), risk, AUTO, DRAFT) == expected
