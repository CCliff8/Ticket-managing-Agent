import logging

from anthropic import Anthropic

from src.ticket_triage.config import settings
from src.ticket_triage.graph.state import TicketState
from src.ticket_triage.models import RiskTier
from src.ticket_triage.sanitize import sanitize_ticket

logger = logging.getLogger(__name__)

_PROMPT = """\
You are a helpful IT support specialist. Using the runbook excerpts below, propose a \
clear step-by-step solution to the support ticket. Always cite which runbook section \
you are drawing from. If the runbooks do not cover the issue, say so explicitly — \
do not invent steps that are not in the runbooks.

Runbook excerpts:
{runbook_context}

Support ticket:
<ticket>
{ticket_text}
</ticket>"""


def resolve_ticket(state: TicketState) -> dict:
    model = (
        settings.resolver_model_high
        if state["classification"].risk_tier == RiskTier.HIGH
        else settings.resolver_model_low
    )
    logger.info("Ticket %s — resolving with model %s", state["ticket_id"], model)

    runbook_context = "\n\n---\n\n".join(
        f"[{chunk.source}]\n{chunk.content}" for chunk in state["retrieved_chunks"]
    )

    if not runbook_context:
        runbook_context = "(no runbook excerpts were found)"

    try:
        client = Anthropic(api_key=settings.anthropic_api_key, timeout=60.0)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": _PROMPT.format(
                        runbook_context=runbook_context,
                        ticket_text=sanitize_ticket(state["ticket_text"]),
                    ),
                }
            ],
        )
        return {"proposed_solution": response.content[0].text}
    except Exception as exc:
        logger.error("Resolver error: %s — ticket will be escalated", exc)
        return {"proposed_solution": None, "error": f"resolver failed: {exc}"}
