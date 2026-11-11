import logging

from src.ticket_triage.graph.state import TicketState
from src.ticket_triage.knowledge_base import get_collection
from src.ticket_triage.models import RunbookChunk
from src.ticket_triage.sanitize import sanitize_ticket

logger = logging.getLogger(__name__)

_TOP_K = 3


def retrieve_runbooks(state: TicketState) -> dict:
    collection = get_collection()
    if collection.count() == 0:
        logger.warning("Knowledge base is empty — run setup_kb.py first")
        return {"retrieved_chunks": []}

    query = f"{sanitize_ticket(state['ticket_text'])} {state['classification'].category.value}"
    results = collection.query(query_texts=[query], n_results=_TOP_K)

    chunks = [
        RunbookChunk(
            source=results["metadatas"][0][i]["source"],
            content=doc,
            relevance_score=max(0.0, 1.0 - results["distances"][0][i]),
        )
        for i, doc in enumerate(results["documents"][0])
    ]

    logger.info(
        "Ticket %s — retrieved %d chunks: %s",
        state["ticket_id"],
        len(chunks),
        [c.source for c in chunks],
    )
    return {"retrieved_chunks": chunks}
