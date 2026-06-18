from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Settings:
    app_name: str = "AdaptiveTutorAI v3"
    api_version: str = "v3"
    environment: str = os.getenv("ENVIRONMENT", "development")
    secret_key: str = os.getenv("SECRET_KEY", "change-me-in-production")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./adaptive_tutor_v3.db")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    qdrant_url: str = os.getenv("QDRANT_URL", "http://qdrant:6333")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "adaptive_tutor_v3")
    data_dir: Path = Path(os.getenv("DATA_DIR", "data"))
    docs_dir: Path = Path(os.getenv("DOCS_DIR", "docs"))
    llm_provider: str = os.getenv("LLM_PROVIDER", "local")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    token_ttl_minutes: int = int(os.getenv("TOKEN_TTL_MINUTES", "480"))
    use_auto_migrations: bool = os.getenv("AUTO_MIGRATIONS", "1") == "1"
    seed_on_startup: bool = os.getenv("SEED_ON_STARTUP", "1") == "1"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_retrieval_results: int = int(os.getenv("MAX_RETRIEVAL_RESULTS", "8"))


settings = Settings()
