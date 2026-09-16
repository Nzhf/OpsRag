"""
Phase 2 - Ingestion pipeline for OpsRAG.

Loads all synthetic manufacturing documents, chunks them sensibly,
embeds each chunk with the Gemini embedding API, and upserts into
a Qdrant collection with rich metadata.

Usage:
    python -m scripts.ingest                # incremental upsert
    python -m scripts.ingest --recreate     # drop & recreate collection first

Deterministic point IDs (hash of source_file + chunk_index) ensure
re-running the script updates existing points instead of duplicating.
"""
import argparse
import asyncio
import hashlib
import re
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from qdrant_client.models import PointStruct

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from app.config import settings
from app.core.qdrant_client import create_collection, upsert_points
from app.services.embeddings import EmbeddingService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ingest")

DATA_DIR = PROJECT_ROOT / "data"


def deterministic_point_id(source_file: str, chunk_index: int) -> str:
    """Generate a deterministic point ID so re-runs update, not duplicate."""
    raw = f"{source_file}:{chunk_index}"
    return hashlib.md5(raw.encode()).hexdigest()


def _make_chunk(
    source_file: str, chunk_index: int, text: str,
    doc_type: str, title: str = "", line: str = "",
    department: str = "", date: str = "",
) -> Dict[str, Any]:
    """Build a chunk dict with content + metadata payload."""
    return {
        "text": text,
        "metadata": {
            "doc_type": doc_type,
            "source_file": source_file,
            "title": title,
            "line": line,
            "department": department,
            "date": date,
            "chunk_index": chunk_index,
        },
    }


# ---------------------------------------------------------------------------
# SOP loading & chunking
# ---------------------------------------------------------------------------

def load_sops() -> List[Dict[str, Any]]:
    """Load and chunk all SOP markdown files.

    Splits each SOP by ``##`` section headings; if a section exceeds
    the target chunk size it is further split by paragraph with overlap.
    """
    chunks: List[Dict[str, Any]] = []

    for md_file in sorted(SOPS_DIR.glob("*.md")):
        source_file = md_file.name
        text = md_file.read_text(encoding="utf-8")

        title_match = re.match(r"^#\s+(.+)", text.strip())
        title = title_match.group(1).strip() if title_match else source_file

        metadata = _parse_sop_metadata(text)
        sections = _split_by_sections(text)

        chunk_index = 0
        for heading, section_text in sections:
            if len(section_text) <= MAX_CHUNK_CHARS:
                chunks.append(_make_chunk(
                    source_file, chunk_index, section_text,
                    "sop", title, metadata.get("line", ""),
                    metadata.get("department", ""), metadata.get("date", ""),
                ))
                chunk_index += 1
            else:
                paragraphs = _split_paragraphs(section_text)
                current_overlap = ""
                current_chunk = ""

                for para in paragraphs:
                    if len(current_chunk) + len(para) <= MAX_CHUNK_CHARS:
                        if current_chunk:
                            current_chunk += "\n\n"
                        current_chunk += para
                    else:
                        if current_chunk:
                            full = current_overlap + "\n\n" + current_chunk if current_overlap else current_chunk
                            chunks.append(_make_chunk(
                                source_file, chunk_index, full.strip(),
                                "sop", title, metadata.get("line", ""),
                                metadata.get("department", ""), metadata.get("date", ""),
                            ))
                            chunk_index += 1


