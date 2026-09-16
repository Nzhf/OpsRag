"""Agentic tool-calling orchestration loop.

This module implements the core agent behaviour:

1. Send the user's question (plus tool definitions) to Groq.
2. If the model emits tool calls, execute the matching function from
   the TOOL_REGISTRY and append the result back as a tool-role message.
3. Call Groq again with the updated conversation for a final answer.
4. If the model answers directly without a tool call, return that.

The result includes the final answer, any sources surfaced by the tools,
and a record of the tool calls made (useful for the frontend display).
"""
from app.core.groq_client import GroqClient
from app.services.tools import TOOL_DEFINITIONS, TOOL_REGISTRY
from app.models import AgentResponse, SourceDocument
from typing import Dict, Any, List
import json
import logging

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are OpsRAG, a Manufacturing Operations RAG Assistant
for BizLink Penang Manufacturing (a fictional electronics assembly site).

You help factory operators, line leaders, and technicians with:
1. Looking up SOP procedures (lookup_sop)
2. Checking inventory levels (check_inventory_status)
3. Summarizing defect log entries (summarize_defect_log)

Guidelines:
- If the user asks about a procedure, process, or how-to, use lookup_sop.
- If the user asks about material stock levels or "how much X we have",
  use check_inventory_status.
- If the user asks about defect patterns or summaries, use summarize_defect_log.
- You can call multiple tools in a single turn if the question requires it.
- Always base your final answer on the actual tool results. Never make up
  inventory numbers, defect counts, or SOP content.
- Cite which source document or data file each part of your answer came from.
- Keep answers concise and actionable for a factory floor audience.
"""


class AgentService:
    """Orchestrates the tool-calling loop with Groq."""

    def __init__(self):
        self.client = GroqClient()

    async def run(self, question: str) -> AgentResponse:
        """Run the agentic loop and return the final answer.

        Args:
            question: The user's natural-language question.

        Returns:
            An AgentResponse with answer, sources, and tool calls.
        """
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]

        all_tool_calls: List[Dict[str, Any]] = []
        sources: List[SourceDocument] = []

        # ---- First call to Groq ----
        response = await self.client.chat_completion(
            messages=messages,
            tools=TOOL_DEFINITIONS,
            tool_choice="auto",
        )
        assistant_msg = GroqClient.extract_message(response)

        # ---- Execute any tool calls ----
        if assistant_msg.get("tool_calls"):
            messages.append({
                "role": "assistant",
                "content": assistant_msg.get("content"),
                "tool_calls": assistant_msg["tool_calls"],
            })

            for tc in assistant_msg["tool_calls"]:
                func_name = tc["function"]["name"]
                args_str = tc["function"].get("arguments", "{}")
                try:
                    args = json.loads(args_str)
                except json.JSONDecodeError:
                    args = {}

                logger.info("Tool call: %s(%s)", func_name, args)

                if func_name in TOOL_REGISTRY:
                    result = await TOOL_REGISTRY[func_name](**args)
                    result_str = json.dumps(result, default=str)
                else:
                    result_str = json.dumps(
                        {"error": f"Unknown tool: {func_name}"}
                    )
                    result = {"error": f"Unknown tool: {func_name}"}

                all_tool_calls.append({
                    "name": func_name,
                    "arguments": args,
                    "result": result,
                })

                self._collect_sources_from_tool(func_name, result, sources)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result_str,
                })

            # ---- Second call: get the final natural-language answer ----
            response = await self.client.chat_completion(
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto",
            )
            assistant_msg = GroqClient.extract_message(response)

        # ---- Build the final response ----
        # Deduplicate sources by source_file
        seen_files: set = set()
        unique_sources: List[SourceDocument] = []
        for s in sources:
            key = s.source_file or s.excerpt[:50]
            if key not in seen_files:
                seen_files.add(key)
                unique_sources.append(s)

        return AgentResponse(
            answer=assistant_msg.get("content", ""),
            sources=unique_sources,
            tool_calls=all_tool_calls if all_tool_calls else None,
        )

    @staticmethod
    def _collect_sources_from_tool(
        func_name: str,
        result: Dict[str, Any],
        sources: List[SourceDocument],
    ) -> None:
        """Extract SourceDocument entries from a tool result."""
        if func_name == "lookup_sop":
            if result.get("found"):
                sources.append(SourceDocument(
                    doc_type="sop",
                    source_file=result.get("source_file", ""),
                    excerpt=result.get("excerpt", "")[:500],
                    score=result.get("score", 0.0),
                    metadata={"title": result.get("title", "")},
                ))
        elif func_name == "check_inventory_status":
            if result.get("found"):
                sources.append(SourceDocument(
                    doc_type="inventory",
                    source_file="inventory_snapshot_august_2026.json",
                    excerpt=result.get("status_detail", ""),
                    score=1.0,
                    metadata={
                        "item_id": result.get("item_id", ""),
                        "quantity_on_hand": result.get("quantity_on_hand", 0),
                        "reorder_threshold": result.get("reorder_threshold", 0),
                        "status": result.get("status", ""),
                    },
                ))
        elif func_name == "summarize_defect_log":
            sources.append(SourceDocument(
                doc_type="defect_log",
                source_file="defect_log_august_2026.json",
                excerpt=f"Total defects in period: {result.get('total_defects', 0)}",
                score=1.0,
                metadata={
                    "date_range": result.get("date_range_query", ""),
                    "by_defect_type": result.get("by_defect_type", {}),
                    "by_line": result.get("by_line", {}),
                },
            ))