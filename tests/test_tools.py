"""Phase 8 unit tests: confirm check_inventory_status() correctly
categorizes ok / low / critical given known inventory fixtures, and
that summarize_defect_log() parses date ranges sensibly.

These are hermetic: no network, no real API keys (conftest.py injects
placeholders). The real inventory/defect data files ARE used for the
summarize tests since they ship with the repo.
"""
import asyncio
import pytest

from app.services import tools


SAMPLE_INVENTORY = [
    {
        "item_id": "TEST-001",
        "description": "Solder Paste SAC305 Type 4",
        "quantity_on_hand": 500,          # >= threshold  -> ok
        "reorder_threshold": 100,
        "unit_of_measure": "jars",
    },
    {
        "item_id": "TEST-002",
        "description": "Resistor 4.7k 1% 0402",
        "quantity_on_hand": 600,          # >= 50% but < threshold -> low
        "reorder_threshold": 1000,
        "unit_of_measure": "pieces",
    },
    {
        "item_id": "TEST-003",
        "description": "MCU STM32F407VGT6",
        "quantity_on_hand": 200,          # < 50% of threshold -> critical
        "reorder_threshold": 1000,
        "unit_of_measure": "pieces",
    },
]


@pytest.fixture
def patch_inventory(monkeypatch):
    """Swap the real inventory loader for a known fixture set."""
    monkeypatch.setattr(tools, "_load_inventory", lambda: SAMPLE_INVENTORY)


# --- _classify_status ------------------------------------------------------

def test_classify_ok():
    assert tools._classify_status(100, 50) == "ok"


def test_classify_low():
    # 30 is below the threshold of 50 but at/above half of it.
    assert tools._classify_status(30, 50) == "low"


def test_classify_critical():
    assert tools._classify_status(10, 50) == "critical"


def test_classify_exact_threshold_is_ok():
    assert tools._classify_status(50, 50) == "ok"


# --- check_inventory_status ------------------------------------------------

def test_check_inventory_ok(patch_inventory):
    result = asyncio.run(tools.check_inventory_status("solder paste"))
    assert result["found"] is True
    assert result["status"] == "ok"
    assert result["quantity_on_hand"] == 500


def test_check_inventory_low(patch_inventory):
    result = asyncio.run(tools.check_inventory_status("4.7k resistor"))
    assert result["status"] == "low"


def test_check_inventory_critical(patch_inventory):
    result = asyncio.run(tools.check_inventory_status("STM32F407"))
    assert result["status"] == "critical"


def test_check_inventory_matches_item_id(patch_inventory):
    result = asyncio.run(tools.check_inventory_status("TEST-003"))
    assert result["item_id"] == "TEST-003"


def test_check_inventory_not_found(patch_inventory):
    result = asyncio.run(tools.check_inventory_status("unicorn tears"))
    assert result["found"] is False


# --- summarize_defect_log --------------------------------------------------

def test_summarize_full_month():
    result = asyncio.run(tools.summarize_defect_log("August 2026"))
    assert result["total_defects"] > 0
    assert result["by_defect_type"]
    assert result["by_line"]
    assert result["start_date"] == "2026-08-01"
    assert result["end_date"] == "2026-08-31"


def test_summarize_last_n_days():
    result = asyncio.run(tools.summarize_defect_log("last 7 days"))
    assert result["total_defects"] >= 0
    # Window must end on the most recent defect date in the log.
    assert result["end_date"] == "2026-08-30"


def test_summarize_explicit_range():
    result = asyncio.run(tools.summarize_defect_log("2026-08-01 to 2026-08-07"))
    assert result["total_defects"] > 0
    assert all(
        "2026-08-01" <= e["date"] <= "2026-08-07"
        for e in result["sample_entries"]
    )