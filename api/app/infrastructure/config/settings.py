"""Application settings loaded from environment variables."""

import os
from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    """Store application configuration values.

    The settings object centralizes all environment-driven configuration used
    by infrastructure adapters and application wiring.
    """

    google_cloud_project: str = os.environ["GOOGLE_CLOUD_PROJECT"]
    google_cloud_location: str = os.environ.get("GOOGLE_CLOUD_LOCATION")
    db_host: str = os.environ.get("DB_HOST")
    db_port: int = int(os.environ.get("DB_PORT"))
    db_name: str = os.environ.get("DB_NAME")
    db_user: str = os.environ.get("DB_USER")
    db_password: str = os.environ.get("DB_PASSWORD")
    embedding_model_name: str = os.environ.get("EMBEDDING_MODEL_NAME")
    generation_model_name: str = os.environ.get("GENERATION_MODEL_NAME")
    embedding_dimensions: int = int(os.environ.get("EMBEDDING_DIMENSIONS"))
    hnsw_ef_search: int = int(os.environ.get("HNSW_EF_SEARCH"))
    debug_llm: bool = os.environ.get("DEBUG_LLM", "false").lower() == "true"
