from typing import Optional

from typing_extensions import TypedDict

from src.ticket_triage.models import (
    ClassificationResult,
    RoutingDecision,
    RunbookChunk,
    VerificationResult,
)


class TicketState(TypedDict):
    ticket_id: str
    ticket_text: str
    requester_email: Optional[str]
    classification: Optional[ClassificationResult]
    retrieved_chunks: list[RunbookChunk]
    proposed_solution: Optional[str]
    verification: Optional[VerificationResult]
    routing_decision: Optional[RoutingDecision]
    error: Optional[str]
