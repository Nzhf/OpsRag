"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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


@app.get("/", include_in_schema=False)
async def root():
    """Serve the chat UI at the root path."""
    return FileResponse("static/index.html")

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, tags=["RAG"])


@app.on_event("startup")
async def startup_event():
    """Log a reminder if the vector index hasn't been built yet.

    Deliberately non-fatal: a transient Qdrant outage at boot should
    not take the API down — /health and the UI still respond.
    """
    import logging
    try:
        from app.core.qdrant_client import collection_exists
        if not collection_exists():
            logging.warning(
                "Qdrant collection does not exist yet. "
                "Run 'python -m scripts.ingest --recreate-collection' to build it."
            )
    except Exception as exc:  # noqa: BLE001 - startup must never crash
        logging.warning("Could not reach Qdrant at startup: %s", exc)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
