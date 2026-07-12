"""Research Ops tests: null performance, eligibility, record kinds, PIT policy."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.research_ops import get_readiness, get_summary
from app.research_validation import get_validation
from app.research_outcomes import get_outcomes

EXPECTED_MODULES = {
    "btc", "eth", "macro", "us-stock", "cn-stock", "hk-stock", "sg-stock",
    "commodity", "fi", "forex", "defi", "narrative", "guru-council", "ta",
}


def test_all_modules_present():
    modules = {m["module"] for m in get_readiness()["modules"]}
    assert EXPECTED_MODULES <= modules


def test_no_alpha_claim_present():
    assert "No alpha" in get_readiness()["no_alpha_claim"]
    assert "No alpha" in get_summary()["no_alpha_claim"]


def test_performance_is_null_with_reason():
    for o in get_outcomes()["modules"]:
        perf = o["performance"]
        assert perf["hit_rate"] is None
        assert perf["avg_return_pct"] is None
        assert perf["sharpe"] is None
        assert perf["reason"]


def test_public_eligibility_explicit():
    modules = {m["module"]: m for m in get_readiness()["modules"]}
    # btc/eth are the eligible live modules.
    assert modules["btc"]["public_performance_eligible"] is True
    assert modules["eth"]["public_performance_eligible"] is True
    # validation-only equities are explicitly NOT eligible.
    assert modules["us-stock"]["public_performance_eligible"] is False


def test_pit_policy_values_valid():
    valid = {"PIT", "MIXED", "REVISED"}
    for m in get_readiness()["modules"]:
        assert m["pit_policy"] in valid


def test_record_kinds_preserved():
    kinds = {m["record_kind"] for m in get_readiness()["modules"]}
    assert {"live", "validation_only", "reconstructed", "signal_only", "warming_up"} & kinds


def test_summary_reports_zero_public_performance():
    # No module should publish performance in the public demo.
    assert get_summary()["modules_with_public_performance"] == 0


def test_validation_view_covers_all_modules():
    assert len(get_validation()["modules"]) == len(get_readiness()["modules"])
