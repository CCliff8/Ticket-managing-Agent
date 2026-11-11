import logging
from pathlib import Path

import chromadb

from src.ticket_triage.config import settings

logger = logging.getLogger(__name__)

_COLLECTION = "runbooks"
_CHUNK_SIZE = 400
_OVERLAP = 50


def _chunk(text: str) -> list[str]:
    words = text.split()
    chunks, step = [], _CHUNK_SIZE - _OVERLAP
    for i in range(0, len(words), step):
        chunk = " ".join(words[i : i + _CHUNK_SIZE])
        if chunk:
            chunks.append(chunk)
    return chunks or [text]


def _client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=settings.chroma_persist_dir)


def get_collection() -> chromadb.Collection:
    return _client().get_or_create_collection(_COLLECTION)


def load_runbooks() -> None:
    client = _client()
    try:
        client.delete_collection(_COLLECTION)
    except ValueError:  # collection does not exist yet
        pass
    collection = client.create_collection(_COLLECTION)

    runbooks = sorted(Path(settings.runbooks_dir).glob("*.md"))
    docs, metas, ids = [], [], []
    for path in runbooks:
        for j, chunk in enumerate(_chunk(path.read_text("utf-8"))):
            docs.append(chunk)
            metas.append({"source": path.name})
            ids.append(f"{path.stem}_{j}")

    if docs:
        collection.add(documents=docs, metadatas=metas, ids=ids)

    logger.info("Loaded %d chunks from %d runbooks.", len(docs), len(runbooks))
    print(f"Loaded {len(docs)} chunks from {len(runbooks)} runbooks.")


def add_resolution(ticket_id: str, resolution: str) -> None:
    collection = get_collection()
    collection.upsert(
        documents=[resolution],
        metadatas=[{"source": f"human_resolution_{ticket_id}"}],
        ids=[f"resolution_{ticket_id}"],
    )
    print(f"Resolution for ticket {ticket_id} saved to knowledge base.")
