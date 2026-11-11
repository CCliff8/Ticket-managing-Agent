from dotenv import load_dotenv

load_dotenv()

from src.ticket_triage.knowledge_base import load_runbooks

if __name__ == "__main__":
    load_runbooks()
