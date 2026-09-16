"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import health
from app.routers import chat

# Create FastAPI app
app = FastAPI(
    title="OpsRAG",
    description="Manufacturing Operations RAG Assistant",
    version="0.1.0",
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (Phase 5 frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["RAG"])


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    # The Qdrant collection is created by the ingest script.
    # We log a reminder if it hasn't been set up yet.
    from app.core.qdrant_client import collection_exists
    if not collection_exists():
        import logging
        logging.warning(
            "Qdrant collection '%s' does not exist. "
            "Run 'python -m scripts.ingest' to populate the vector index.",
            "opsrag_docs",
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
