"""Retrieval service: embeds a query, searches Qdrant, and builds
a context block for downstream generation.

This module wraps the lower-level Qdrant client operations in
app/core/qdrant_client.py and adds RAG-specific logic such as
score-threshold filtering and token-budgeted context assembly.
"""
from app.services.embeddings import EmbeddingService
from app.core.qdrant_client import search
from app.config import settings
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

# Rough 1 token ≈ 4 characters → 3000 tokens ≈ 12 000 chars.
MAX_CONTEXT_CHARS = 12_000


class RetrievalService:
    """Service for embedding queries and searching the vector index."""

    def __init__(self):
        self.embedding_service = EmbeddingService()

    async def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.5,
        doc_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Embed a query and search Qdrant for similar documents.

        Args:
            query: The user's natural-language question.
            top_k: Maximum number of results to return.
            score_threshold: Minimum similarity score (cosine, 0-1).
            doc_type: If set, restrict search to this doc_type payload value.

        Returns:
            List of scored result dicts (see core.qdrant_client.search).
        """
        query_vector = await self.embedding_service.embed_text(query)
        results = search(
            query_vector=query_vector,
            top_k=top_k,
            score_threshold=score_threshold,
            doc_type=doc_type,
        )
        logger.info("Retrieved %d results for query: %s", len(results), query[:80])
        return results

    @staticmethod
    def build_context(results: List[Dict[str, Any]], max_chars: int = MAX_CONTEXT_CHARS) -> str:
        """Assemble a context string from retrieved results.

        Each result's content is prefixed with its source file name so
        the generation model can reference it.  The total is capped at
        *max_chars* to stay within a reasonable token budget (~3000 tokens).

        Args:
            results: Output from :meth:`search`.
            max_chars: Maximum total character budget for the context block.

        Returns:
            A single string suitable for insertion into the generation prompt.
        """
        parts: List[str] = []
        current_len = 0

        for i, r in enumerate(results):
            source = r.get("source_file", "unknown")
            excerpt = r.get("content", "")
            block = f"[{source}] {excerpt}\n\n"

            if current_len + len(block) > max_chars:
                # Truncate the last block to fit the budget.
                remaining = max_chars - current_len
                if remaining > 100:
                    parts.append(block[:remaining])
                break

            parts.append(block)
            current_len += len(block)

        return "".join(parts)
