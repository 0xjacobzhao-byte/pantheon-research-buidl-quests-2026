"""Five-model schema + cached-store tests (fail-closed, explicit states)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.llm_cached_store import load_case_overlays, load_cases
from app.llm_schema import LLMState


def test_cases_present():
    ids = {c["case_id"] for c in load_cases()}
    assert {"NVDA", "MA", "BTC"} <= ids


def test_every_case_has_five_overlays():
    for case in load_cases():
        bundle = load_case_overlays(case["case_id"])
        assert bundle is not None
        assert len(bundle["overlays"]) == 5


def test_nvda_all_cached_and_carry_evidence_hash():
    bundle = load_case_overlays("NVDA")
    for o in bundle["overlays"]:
        assert o.data_state == LLMState.CACHED
        assert o.evidence_hash and o.evidence_hash.startswith("sha256:")


def test_btc_has_explicit_not_generated_state():
    bundle = load_case_overlays("BTC")
    states = {o.provider.value: o.data_state for o in bundle["overlays"]}
    # gemini is deliberately NOT_GENERATED — an explicit state, not a fabrication.
    assert states["gemini"] == LLMState.NOT_GENERATED
    not_gen = [o for o in bundle["overlays"] if o.data_state == LLMState.NOT_GENERATED][0]
    assert not_gen.business_quality is None
    assert not_gen.error_message


def test_missing_provider_is_explicit_not_fabricated():
    # A non-usable overlay must never carry a fabricated assessment.
    bundle = load_case_overlays("BTC")
    for o in bundle["overlays"]:
        if o.data_state not in (LLMState.CACHED, LLMState.AVAILABLE):
            assert o.business_quality is None
            assert o.confidence is None
