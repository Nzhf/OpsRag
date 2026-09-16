"""Agentic tools for the OpsRAG agent.

Each tool is an async function that the model can call during the
agentic reasoning loop (see app/services/agent.py).  The tool
definitions (JSON schemas expected by the Groq tool-calling format)
and a TOOL_REGISTRY mapping name -> callable are both defined here so
the agent can stay agnostic of the actual implementations.
"""
from app.core.qdrant_client import search
from app.services.embeddings import EmbeddingService
from app.config import settings
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import date, datetime, timedelta
import json
import logging
import re
import difflib

logger = logging.getLogger(__name__)

# Resolve the data directory relative to the project root.
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
INVENTORY_PATH = DATA_DIR / "inventory" / "inventory_snapshot_august_2026.json"
DEFECTS_PATH = DATA_DIR / "defects" / "defect_log_august_2026.json"


# ---------------------------------------------------------------------------
# Tool definitions (JSON schemas passed to Groq)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "lookup_sop",
            "description": (
                "Search the SOP knowledge base for a specific manufacturing "
                "topic or procedure. Use this when the user asks about a "
                "process, procedure, safety requirement, or how-to question "
                "related to SMT, assembly, quality, or materials."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": (
                            "The manufacturing topic, procedure, or subject "
                            "matter to search for. Examples: 'ESD handling', "
                            "'reflow solder profile', 'stencil changeover', "
                            "'incoming material inspection', 'NCR reporting'."
                        ),
                    }
                },
                "required": ["topic"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_inventory_status",
            "description": (
                "Check the current stock level for a specific component, "
                "material, or consumable item in the manufacturing warehouse. "
                "Use this when the user asks 'how much X do we have', 'is X "
                "running low', or 'what is the stock level of X'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": (
                            "The name, description, or ID of the inventory "
                            "item. Examples: 'solder paste', 'MCU STM32F407"
                            "VGT6', '4.7k resistor', 'COMP-001'."
                        ),
                    }
                },
                "required": ["item"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_defect_log",
            "description": (
                "Summarize defect log entries for a specified date range, "
                "including counts grouped by defect type and production line. "
                "Use this when the user asks about defect patterns, 'what "
                "defects occurred last week', or 'summarize defects for "
                "August'."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "date_range": {
                        "type": "string",
                        "description": (
                            "A date range description. Examples: 'last 7 days'"
                            ", 'August 2026', '2026-08-01 to 2026-08-15', "
                            "'this week'."
                        ),
                    }
                },
                "required": ["date_range"],
            },
        },
    },
]


# ---------------------------------------------------------------------------
# Tool #1: lookup_sop
# ---------------------------------------------------------------------------

async def lookup_sop(topic: str) -> Dict[str, Any]:
    """Vector-search the SOP documents for *topic*.

    Returns the most relevant SOP excerpt along with metadata.
    """
    embedding_service = EmbeddingService()
    query_vector = await embedding_service.embed_text(topic)

    results = search(
        query_vector=query_vector,
        top_k=3,
        score_threshold=0.5,
        doc_type="sop",
    )

    if not results:
        return {
            "topic": topic,
            "found": False,
            "message": (
                f"No SOP documents found matching '{topic}'. "
                "The topic may not be covered in the current knowledge base."
            ),
            "excerpt": "",
            "source_file": "",
        }

    

# ---------------------------------------------------------------------------
# Tool #2: check_inventory_status  (inventory helpers)
# ---------------------------------------------------------------------------

def _load_inventory() -> List[Dict[str, Any]]:
    """Load the inventory snapshot from the JSON data file."""
    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["inventory"]


def _find_inventory_item(query: str) -> Optional[Dict[str, Any]]:
    """Fuzzy-match an inventory item by item_id, description, or manufacturer_pn.

    Returns the best-matching item dict, or None if nothing is found.
    """
    items = _load_inventory()
    query_lower = query.lower().strip()

    # 1. Exact match on item_id (e.g. "COMP-001")
    for item in items:
        if item["item_id"].lower() == query_lower:
            return item

    # 2. Exact match on description (case-insensitive)
    for item in items:
        if item["description"].lower() == query_lower:
            return item

    # 3. Substring match on description
    for item in items:
        desc = item["description"].lower()
        if query_lower in desc:
            return item

    # 4. Fuzzy match using difflib
    descriptions = [item["description"].lower() for item in items]
    matches = difflib.get_close_matches(query_lower, descriptions, n=1, cutoff=0.4)
    if matches:
        for item in items:
            if item["description"].lower() == matches[0]:
                return item

    return None


def _classify_status(quantity: int, threshold: int) -> str:
    """Classify stock level as ok / low / critical.

    - ok:      quantity >= threshold     (at or above reorder point)
    - low:     threshold > quantity >= 50 % of threshold
    - critical: quantity < 50 % of threshold
    """
    if quantity >= threshold:
        return "ok"
    elif quantity >= threshold * 0.5:
        return "low"
    else:
        return "critical"


