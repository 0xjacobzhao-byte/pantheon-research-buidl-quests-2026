"""Unified judge demo tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.judge_demo import build_full_demo


def test_full_demo_covers_all_modules():
    demo = build_full_demo()
    assert set(demo["modules"]) == {
        "five_model_llm_cockpit", "macro_risk_budget", "research_ops",
        "data_lineage", "paper_gateway", "btc_three_layer_stack",
    }


def test_full_demo_equity_flow_has_eleven_steps():
    demo = build_full_demo()
    assert len(demo["equity_flow"]) == 11
    assert all(s["status"] in ("ok", "error") for s in demo["equity_flow"])


def test_full_demo_btc_flow_ends_no_execution():
    demo = build_full_demo()
    last = demo["btc_flow"][-1]
    assert "No live order" in last["detail"] or "research-only" in last["detail"]


def test_full_demo_is_fail_safe():
    demo = build_full_demo()
    assert demo["safety"]["live_enabled"] is False
    assert demo["safety"]["llm_can_execute"] is False
    assert demo["safety"]["offline_first"] is True
