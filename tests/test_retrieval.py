"""Phase 8 integration test: confirm retrieval.search() returns a
non-empty, correctly-ordered result for a query matching known ingested
content (per the build plan).

This is an OPT-IN integration test — it hits the real Gemini embedding
API and a real (ingested) Qdrant collection. Run it with:

    OPSRAG_RUN_INTEGRATION=1 pytest tests/test_retrieval.py

after having (a) put real keys in .env and (b) run scripts.ingest once.
Skipped by default so `pytest` stays hermetic for CI / fresh clones.
"""
import asyncio
import os

import pytest

pytestmark = pytest.mark.skipif(
    os.getenv("OPSRAG_RUN_INTEGRATION", "").lower() not in ("1", "true", "yes"),
    reason=(
        "Integration test: needs real .env keys and an ingested Qdrant "
        "collection. Opt in with OPSRAG_RUN_INTEGRATION=1."
    ),
)


def test_search_returns_relevant_ordered_results():
    from app.services.retrieval import RetrievalService

    service = RetrievalService()
    results = asyncio.run(
        service.search(
            query="What are the ESD handling requirements for PCB assembly?",
            top_k=5,
            score_threshold=0.5,
        )
    )

    # Non-empty: the ingested corpus definitely covers ESD handling.
    assert len(results) > 0

    # Correctly ordered: Qdrant returns cosine similarity descending.
    scores = [r["score"] for r in results]
    assert scores == sorted(scores, reverse=True)

    # Relevant: at least one hit references the ESD SOP.
    assert any(
        "esd" in (r.get("source_file", "") + " " + r.get("content", "")).lower()
        for r in results
    )


def test_search_with_doc_type_filter():
    from app.services.retrieval import RetrievalService

    service = RetrievalService()
    results = asyncio.run(
        service.search(
            query="line changeover procedure",
            top_k=5,
            score_threshold=0.5,
            doc_type="sop",
        )
    )

    assert len(results) > 0
    # Filter respected: every hit is an SOP.
    assert all(r["doc_type"] == "sop" for r in results)