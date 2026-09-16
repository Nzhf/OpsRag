"""Generation service using the Groq API.

Used by the plain RAG endpoint (/chat/query) to produce a grounded
answer from retrieved context.  The agentic endpoint (/chat/agent)
uses core.groq_client.GroqClient directly so it can pass tool
definitions and handle multi-step tool-calling.
"""
from app.core.groq_client import GroqClient
from app.config import settings
from typing import List, Dict, Any

SYSTEM_PROMPT_RAG = """You are OpsRAG, a Manufacturing Operations RAG Assistant
for BizLink Penang Manufacturing. Your job is to answer questions
from factory operators, technicians, and supervisors using only the
information provided in the context below.

Instructions:
- Answer strictly from the provided context. Do not add information
  from your own training data.
- Reference which source document each part of your answer came from.
- If the context does not contain enough information to answer the
  question, say so explicitly rather than guessing.
- Keep answers concise and actionable.
"""

# Rough 1 token ≈ 4 characters → 3000 tokens ≈ 12 000 chars.
MAX_CONTEXT_CHARS = 12_000


class GenerationService:
    """Service for plain (non-agentic) text generation via Groq."""

    def __init__(self):
        self.client = GroqClient()

    async def generate(
        self,
        question: str,
        context: str,
        system_prompt: str = SYSTEM_PROMPT_RAG,
    ) -> str:
        """Generate a grounded answer from retrieved context.

        Args:
            question: The user's question.
            context: Concatenated text from retrieved documents.
            system_prompt: System prompt instructing grounding behaviour.

        Returns:
            The generated answer text.
        """
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ]

        response = await self.client.chat_completion(
            messages=messages,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
        )

        message = GroqClient.extract_message(response)
        return message["content"]

