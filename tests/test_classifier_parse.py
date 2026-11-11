import pytest

from src.ticket_triage.agents.classifier import _fallback, _parse
from src.ticket_triage.models import Category, RiskTier


def test_parse_valid_json_embedded_in_prose():
    raw = 'Sure! {"category":"vpn","urgency":"low","risk_tier":"low","reasoning":"routine"}'
    result = _parse(raw)
    assert result.category == Category.VPN
    assert result.risk_tier == RiskTier.LOW


def test_parse_rejects_non_json():
    with pytest.raises(ValueError):
        _parse("no json here")


def test_fallback_is_high_risk():
    assert _fallback().risk_tier == RiskTier.HIGH
