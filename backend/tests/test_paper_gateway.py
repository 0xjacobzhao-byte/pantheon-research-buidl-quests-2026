"""Paper gateway tests: LIVE disabled, no broker, LLM cannot execute, audit."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import paper_gateway
from app.paper_gateway import models as pg_models
from app.paper_gateway.service import reset_service
from app.paper_gateway.provenance import compute_audit_hash, verify_audit_hash


def _svc():
    return reset_service()


def test_live_constants_disabled():
    assert pg_models.LIVE_ENABLED is False
    assert pg_models.BROKER_CONNECTED is False
    assert pg_models.REAL_ORDER_PATH is False
    assert pg_models.PAPER_ONLY is True


def test_no_broker_import_in_package():
    # The package must not import any broker/exchange SDK or call an order path.
    root = Path(paper_gateway.__file__).parent
    banned_imports = ("import ccxt", "from ccxt", "import okx", "binance.client",
                      "longport", "moomoo", "ibapi")
    banned_calls = (".place_order(", ".submit_order(", ".create_order(", ".send_order(")
    for py in root.glob("*.py"):
        text = py.read_text().lower()
        for token in banned_imports + banned_calls:
            assert token not in text, f"{py.name} references {token}"


def test_status_proves_paper_only():
    status = _svc().status()
    assert status.live_enabled is False
    assert status.broker_adapter_present is False
    assert status.llm_can_execute is False
    assert status.llm_can_approve is False
    assert status.human_approval_required is True


def test_llm_actor_cannot_execute_without_human_approval():
    svc = _svc()
    proof = svc.live_disabled_proof()
    assert proof["live_disabled"] is True
    assert proof["llm_actor_auto_executed_without_approval"] == 0


def test_approval_required_before_simulation():
    svc = _svc()
    intent = svc.create_intent({
        "intent_id": "t1", "ticker": "NVDA", "side": "buy", "quantity": 1, "notional_usd": 100,
        "provenance": {"source_module": "m", "validation_maturity": "MATURE", "actor_type": "llm"},
    })
    assert intent.state == pg_models.IntentState.AWAITING_APPROVAL
    # Simulating before approval must not fill.
    after = svc.simulate("t1")
    assert after.state == pg_models.IntentState.AWAITING_APPROVAL
    assert after.paper_fill is None
    # Approve (human) then simulate.
    svc.approve("t1", operator="pm")
    filled = svc.simulate("t1")
    assert filled.state == pg_models.IntentState.PAPER_FILLED
    assert filled.paper_fill.venue == "PAPER_SIMULATOR"
    assert filled.paper_fill.is_paper is True


def test_macro_hard_stop_rejected():
    svc = _svc()
    intent = svc.create_intent({
        "intent_id": "t2", "ticker": "MA", "side": "buy", "quantity": 1, "notional_usd": 100,
        "provenance": {"source_module": "m", "validation_maturity": "MATURE", "actor_type": "llm"},
        "risk_context": {"macro_hard_stop": True},
    })
    assert intent.state == pg_models.IntentState.RISK_REJECTED
    assert pg_models.RiskReason.MACRO_HARD_STOP in intent.rejection_reasons


def test_validation_not_ready_rejected():
    svc = _svc()
    intent = svc.create_intent({
        "intent_id": "t3", "ticker": "BTC", "side": "buy", "quantity": 1, "notional_usd": 100,
        "provenance": {"source_module": "m", "validation_maturity": "SIGNAL_ONLY", "actor_type": "llm"},
    })
    assert pg_models.RiskReason.VALIDATION_NOT_READY in intent.rejection_reasons


def test_provenance_missing_fails_closed():
    svc = _svc()
    intent = svc.create_intent({
        "intent_id": "t4", "ticker": "NVDA", "side": "buy", "quantity": 1, "notional_usd": 100,
        "provenance": {"source_module": "", "validation_maturity": "MATURE", "actor_type": "llm",
                       "actor_identity": ""},
    })
    assert pg_models.RiskReason.PROVENANCE_MISSING in intent.rejection_reasons


def test_bad_audit_hash_blocked():
    svc = _svc()
    intent = svc.create_intent({
        "intent_id": "t5", "ticker": "NVDA", "side": "buy", "quantity": 1, "notional_usd": 100,
        "provenance": {"source_module": "m", "validation_maturity": "MATURE", "actor_type": "llm"},
    })
    # Tamper with a hash-committed field after stamping.
    intent.quantity = 999
    assert verify_audit_hash(intent) is False


def test_audit_chain_is_append_only_and_intact():
    svc = _svc()
    report = svc.provenance_completeness_report()
    assert report["audit_chain_intact"] is True