async def check_inventory_status(item: str) -> Dict[str, Any]:
    """Look up *item* in the inventory JSON and classify stock level."""
    found = _find_inventory_item(item)

    if found is None:
        return {
            "item": item,
            "found": False,
            "message": (
                f"'{item}' was not found in the inventory database. "
                "Please check the spelling or item ID and try again."
            ),
        }

    quantity = found["quantity_on_hand"]
    threshold = found["reorder_threshold"]
    status = _classify_status(quantity, threshold)

    return {
        "item": found["description"],
        "item_id": found["item_id"],
        "found": True,
        "quantity_on_hand": quantity,
        "reorder_threshold": threshold,
        "unit": found.get("unit_of_measure", "pieces"),
        "status": status,
        "location": found.get("location", ""),
        "status_detail": (
            f"Stock level is {status}. "
            f"{quantity} {found.get('unit_of_measure', 'pieces')} on hand, "
            f"reorder threshold is {threshold}."
        ),
    }


# ---------------------------------------------------------------------------
# Tool #3: summarize_defect_log  (defect-log helpers)
# ---------------------------------------------------------------------------

def _load_defect_log() -> List[Dict[str, Any]]:
    """Load defect log entries from the JSON data file."""
    with open(DEFECTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["defects"]


def _parse_date_range(date_range: str) -> tuple:
    """Parse a human-readable date range string.

    Supports "last N days", "this week", "YYYY-MM-DD to YYYY-MM-DD",
    "Month Year" (e.g. "August 2026"), or defaults to all available data.
    """
    text = date_range.strip().lower()

    # Explicit range: "2026-08-01 to 2026-08-15" or "2026-08-01 - 2026-08-15"
    match = re.search(
        r"(\d{4}-\d{2}-\d{2})\s*(?:to|[-])\s*(\d{4}-\d{2}-\d{2})", date_range
    )
    if match:
        start = datetime.strptime(match.group(1), "%Y-%m-%d").date()
        end = datetime.strptime(match.group(2), "%Y-%m-%d").date()
        return start, end

    # "last N days"
    match = re.search(r"last (\d+) days?", text)
    if match:
        n = int(match.group(1))
        defects = _load_defect_log()
        latest = max(
            datetime.strptime(d["date"], "%Y-%m-%d").date() for d in defects
        )
        return latest - timedelta(days=n), latest

    # "this week"
    if "this week" in text:
        defects = _load_defect_log()
        latest = max(
            datetime.strptime(d["date"], "%Y-%m-%d").date() for d in defects
        )
        start = latest - timedelta(days=latest.weekday())
        end = start + timedelta(days=6)
        return start, end

    # "Month Year" (e.g. "August 2026")
    match = re.search(r"(\w+)\s+(\d{4})", date_range)
    if match:
        month_str, year_str = match.group(1), match.group(2)
        try:
            dt = datetime.strptime(f"{month_str} {year_str}", "%B %Y")
        except ValueError:
            try:
                dt = datetime.strptime(f"{month_str} {year_str}", "%b %Y")
            except ValueError:
                dt = None
        if dt:
            year, month = dt.year, dt.month
            start = date(year, month, 1)
            if month == 12:
                end = date(year, 12, 31)
            else:
                end = date(year, month + 1, 1) - timedelta(days=1)
            return start, end

    # Default: entire range of available data
    defects = _load_defect_log()
    if not defects:
        return date(2026, 1, 1), date(2026, 12, 31)
    dates = [
        datetime.strptime(d["date"], "%Y-%m-%d").date() for d in defects
    ]
    return min(dates), max(dates)


async def summarize_defect_log(date_range: str) -> Dict[str, Any]:
    """Summarize defect entries matching *date_range*."""
    defects = _load_defect_log()
    start, end = _parse_date_range(date_range)

    filtered: List[Dict[str, Any]] = []
    for d in defects:
        d_date = datetime.strptime(d["date"], "%Y-%m-%d").date()
        if start <= d_date <= end:
            filtered.append(d)

    by_type: Dict[str, int] = {}
    by_line: Dict[str, int] = {}
    by_shift: Dict[str, int] = {}
    root_causes: List[str] = []

    for d in filtered:
        dtype = d.get("defect_type", "Unknown")
        line = d.get("line", "Unknown")
        shift = d.get("shift", "Unknown")
        by_type[dtype] = by_type.get(dtype, 0) + 1
        by_line[line] = by_line.get(line, 0) + 1
        by_shift[shift] = by_shift.get(shift, 0) + 1

        rc = d.get("root_cause", "")
        if rc and len(root_causes) < 10:
            root_causes.append(rc)

    return {
        "date_range_query": date_range,
        "start_date": str(start),
        "end_date": str(end),
        "total_defects": len(filtered),
        "by_defect_type": by_type,
        "by_line": by_line,
        "by_shift": by_shift,
        "top_root_causes": root_causes[:5],
        "sample_entries": [
            {
                "defect_id": d.get("defect_id"),
                "date": d.get("date"),
                "line": d.get("line"),
                "defect_type": d.get("defect_type"),
                "root_cause": d.get("root_cause"),
                "corrective_action": d.get("corrective_action"),
            }
            for d in filtered[:5]
        ],
    }


# ---------------------------------------------------------------------------
# Registry: maps function names to callables for the agent loop.
# ---------------------------------------------------------------------------

TOOL_REGISTRY: Dict[str, Any] = {
    "lookup_sop": lookup_sop,
    "check_inventory_status": check_inventory_status,
    "summarize_defect_log": summarize_defect_log,
}
