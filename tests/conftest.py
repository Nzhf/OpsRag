"""Shared pytest configuration.

Sets placeholder env vars BEFORE any app import so unit tests run
hermetically (app.config instantiates Settings at import time and
requires these keys). Real values in a local .env take precedence,
which is exactly what the integration test wants.
"""
import os
import sys
from pathlib import Path

# Make the project root importable regardless of how pytest is invoked.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

for _var, _val in {
    "QDRANT_URL": "http://localhost:6333",
    "QDRANT_API_KEY": "test-key",
    "GEMINI_API_KEY": "test-key",
    "GROQ_API_KEY": "test-key",
}.items():
    os.environ.setdefault(_var, _val)