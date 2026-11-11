import argparse
import logging
import sys
import uuid
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from src.ticket_triage.graph.pipeline import build_graph

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(name)s — %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit a support ticket for automated triage")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticket", type=Path, metavar="FILE", help="Path to a .txt ticket file")
    group.add_argument("--text", type=str, metavar="TEXT", help="Ticket text as a quoted string")
    parser.add_argument(
        "--requester-email",
        metavar="EMAIL",
        help="Requester address; auto-resolved replies are sent here (default: reviewer inbox)",
    )
    args = parser.parse_args()

    ticket_text = (
        args.ticket.read_text("utf-8").strip() if args.ticket else args.text.strip()
    )
    if not ticket_text:
        parser.error("Ticket text is empty.")

    ticket_id = uuid.uuid4().hex[:8]
    logger.info("Processing ticket %s", ticket_id)

    graph = build_graph()
    result = graph.invoke(
        {
            "ticket_id": ticket_id,
            "ticket_text": ticket_text,
            "requester_email": args.requester_email,
            "classification": None,
            "retrieved_chunks": [],
            "proposed_solution": None,
            "verification": None,
            "routing_decision": None,
            "error": None,
        }
    )

    c = result["classification"]
    v = result["verification"]
    print(f"\n{'─'*50}")
    print(f"Ticket ID  : {ticket_id}")
    print(f"Category   : {c.category.value}")
    print(f"Risk tier  : {c.risk_tier.value}  |  Urgency: {c.urgency.value}")
    print(f"Confidence : {v.confidence:.0%}")
    print(f"Decision   : {result['routing_decision'].value}")
    if result.get("error"):
        print(f"Warning    : {result['error']}")
    print(f"{'─'*50}\n")
    if result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
