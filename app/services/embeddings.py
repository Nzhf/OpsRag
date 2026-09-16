"""Embedding service using Google Gemini API.

Uses the Gemini embedContent REST endpoint directly via httpx to avoid
an extra SDK dependency.  The response vector dimension is confirmed
from the actual API response rather than assumed.
"""
import httpx
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating embeddings using Google Gemini."""

    def __init__(self):
        self.api_key = settings.gemini_api_key
        self.model = settings.embedding_model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    async def embed_text(self, text: str) -> list[float]:
        """Generate embedding for a single text."""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/models/{self.model}:embedContent",
                params={"key": self.api_key},
                json={
                    "model": f"models/{self.model}",
                    "content": {"parts": [{"text": text}]},
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["embedding"]["values"]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for multiple texts in parallel.

        Uses asyncio.gather so multiple API calls run concurrently,
        which is much faster than sequential calls during ingestion.
        """
        import asyncio

        tasks = [self.embed_text(t) for t in texts]
        return await asyncio.gather(*tasks, return_exceptions=True)

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Rough token count estimate (1 token ≈ 4 characters)."""
        return len(text) // 4

