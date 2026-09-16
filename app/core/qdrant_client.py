"""Qdrant vector database client singleton and collection management."""
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)
from app.config import settings
from typing import List, Optional, Dict, Any
import hashlib
import logging

logger = logging.getLogger(__name__)

# Module-level singleton; initialised lazily on first use.
_client: Optional[QdrantClient] = None


def get_client() -> QdrantClient:
    """Return the shared QdrantClient instance, creating it on first call."""
    global _client
    if _client is None:
        _client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _client


def create_collection(vector_size: int, recreate: bool = False) -> None:
    """Create the Qdrant collection, optionally dropping an existing one first.

    Args:
        vector_size: Dimensionality of the embedding vectors.
        recreate: If True, drop and recreate the collection (clean rebuild).
    """
    client = get_client()

    if recreate:
        # Drop the existing collection, then recreate from scratch.
        try:
            client.delete_collection(settings.collection_name)
            logger.info("Deleted existing collection: %s", settings.collection_name)
        except Exception:
            pass  # Collection didn't exist; that's fine.

        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        logger.info(
            "Created collection '%s' with vector_size=%d, distance=COSINE",
            settings.collection_name,
            vector_size,
        )
    elif not collection_exists():
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
        logger.info(
            "Created collection '%s' with vector_size=%d, distance=COSINE",
            settings.collection_name,
            vector_size,
        )
    else:
        logger.info(
            "Collection '%s' already exists; upserting into it.",
            settings.collection_name,
        )


def collection_exists() -> bool:
    """Return True if the target collection already exists."""
    client = get_client()
    collections = client.get_collections().collections
    return any(c.name == settings.collection_name for c in collections)


def upsert_points(points: List[PointStruct]) -> int:
    """Upsert a batch of points into the Qdrant collection.

    Args:
        points: List of PointStruct objects with deterministic IDs.

    Returns:
        Number of points upserted.
    """
    client = get_client()
    client.upsert(
        collection_name=settings.collection_name,
        points=points,
        # Wait for the operation to complete so callers can immediately search.
        wait=True,
    )
    logger.info("Upserted %d points into '%s'", len(points), settings.collection_name)
    return len(points)


def search(
    query_vector: List[float],
    top_k: int = 5,
    score_threshold: float = 0.5,
    doc_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search the collection for similar vectors.

    Args:
        query_vector: Embedding vector of the query.
        top_k: Maximum number of results to return.
        score_threshold: Minimum similarity score (0-1 for cosine).
        doc_type: If provided, filter results to this document type.

    Returns:
        List of dicts with keys: content, doc_type, doc_id, score, metadata.
    """
    client = get_client()

    query_filter = None
    if doc_type is not None:
        query_filter = Filter(
            must=[FieldCondition(key="doc_type", match=MatchValue(value=doc_type))]
        )

    search_result = client.query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        limit=top_k,
        score_threshold=score_threshold,
        query_filter=query_filter,
        with_payload=True,
    )

    results: List[Dict[str, Any]] = []
    for hit in search_result.points:
        payload = hit.payload or {}
        results.append({
            "content": payload.get("content", ""),
            "doc_type": payload.get("doc_type", ""),
            "doc_id": payload.get("doc_id", ""),
            "source_file": payload.get("source_file", ""),
            "title": payload.get("title", ""),
            "score": hit.score,
            "metadata": {
                k: v for k, v in payload.items()
                if k not in ("content", "doc_type", "doc_id", "source_file", "title")
            },
        })

    return results


def make_point_id(source_file: str, chunk_index: int) -> str:
    """Generate a deterministic point ID from source_file and chunk_index.

    This ensures re-running the ingest script updates existing points
    rather than creating duplicates.
    """
    raw = f"{source_file}:{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()
