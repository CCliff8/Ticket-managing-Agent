import logging

from langgraph.graph import END, StateGraph

from src.ticket_triage.agents.classifier import classify_ticket
from src.ticket_triage.agents.resolver import resolve_ticket
from src.ticket_triage.agents.retriever import retrieve_runbooks
from src.ticket_triage.agents.verifier import verify_solution
from src.ticket_triage.config import settings
from src.ticket_triage.email_client import send_email
from src.ticket_triage.graph.state import TicketState
from src.ticket_triage.models import RoutingDecision
from src.ticket_triage.routing import decide_route

logger = logging.getLogger(__name__)


def _route(state: TicketState) -> str:
    return decide_route(
        state["verification"],
        state["classification"].risk_tier,
        settings.auto_resolve_confidence,
        settings.draft_review_confidence,
    ).value


def _deliver(state: TicketState, to: str, subject: str, body: str, decision: RoutingDecision) -> dict:
    """Send an email; on failure keep the decision but record the error."""
    try:
        send_email(to=to, subject=subject, body=body)
    except Exception as exc:
        logger.error("Ticket %s — email delivery failed: %s", state["ticket_id"], exc)
        return {"routing_decision": decision, "error": f"email delivery failed: {exc}"}
    return {"routing_decision": decision}


def _auto_reply(state: TicketState) -> dict:
    body = (
        f"Dear User,\n\n"
        f"Your support ticket (ID: {state['ticket_id']}) has been resolved:\n\n"
        f"{state['proposed_solution']}\n\n"
        f"If this did not resolve your issue, please reply to this email.\n\n"
        f"Best regards,\nSupport Team"
    )
    # Reply to the requester when known; otherwise fall back to the reviewer inbox.
    to = state.get("requester_email") or settings.human_review_email
    logger.info("Auto-resolving ticket %s", state["ticket_id"])
    return _deliver(
        state, to, f"[RESOLVED] Ticket {state['ticket_id']}", body, RoutingDecision.AUTO_RESOLVE
    )


def _draft_review(state: TicketState) -> dict:
    c = state["classification"]
    v = state["verification"]
    body = (
        f"DRAFT FOR YOUR REVIEW\n"
        f"{'─'*50}\n"
        f"Ticket ID  : {state['ticket_id']}\n"
        f"Category   : {c.category.value}  |  Urgency: {c.urgency.value}  |  Risk: {c.risk_tier.value}\n"
        f"Confidence : {v.confidence:.0%}\n"
        f"Requester  : {state.get('requester_email') or 'unknown'}\n\n"
        f"--- Proposed solution ---\n"
        f"{state['proposed_solution']}\n\n"
        f"--- Original ticket ---\n"
        f"{state['ticket_text']}"
    )
    logger.info("Sending draft for review — ticket %s", state["ticket_id"])
    return _deliver(
        state,
        settings.human_review_email,
        f"[REVIEW] Ticket {state['ticket_id']}",
        body,
        RoutingDecision.DRAFT_REVIEW,
    )


def _escalate(state: TicketState) -> dict:
    c = state["classification"]
    v = state["verification"]
    confidence_str = f"{v.confidence:.0%}" if v else "N/A"
    reasoning = v.reasoning if v else "N/A"
    body = (
        f"ESCALATION REQUIRED — Human action needed\n"
        f"{'─'*50}\n"
        f"Ticket ID  : {state['ticket_id']}\n"
        f"Category   : {c.category.value}\n"
        f"Risk tier  : {c.risk_tier.value}  |  Urgency: {c.urgency.value}\n"
        f"Confidence : {confidence_str}\n"
        f"Verifier   : {reasoning}\n"
        f"Requester  : {state.get('requester_email') or 'unknown'}\n\n"
        f"--- Original ticket ---\n"
        f"{state['ticket_text']}"
    )
    logger.info("Escalating ticket %s", state["ticket_id"])
    return _deliver(
        state,
        settings.human_review_email,
        f"[ESCALATION] Ticket {state['ticket_id']}",
        body,
        RoutingDecision.ESCALATE,
    )


def build_graph():
    g = StateGraph(TicketState)

    g.add_node("classify", classify_ticket)
    g.add_node("retrieve", retrieve_runbooks)
    g.add_node("resolve", resolve_ticket)
    g.add_node("verify", verify_solution)
    g.add_node("auto_reply", _auto_reply)
    g.add_node("draft_review", _draft_review)
    g.add_node("escalate", _escalate)

    g.set_entry_point("classify")
    g.add_edge("classify", "retrieve")
    g.add_edge("retrieve", "resolve")
    g.add_edge("resolve", "verify")
    g.add_conditional_edges(
        "verify",
        _route,
        {
            RoutingDecision.AUTO_RESOLVE.value: "auto_reply",
            RoutingDecision.DRAFT_REVIEW.value: "draft_review",
            RoutingDecision.ESCALATE.value: "escalate",
        },
    )
    g.add_edge("auto_reply", END)
    g.add_edge("draft_review", END)
    g.add_edge("escalate", END)

    return g.compile()
