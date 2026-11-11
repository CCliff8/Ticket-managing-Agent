from enum import Enum

from pydantic import BaseModel, Field


class RiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Urgency(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Category(str, Enum):
    VPN = "vpn"
    PASSWORD = "password"
    SOFTWARE = "software"
    BILLING = "billing"
    SECURITY = "security"
    EMAIL = "email"
    HARDWARE = "hardware"
    DATA_LOSS = "data_loss"
    OTHER = "other"


class ClassificationResult(BaseModel):
    category: Category
    urgency: Urgency
    risk_tier: RiskTier
    reasoning: str = Field(max_length=500)


class RunbookChunk(BaseModel):
    source: str
    content: str
    relevance_score: float


class VerificationResult(BaseModel):
    verdict: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(max_length=500)


class RoutingDecision(str, Enum):
    AUTO_RESOLVE = "auto_resolve"
    DRAFT_REVIEW = "draft_review"
    ESCALATE = "escalate"
