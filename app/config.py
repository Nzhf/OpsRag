"""Application configuration using pydantic-settings."""
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Qdrant Cloud
    qdrant_url: str = Field(..., description="Qdrant Cloud cluster URL")
    qdrant_api_key: str = Field(..., description="Qdrant API key")

    # Google Gemini
    gemini_api_key: str = Field(..., description="Google Gemini API key for embeddings")

    # Groq
    groq_api_key: str = Field(..., description="Groq API key for generation and tool-calling")
    groq_model: str = Field(
        default="llama-3.3-70b-versatile",
        description="Groq model name (check console.groq.com/docs/tool-use at build time)"
    )

    # Application
    collection_name: str = Field(default="opsrag_docs", description="Qdrant collection name")
    embedding_model: str = Field(default="text-embedding-004", description="Gemini embedding model")
    embedding_dimension: int = Field(default=768, description="Embedding vector dimension")
    temperature: float = Field(default=0.1, description="LLM temperature")
    max_tokens: int = Field(default=4096, description="Max tokens for LLM response")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
