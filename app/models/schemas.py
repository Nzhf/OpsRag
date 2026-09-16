"""Pydantic models for request/response schemas."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date


class ChatRequest(BaseModel):
    """Request body for /chat/query and /chat/agent."""
    question: str = Field(..., min_length=1, description="User's question")
    top_k: int = Field(default=5, ge=1, le=20, description="Number of documents to retrieve")


class SourceDocument(BaseModel):
    """A source document returned in the response."""
    doc_type: str
    source_file: str
    excerpt: str
    score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    """Response from the plain RAG endpoint (/chat/query)."""
    answer: str
    sources: List[SourceDocument]


class AgentResponse(BaseModel):
    """Response from the agentic endpoint (/chat/agent)."""
    answer: str
    sources: List[SourceDocument]
    tool_calls: Optional[List[Dict[str, Any]]] = None


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str


class ToolCall(BaseModel):
    """A single tool call from the agent."""
    name: str
    arguments: Dict[str, Any]
    result: str


class AgentStep(BaseModel):
    """One step in the agentic reasoning loop."""
    step_type: str  # "tool_call" or "response"
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None


class SopDocument(BaseModel):
    """SOP document structure."""
    doc_id: str
    title: str
    doc_type: str = "sop"
    content: str
    line: str
    department: str
    created_date: date


class DefectLog(BaseModel):
    """Defect log entry structure."""
    doc_id: str
    doc_type: str = "defect_log"
    defect_type: str
    line: str
    shift: str
    root_cause: str
    corrective_action: str
    log_date: date


class ShiftHandover(BaseModel):
    """Shift handover note structure."""
    doc_id: str
    doc_type: str = "handover"
    shift: str
    line: str
    notes: str
    handover_date: date


class InventoryItem(BaseModel):
    """Inventory item structure."""
    item_id: str
    item_name: str
    quantity: int
    reorder_threshold: int
    unit: str