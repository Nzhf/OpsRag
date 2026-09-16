"""Chat/RAG router with /chat/query (Phase 3) and /chat/agent (Phase 4).

/chat/query  - Plain retrieval-augmented generation: embed question,
               search Qdrant, build context, generate answer.

/chat/agent  - Agentic tool-calling: model decides which of three tools
               to invoke (lookup_sop, check_inventory_status,
               summarize_defect_log), executes them locally, and returns
               a final grounded answer.
"""
from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse, AgentResponse, SourceDocument
from app.services.retrieval import RetrievalService
from app.services.generation import GenerationService
from app.services.agent import AgentService

router = APIRouter()

# Singletons — created once per module load (settings are env-driven so
# these are safe to reuse across requests within the same process).
_retrieval = RetrievalService()
_generation = GenerationService()
_agent = AgentService()

# Fallback answer returned when retrieval finds nothing relevant.


@router.post("/chat/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """Plain RAG endpoint (Phase 3).

    Embeds the question, searches Qdrant for relevant documents,
    builds a context window, and calls Groq to generate an answer.
    Returns a fallback message if retrieval yields nothing above
    the score threshold.
    """
    # 1. Search the vector index
    results = await _retrieval.search(
        query=request.question,
        top_k=request.top_k,
        score_threshold=0.5,
    )

    # 2. Fallback if nothing relevant was found
    if not results:
        return ChatResponse(
            answer=_FALLBACK_ANSWER,
            sources=[],
        )

    # 3. Build context and generate
    context = _retrieval.build_context(results)
    answer = await _generation.generate(
        question=request.question,
        context=context,
    )

    # 4. Format sources for the response
    sources = [
        SourceDocument(
            doc_type=r.get("doc_type", ""),
            source_file=r.get("source_file", ""),
            excerpt=r.get("content", "")[:500],
            score=round(r.get("score", 0.0), 4),
            metadata=r.get("metadata", {}),
        )
        for r in results
    ]

    return ChatResponse(answer=answer, sources=sources)


@router.post("/chat/agent", response_model=AgentResponse)
async def chat_agent(request: ChatRequest):
    """Agentic tool-calling endpoint (Phase 4).

    The model receives three tools (lookup_sop, check_inventory_status,
    summarize_defect_log) and decides which to invoke.  Each tool call
    is executed locally, the results are fed back to the model, and a
    final grounded answer is produced.
    """
    return await _agent.run(question=request.question)
_FALLBACK_ANSWER = (
    "I don't have enough information in my knowledge base to answer that "
    "question. Could you try rephrasing, or ask something about SOPs, "
    "inventory levels, or defect summaries?"
)
