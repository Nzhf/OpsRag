# OpsRAG — Manufacturing Operations RAG Assistant

A retrieval-augmented generation (RAG) assistant with **agentic tool-calling**, built for a fictional Penang-based electronics manufacturing site. Ask questions about SOP procedures, defect history, shift-handover notes, and inventory levels — and get answers with cited sources.

Built with **FastAPI** (Python), **Qdrant** (vector search), **Google Gemini** (embeddings), and **Groq** (LLM generation + tool-calling).

> The corpus is 100% synthetic, written to be internally consistent (same lines, shifts, products, and personnel across all document types) so retrieval demos look coherent. See [Limitations](#limitations).

---

## Architecture

```
                         ┌──────────────────────────────────────────┐
                         │              FastAPI app                 │
   Browser ── GET /  ──▶ │  static/index.html (chat UI, RAG/Agent)  │
                         │                                          │
        POST /chat/query │  ┌────────────┐   ┌───────────────────┐  │
   ────────────────────▶ │  │ embeddings │──▶│ retrieval (Qdrant │  │
        POST /chat/agent │  │  (Gemini)  │   │  vector search)   │  │
   ────────────────────▶ │  └────────────┘   └─────────┬─────────┘  │
                         │                             │ context    │
                         │  ┌────────────┐   ┌─────────▼─────────┐  │
                         │  │generation  │◀──│ context builder   │  │
                         │  │  (Groq)    │   └───────────────────┘  │
                         │  └────────────┘                          │
                         │        ▲  tool calls  ┌───────────────┐  │
                         │        └───────────────│ agent loop    │  │
                         │                        │ + 3 tools     │──┼──▶ inventory.json
                         └────────────────────────┴───────────────┘  └──▶ defect_log.json
                                            (lookup_sop ──▶ Qdrant)
```

**Two answer modes, deliberately separated:**

- **`/chat/query` (plain RAG):** embed question → vector search → build a token-budgeted context → LLM answers *only* from that context, citing documents. If nothing scores above the relevance threshold, a fixed fallback is returned instead of a hallucination.
- **`/chat/agent` (agentic):** the LLM receives three tool schemas and *decides* which to call. Each call is executed locally in Python, results are fed back into the conversation, and the model writes the final answer from real tool output.

## Project structure

```
app/
  main.py               FastAPI app, CORS, static mount, root route
  config.py             pydantic-settings (env-driven)
  core/
    qdrant_client.py    Qdrant client singleton, collection mgmt, vector search
    groq_client.py      Groq chat-completion wrapper (OpenAI-compatible)
  models/schemas.py     request/response Pydantic models
  routers/
    health.py           GET /health
    chat.py             POST /chat/query, POST /chat/agent
  services/
    embeddings.py       Gemini embedContent wrapper (async batching)
    retrieval.py        search + context assembly (score threshold, token budget)
    generation.py       grounded plain-RAG generation
    tools.py            3 tool schemas + implementations + TOOL_REGISTRY
    agent.py            tool-calling orchestration loop
scripts/
  ingest.py             Phase-2 pipeline: chunk → embed → upsert (re-runnable)
data/                   synthetic corpus (SOPs, defects, handovers, inventory)
static/index.html       minimal chat UI
tests/                  hermetic unit tests + opt-in integration test
```

## Quickstart

```bash
# 1. Clone and install
git clone https://github.com/Nzhf/opsrag.git
cd opsrag
python -m venv venv
venv\Scripts\activate          # Windows (source venv/bin/activate on Linux)
pip install -r requirements.txt

# 2. Configure keys
copy .env.example .env         # then edit .env with your real keys

# 3. Build the vector index (one-time, re-runnable)
python -m scripts.ingest --recreate-collection

# 4. Run the API + UI
uvicorn app.main:app --reload
# open http://localhost:8000
```

Requires Python 3.11+. Free-tier accounts at [Qdrant Cloud](https://cloud.qdrant.io), [Google AI Studio](https://aistudio.google.com/app/apikey), and [Groq Console](https://console.groq.com) are sufficient.

---

## Environment variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `QDRANT_URL` | ✅ | — | Qdrant Cloud cluster URL (or `http://qdrant:6333` for the compose local-Qdrant profile) |
| `QDRANT_API_KEY` | ✅ | — | Qdrant API key |
| `GEMINI_API_KEY` | ✅ | — | Google AI Studio key, used for `text-embedding-004` embeddings |
| `GROQ_API_KEY` | ✅ | — | Groq key, used for generation and tool-calling |
| `QDRANT_COLLECTION_NAME` | — | `opsrag_docs` | Target collection name |
| `GEMINI_EMBEDDING_MODEL` | — | `text-embedding-004` | Embedding model |
| `GROQ_MODEL` | — | `llama-3.3-70b-versatile` | Groq model. Groq rotates its lineup — verify the current tool-use-capable model at [console.groq.com/docs/tool-use](https://console.groq.com/docs/tool-use) |

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness check |
| `POST` | `/chat/query` | Plain RAG: retrieve + grounded answer with cited sources |
| `POST` | `/chat/agent` | Agentic: model picks and calls tools, answers from tool output |
| `GET` | `/` | Chat UI |
| `GET` | `/docs` | OpenAPI/Swagger docs |

## Example queries

**RAG mode — SOP question** (`POST /chat/query`):

```json
// Request
{ "question": "What are the wrist strap requirements before handling PCBs?" }

// Response (abridged)
{
  "answer": "Before handling PCBs you must place the conductive band snugly
             against bare skin and connect the coiled cord to the common
             point ground terminal BEFORE touching ESD-sensitive items.
             Test the wrist strap at the station entrance at the start of
             each shift and after breaks... (002-esd-handling-pcb-assembly.md)",
  "sources": [
    { "doc_type": "sop", "source_file": "002-esd-handling-pcb-assembly.md",
      "excerpt": "Place conductive band snugly against bare skin...", "score": 0.83 }
  ]
}
```

**RAG mode — off-topic question:** returns the fixed fallback (`"I don't have enough information in my knowledge base..."`) with no sources — no hallucinated filler.

**Agent mode — inventory** (`POST /chat/agent`):

```json
// Request
{ "question": "how much solder paste do we have left?" }

// Response (abridged)
{
  "answer": "We currently have 45 jars of Solder Paste SAC305 Type 4 on hand
             against a reorder threshold of 20 — stock level is OK.",
  "tool_calls": [
    { "name": "check_inventory_status",
      "arguments": { "item": "solder paste" },
      "result": { "quantity_on_hand": 45, "reorder_threshold": 20, "status": "ok" } }
  ],
  "sources": [ { "doc_type": "inventory", "source_file": "inventory_snapshot_august_2026.json", ... } ]
}
```

**Agent mode — defect summary:**

```json
{ "question": "summarize this week's defects" }
// → model calls summarize_defect_log("last 7 days"), then writes a
//   natural-language summary from the returned counts-by-type/line.
```

*(Sample outputs are illustrative; exact wording varies per model run.)*

---

## How the agentic tool-calling works (plain language)

In plain RAG mode, every question takes the same path: search the vector database, assemble the retrieved text into a prompt, generate an answer. That works well for document questions, but it cannot answer "how many 4.7k resistors do we have?" — that answer is not buried in a paragraph of prose, it lives in a structured inventory file.

Agent mode reverses who makes the decisions. OpsRAG gives the model three tool definitions — JSON schemas describing an SOP lookup, an inventory check, and a defect-log summarizer — and lets the model choose how to answer (`tool_choice="auto"`). The model never executes anything itself. Instead, it replies with a structured *request*: "call `check_inventory_status` with the argument `solder paste`."

The orchestration loop in `app/services/agent.py` parses that request, looks the function up in a Python `TOOL_REGISTRY` dict, and executes it. Each tool runs locally in Python:

- `lookup_sop` performs a vector search filtered to `doc_type == "sop"` — appropriate for semantic "how do we do X?" questions.
- `check_inventory_status` skips vector search entirely and matches against the inventory JSON using exact, substring, and fuzzy matching — appropriate because stock levels are exact facts, not semantics.
- `summarize_defect_log` parses a natural-language date range and aggregates the defect log by type, line, and shift.

The tool's result is appended back into the conversation as a `role="tool"` message, and Groq is called a second time — now with the tool output in context — to write the final natural-language answer. If the model decides no tool is needed, it simply answers directly.

The key design property is separation of concerns: the model is the *decision-maker*, the Python services are the *hands*. The LLM never invents a stock number — it can only relay what a tool actually returned, and if the tool says "not found," the answer says so. And because `/chat/agent` returns the list of tool calls alongside the answer, the UI can display exactly which tools fired and with what arguments: the reasoning chain is inspectable, not hidden.

## Tests

```bash
pytest                        # hermetic unit tests (no keys needed)
OPSRAG_RUN_INTEGRATION=1 pytest tests/test_retrieval.py
                              # hits real Gemini + ingested Qdrant; run after ingesting
```

- `tests/test_tools.py` — inventory status classification (ok / low / critical boundaries), item-ID matching, not-found handling, and date-range parsing for the defect summarizer, against known fixtures.
- `tests/test_retrieval.py` — opt-in integration: verifies `retrieval.search()` returns non-empty, correctly score-ordered results for a query matching known ingested content, and that the `doc_type` filter is respected.

## Deployment (Railway)

1. Push this repo to GitHub (done — Railway deploys from the repo).
2. Create a new project → *Deploy from GitHub repo* → select `opsrag`.
3. Railway auto-detects the `Dockerfile`; no build config needed.
4. Set these variables in the Railway dashboard (**Variables** tab):

   | Variable | Value |
   |---|---|
   | `QDRANT_URL` | your Qdrant Cloud URL |
   | `QDRANT_API_KEY` | your Qdrant key |
   | `GEMINI_API_KEY` | your Google AI Studio key |
   | `GROQ_API_KEY` | your Groq key |
   | `GROQ_MODEL` | current tool-use model from Groq docs |

5. Generate a public domain under **Settings → Networking**.
6. Ingest once from your machine against the same Qdrant Cloud cluster (`python -m scripts.ingest --recreate-collection`) — the container itself only needs to serve queries.

## Screenshots

*(placeholders — replace with actual captures)*

- ![Chat UI — RAG mode with cited sources](docs/screenshot-rag-mode.png)
- ![Chat UI — Agent mode showing tool-call chips](docs/screenshot-agent-mode.png)
- ![Container running on Railway](docs/screenshot-railway.png)

## Limitations

- **The corpus is fully synthetic.** Documents were authored for this project to be internally consistent (shared line names, shifts, products, personnel, and a coherent August 2026 timeline) — but they are not real BizLink/Jabil operational data.
- **Retrieval quality is demo-scale.** One Qdrant collection, no hybrid search, no reranker, and a fixed 0.5 cosine threshold that was hand-tuned, not evaluated against a labeled query set.
- **Inventory/defect tools read static JSON snapshots**, not a live ERP. The inventory tool is deliberately *not* vector search — it's exact/substring/fuzzy matching over structured records.
- **The agent is single-turn.** Each request starts a fresh conversation; there is no multi-turn memory or conversation store.
- **No auth, rate limiting, or streaming.** This is a portfolio-scale demo, deliberately thin outside the RAG/agent core.