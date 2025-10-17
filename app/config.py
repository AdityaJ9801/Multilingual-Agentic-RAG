"""Configuration management for the RAG system."""
import os
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Multilingual Agentic RAG"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    log_level: str = "INFO"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_reload: bool = True

    # Security
    secret_key: str = "your-secret-key-change-in-production"
    api_key: str = "your-api-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60

    # Ollama
    ollama_base_url: str = "http://ollama:11434"
    ollama_model: str = "mistral"
    ollama_temperature: float = 0.7
    ollama_top_p: float = 0.9
    ollama_max_tokens: int = 2048
    ollama_timeout: int = 120
    ollama_retry_attempts: int = 3
    ollama_retry_delay: int = 2

    # Qdrant
    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_api_key: str = ""
    qdrant_timeout: int = 30
    qdrant_collection_name: str = "documents"
    qdrant_vector_size: int = 1024
    qdrant_distance_metric: str = "Cosine"

    # Embeddings
    embedding_model: str = "intfloat/multilingual-e5-large"
    embedding_batch_size: int = 32
    embedding_device: str = "cpu"

    # Languages
    supported_languages: List[str] = ["en", "es", "fr", "zh", "ar"]
    default_language: str = "en"
    language_detection_confidence_threshold: float = 0.5

    # Document Processing
    max_file_size_mb: int = 50
    chunk_size: int = 512
    chunk_overlap: int = 51
    supported_file_types: List[str] = ["pdf", "txt", "md", "json", "csv"]

    # Agents
    agent_timeout: int = 30
    agent_max_retries: int = 3
    enable_agent_logging: bool = True

    # Features
    enable_validation_agent: bool = True
    enable_fact_checking: bool = True
    enable_citation_verification: bool = True
    enable_caching: bool = True
    cache_ttl_seconds: int = 3600

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


def validate_settings() -> None:
    """Validate settings on startup."""
    settings = get_settings()

    # Validate language configuration
    if settings.default_language not in settings.supported_languages:
        raise ValueError(
            f"DEFAULT_LANGUAGE '{settings.default_language}' not in SUPPORTED_LANGUAGES"
        )

    # Validate file size
    if settings.max_file_size_mb <= 0:
        raise ValueError("MAX_FILE_SIZE_MB must be positive")

    # Validate chunk configuration
    if settings.chunk_size <= 0:
        raise ValueError("CHUNK_SIZE must be positive")

    if settings.chunk_overlap >= settings.chunk_size:
        raise ValueError("CHUNK_OVERLAP must be less than CHUNK_SIZE")

