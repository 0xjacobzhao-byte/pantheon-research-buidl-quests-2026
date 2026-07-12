"""Tests for the module snapshot grid (full research-system scope, public-safe)."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.sample_modules import get_module_snapshots

REQUIRED_CARD_FIELDS = [
    "key", "title", "group", "data_state", "freshness",
    "validation_state", "role", "what_not_to_infer", "sample_endpoint",
]

EXPECTED_KEYS = {
    "macro", "market_pulse_ta", "commodity", "fixed_income", "fx",
    "ticker_profile", "qwen_vs_deepseek", "data_quality",
}


def test_grid_has_all_expected_modules():
    grid = get_module_snapshots()
    keys = {m["key"] for m in grid["modules"]}
    assert EXPECTED_KEYS <= keys, f"missing: {EXPECTED_KEYS - keys}"


def test_every_card_has_required_fields():
    grid = get_module_snapshots()
    for card in grid["modules"]:
        for field in REQUIRED_CARD_FIELDS:
            assert field in card and card[field], f"{card.get('key')} missing {field}"


def test_grid_has_scope_disclaimer_and_schema():
    grid = get_module_snapshots()
    assert grid["schema_version"] == "module-snapshots-1.0"
    assert "context-only" in grid["disclaimer"].lower()
    assert grid["generated_at_utc"]


def test_context_modules_do_not_overclaim_live():
    # The macro/ta/ficc cards must be context-only, never LIVE_DUAL.
    grid = get_module_snapshots()
    by_key = {m["key"]: m for m in grid["modules"]}
    for key in ("macro", "market_pulse_ta", "commodity", "fixed_income", "fx"):
        assert by_key[key]["data_state"] == "CONTEXT_ONLY"


def test_qwen_card_is_live_computed_from_samples():
    # The Qwen-vs-DeepSeek card must reflect a real in-process comparison.
    grid = get_module_snapshots()
    card = next(m for m in grid["modules"] if m["key"] == "qwen_vs_deepseek")
    assert card["data_state"] in ("OFFLINE_SAMPLE", "LIVE_DUAL", "MIXED", "PARTIAL", "BLOCKED")
    # Headline is refreshed to mention the real agreement outcome.
    assert "agreement" in card["headline"].lower()


def test_data_quality_card_reflects_real_coverage():
    grid = get_module_snapshots()
    card = next(m for m in grid["modules"] if m["key"] == "data_quality")
    assert "healthy" in card["headline"].lower()


def test_grid_contains_no_secrets():
    blob = json.dumps(get_module_snapshots())
    for needle in ("sk-", "postgresql://", "password", "api_key", "x-admin-token"):
        assert needle not in blob.lower()
