import argparse

from dotenv import load_dotenv

load_dotenv()

from src.ticket_triage.knowledge_base import add_resolution


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Save a human resolution to the knowledge base (feedback loop)"
    )
    parser.add_argument("--ticket-id", required=True, help="ID of the resolved ticket")
    parser.add_argument(
        "--resolution", required=True, help="Text description of how the ticket was resolved"
    )
    args = parser.parse_args()
    add_resolution(args.ticket_id, args.resolution)


if __name__ == "__main__":
    main()
