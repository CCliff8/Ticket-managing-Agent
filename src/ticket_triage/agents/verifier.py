import json
import logging
import re

from anthropic import Anthropic

from src.ticket_triage.config import settings
from src.ticket_triage.graph.state import TicketState
from src.ticket_triage.models import VerificationResult

logger = logging.getLogger(__name__)

_PROMPT = """\
You are a QA agent. Evaluate whether the proposed solution is:
1. Grounded in the runbook excerpts (no hallucinated steps not present in the runbooks)
2. Safe and appropriate to send directly to a user

Runbook excerpts:
{runbook_context}

Proposed solution:
{proposed_solution}

Return ONLY a JSON object with exactly these fields:
- "verdict": true if grounded and safe, false otherwise
- "confidence": float between 0.0 and 1.0 (certainty the solution is correct and safe)
- "reasoning": brief explanation, max 80 words

No prose, no markdown — only valid JSON."""


def _fallback() -> VerificationResult:
    return VerificationResult(
        verdict=False,
        confidence=0.0,
        reasoning="Verification failed — defaulting to escalation for safety.",
    )


def verify_solution(state: TicketState) -> dict:
    if not state["proposed_solution"] or not state["retrieved_chunks"]:
        logger.warning("Ticket %s — nothing to verify, escalating", state["ticket_id"])
        return {"verification": _fallback()}

    runbook_context = "\n\n---\n\n".join(
        f"[{c.source}]\n{c.content}" for c in state["retrieved_chunks"]
    )

    try:
        client = Anthropic(api_key=settings.anthropic_api_key, timeout=60.0)
        response = client.messages.create(
            model=settings.resolver_model_low,
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": _PROMPT.format(
                        runbook_context=runbook_context,
                        proposed_solution=state["proposed_solution"],
                    ),
                }
            ],
        )
        match = re.search(r"\{.*\}", response.content[0].text, re.DOTALL)
        if not match:
            raise ValueError("No JSON in verifier response")
        verification = VerificationResult(**json.loads(match.group()))
    except Exception as exc:
        logger.warning("Verifier error: %s — using fallback", exc)
        verification = _fallback()

    logger.info(
        "Ticket %s — verdict=%s confidence=%.2f",
        state["ticket_id"],
        verification.verdict,
        verification.confidence,
    )
    return {"verification": verification}
