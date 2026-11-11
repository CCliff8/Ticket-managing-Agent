from enum import Enum

from pydantic_settings import BaseSettings


class ClassifierBackend(str, Enum):
    OLLAMA = "ollama"
    GROQ = "groq"


class Settings(BaseSettings):
    # Classifier
    classifier_backend: ClassifierBackend = ClassifierBackend.OLLAMA
    classifier_model: str = "llama3.2:3b"
    ollama_base_url: str = "http://localhost:11434"
    groq_api_key: str = ""

    # Resolver
    anthropic_api_key: str = ""
    resolver_model_low: str = "claude-haiku-4-5-20251001"
    resolver_model_high: str = "claude-sonnet-4-6"

    # Email
    email_address: str = ""
    email_app_password: str = ""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    human_review_email: str = ""

    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"
    runbooks_dir: str = "./runbooks"

    # Routing thresholds
    auto_resolve_confidence: float = 0.8
    draft_review_confidence: float = 0.5

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