def _parse_sop_metadata(text: str) -> Dict[str, str]:
    """Extract metadata from the **Key:** Value header block of an SOP."""
    fields = {}
    patterns = {
        "document_id": r"\*\*Document ID:\*\*\s*(.+)",
        "version": r"\*\*Version:\*\*\s*(.+)",
        "date": r"\*\*Effective Date:\*\*\s*(.+)",
        "department": r"\*\*Department:\*\*\s*(.+)",
        "line": r"\*\*Applies to:\*\*\s*(.+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            fields[key] = match.group(1).strip()
    return fields


def _split_by_sections(text: str) -> List[Tuple[str, str]]:
    """Split markdown body by ``##`` section headings."""
    parts = text.split("\n---\n", 1)
    body = parts[1] if len(parts) > 1 else text
    heading_re = re.compile(r"^##\s+(.+)$", re.MULTILINE)
    matches = list(heading_re.finditer(body))
    sections: List[Tuple[str, str]] = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections.append((match.group(1), body[start:end].strip()))
    return sections


def _split_paragraphs(text: str) -> List[str]:
    """Split text into paragraphs separated by double newlines."""
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


# ---------------------------------------------------------------------------
# Defect-log loading & chunking
# ---------------------------------------------------------------------------

def load_defect_logs() -> List[Dict[str, Any]]:
    """Load and chunk defect log entries (each entry = one chunk)."""
    chunks: List[Dict[str, Any]] = []
    source_file = DEFECTS_PATH.name

    with open(DEFECTS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, d in enumerate(data["defects"]):
        text = _format_defect_entry(d)
        chunks.append(_make_chunk(
            source_file, i, text,
            "defect_log",
            title=f"{d.get('defect_type', 'Unknown')} - {d.get('defect_id', '')}",
            line=d.get("line", ""),
            department="Quality",
            date=d.get("date", ""),
        ))

    logger.info("Loaded %d defect log chunks", len(chunks))
    return chunks


# ---------------------------------------------------------------------------
# Handover-note loading & chunking
# ---------------------------------------------------------------------------

def load_handover_notes() -> List[Dict[str, Any]]:
    """Load and chunk shift handover notes (each note = one chunk)."""
    chunks: List[Dict[str, Any]] = []
    source_file = HANDOVERS_PATH.name

    with open(HANDOVERS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, h in enumerate(data["handovers"]):
        text = _format_handover_entry(h)
        chunks.append(_make_chunk(
            source_file, i, text,
            "handover",
            title=f"Shift Handover - {h.get('date', '')}",
            line=h.get("line", ""),
            department="Production",
            date=h.get("date", ""),
        ))

    logger.info("Loaded %d handover note chunks", len(chunks))
    return chunks


def _format_handover_entry(h: Dict[str, Any]) -> str:
    """Format a single handover note as readable text."""
    prod = h.get("production_status", {})
    qual = h.get("quality_issues", {})
    equip = h.get("equipment_status", {})
    mat = h.get("material_status", {})
    parts = [
        f"Handover ID: {h.get('handover_id', 'N/A')}",
        f"Date: {h.get('date', 'N/A')}",
        f"Line: {h.get('line', 'N/A')}",
        f"Shift Change: {h.get('outgoing_shift', '')} -> {h.get('incoming_shift', '')}",
        f"Product: {h.get('product', 'N/A')}",
        f"Outgoing Leader: {h.get('line_leader_outgoing', '')}",
        f"Incoming Leader: {h.get('line_leader_incoming', '')}",
        f"Production Status: {prod.get('status', '')}",
        f"Units Produced: {prod.get('units_produced', '')} of target {prod.get('units_target', '')}",
        f"Quality Issues: {qual.get('defects_found', '')}",
        f"NCR Initiated: {qual.get('ncr_initiated', '')}",
        f"Equipment Issues: {equip.get('issues', '')}",
        f"Material Status: {mat.get('low_stock', '')}",
        f"Pending Actions: {', '.join(h.get('pending_actions', []))}",
        f"Notes: {h.get('notes', '')}",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Inventory loading & chunking
# ---------------------------------------------------------------------------

def load_inventory() -> List[Dict[str, Any]]:
    """Load and chunk inventory items (each item = one chunk)."""
    chunks: List[Dict[str, Any]] = []
    source_file = INVENTORY_PATH.name

    with open(INVENTORY_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    snapshot_date = data.get("metadata", {}).get("snapshot_date", "")

    for i, item in enumerate(data["inventory"]):
        text = _format_inventory_entry(item)
        chunks.append(_make_chunk(
            source_file, i, text,
            "inventory",
            title=item.get("description", ""),
            line=item.get("location", ""),
            department="Materials",
            date=snapshot_date,
        ))

    logger.info("Loaded %d inventory chunks", len(chunks))
    return chunks


def _format_inventory_entry(item: Dict[str, Any]) -> str:
    """Format a single inventory item as readable text."""
    parts = [
        f"Item ID: {item.get('item_id', 'N/A')}",
        f"Description: {item.get('description', 'N/A')}",
        f"Category: {item.get('category', 'N/A')}",
        f"Package Type: {item.get('package_type', 'N/A')}",
        f"Manufacturer: {item.get('manufacturer', 'N/A')}",
        f"Manufacturer Part Number: {item.get('manufacturer_pn', 'N/A')}",
        f"Quantity On Hand: {item.get('quantity_on_hand', 0)}",
        f"Unit Of Measure: {item.get('unit_of_measure', 'pieces')}",
        f"Reorder Threshold: {item.get('reorder_threshold', 0)}",
        f"Reorder Quantity: {item.get('reorder_quantity', 0)}",
        f"Location: {item.get('location', 'N/A')}",
        f"Lot Number: {item.get('lot_number', 'N/A')}",
        f"Date Code: {item.get('date_code', 'N/A')}",
        f"MSL Level: {item.get('msd_level', 'N/A')}",
        f"Storage Requirements: {item.get('storage_requirements', 'N/A')}",
        f"Last Count Date: {item.get('last_count_date', 'N/A')}",
        f"Status: {item.get('status', 'N/A')}",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Embedding + upsert pipeline
# ---------------------------------------------------------------------------

def build_points(
    chunks: List[Dict[str, Any]],
    embeddings: List[List[float]],
) -> List[PointStruct]:
    """Combine chunks and their embeddings into Qdrant PointStructs."""
    points: List[PointStruct] = []
    for chunk, vector in zip(chunks, embeddings):
        meta = chunk["metadata"]
        point_id = deterministic_point_id(meta["source_file"], meta["chunk_index"])
        payload = {
            "content": chunk["text"],
            **meta,
        }
        points.append(PointStruct(id=point_id, vector=vector, payload=payload))
    return points


async def run_ingestion(recreate: bool = False) -> int:
    """Run the full ingestion pipeline and return the number of points upserted."""
    embedding_service = EmbeddingService()

    # 1. Load and chunk all document types.
    all_chunks: List[Dict[str, Any]] = []
    all_chunks.extend(load_sops())
    all_chunks.extend(load_defect_logs())
    all_chunks.extend(load_handover_notes())
    all_chunks.extend(load_inventory())
    logger.info("Total chunks to ingest: %d", len(all_chunks))

    # 2. Confirm the embedding dimension from an actual API response,
    #    rather than assuming the configured value.
    texts = [c["text"] for c in all_chunks]
    logger.info("Embedding %d chunks (batch size %d)...", len(texts), BATCH_SIZE)

    embeddings: List[List[float]] = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        batch_result = await embedding_service.embed_batch(batch)

        # embed_batch uses return_exceptions=True, so filter failures.
        actual: List[List[float]] = []
        for j, emb in enumerate(batch_result):
            if isinstance(emb, Exception):
                logger.error("Embedding failed for batch %d item %d: %s",
                             i // BATCH_SIZE, j, emb)
                actual.append([0.0] * settings.embedding_dimension)
            else:
                actual.append(emb)

        if i == 0 and actual and actual[0]:
            measured = len(actual[0])
            if measured != settings.embedding_dimension:
                logger.warning(
                    "Embedding dimension from API is %d, config default was %d. "
                    "Using measured value.", measured, settings.embedding_dimension,
                )
        embeddings.extend(actual)
        logger.info("Embedded %d / %d chunks", min(i + BATCH_SIZE, len(texts)), len(texts))

    measured_dim = len(embeddings[0]) if embeddings else settings.embedding_dimension

    # 3. Create the collection (drop first if requested).
    create_collection(vector_size=measured_dim, recreate=recreate)

    # 4. Build points with deterministic IDs and upsert.
    points = build_points(all_chunks, embeddings)
    count = upsert_points(points)
    logger.info("Ingestion complete: %d points in collection '%s'",
                count, settings.collection_name)
    return count


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ingest OpsRAG synthetic data into Qdrant."
    )
    parser.add_argument(
        "--recreate-collection", "--recreate",
        dest="recreate", action="store_true",
        help="Drop and recreate the collection before ingesting.",
    )
    args = parser.parse_args()

    count = asyncio.run(run_ingestion(recreate=args.recreate))
    print(f"Done. {count} points upserted into '{settings.collection_name}'.")


def _format_defect_entry(d: Dict[str, Any]) -> str:
    """Format a single defect log entry as readable text."""
    parts = [
        f"Defect ID: {d.get('defect_id', 'N/A')}",
        f"Date: {d.get('date', 'N/A')}",
        f"Line: {d.get('line', 'N/A')}",
        f"Shift: {d.get('shift', 'N/A')}",
        f"Product: {d.get('product', 'N/A')}",
        f"Defect Type: {d.get('defect_type', 'N/A')}",
        f"Defect Code: {d.get('defect_code', 'N/A')}",
        f"Component: {d.get('component_reference', 'N/A')}",
        f"Quantity Affected: {d.get('quantity_affected', 'N/A')}",
        f"Detected By: {d.get('detected_by', 'N/A')}",
        f"Root Cause: {d.get('root_cause', 'N/A')}",
        f"Corrective Action: {d.get('corrective_action', 'N/A')}",
        f"Disposition: {d.get('disposition', 'N/A')}",
        f"Rework Status: {d.get('rework_status', 'N/A')}",
        f"Operator: {d.get('operator_id', 'N/A')}",
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    main()
