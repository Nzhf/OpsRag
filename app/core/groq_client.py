"""Groq API client wrapper for text generation and tool-calling.

The Groq API is OpenAI-compatible, so we use httpx to make the calls
directly, avoiding an extra SDK dependency.  This module centralises
all Groq request/response handling so the service layer stays clean.
"""
import httpx
from app.config import settings
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class GroqClient:
    """Thin async wrapper around the Groq chat-completion endpoint."""

    def __init__(self):
        self.api_key = settings.groq_api_key
        self.model = settings.groq_model
        self.base_url = GROQ_BASE_URL
        self.default_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        tool_choice: str = "auto",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Call the Groq chat-completion endpoint.

        Args:
            messages: Conversation messages (system, user, assistant, tool).
            tools: Optional tool definitions for function-calling.
            tool_choice: "auto", "none", or "required".
            temperature: Sampling temperature (defaults to settings value).
            max_tokens: Max tokens in response (defaults to settings value).

        Returns:
            Parsed JSON response from Groq.
        """
        request_body: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else settings.temperature,
            "max_tokens": max_tokens if max_tokens is not None else settings.max_tokens,
        }

        if tools:
            request_body["tools"] = tools
            request_body["tool_choice"] = tool_choice

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.default_headers,
                json=request_body,
            )
            response.raise_for_status()
            return response.json()

    @staticmethod
    def extract_message(response: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the assistant message from a Groq response.

        Returns a dict with 'content', 'tool_calls' (or None).
        """
        choices = response.get("choices", [])
        if not choices:
            return {"content": "", "tool_calls": None}
        message = choices[0].get("message", {})
        return {
            "role": message.get("role", "assistant"),
            "content": message.get("content") or "",
            "tool_calls": message.get("tool_calls"),
        }

    @staticmethod
    def get_usage(response: Dict[str, Any]) -> Dict[str, int]:
        """Extract token usage from a Groq response."""
        return response.get("usage", {})
