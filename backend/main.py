"""FastAPI application — Pantheon Research (BUIDL_QUESTS 2026 public slice)."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.alibaba_cloud_proof import get_alibaba_proof, get_qwen_config
from app.comparison import run_comparison
from app.data_quality import get_data_quality_report
from app.evidence_pack import build_evidence_pack
from app.models import ProjectInfo
from app.qwen_overlay import run_qwen_overlay
from app.deepseek_overlay import run_deepseek_overlay
from app.sample_loader import list_available_tickers, load_evidence
from app.sample_modules import get_module_snapshots
from app.validation_stub import get_validation_methodology
from app.provider_health import get_provider_health
from app.ticker_profile import load_ticker_profile, list_profile_tickers
from app.validation_timeline import get_validation_timeline
from app.mini_panels import get_macro_mini_panel, get_market_pulse_mini_panel, get_ficc_mini_panel

# --- Full public migration modules ---
from app.llm_registry import list_providers as llm_list_providers
from app.llm_provider_status import get_provider_status as llm_provider_status
from app.llm_cockpit import (
    get_cases as llm_get_cases,
    get_case as llm_get_case,
    get_comparison as llm_get_comparison,
    get_agreement as llm_get_agreement,
)
from app.macro_risk_budget import extract_risk_budget
from app.macro_sample_loader import load_current_snapshot, load_history, load_scenarios
from app.research_ops import get_readiness as research_get_readiness, get_summary as research_get_summary
from app.research_validation import get_validation as research_get_validation
from app.research_outcomes import get_outcomes as research_get_outcomes
from app.data_platform.seed import get_store as dp_get_store
from app.data_platform.lineage import trace_evidence as dp_trace_evidence
from app.paper_gateway.service import get_service as pg_get_service
from app.btc_stack import get_stack as btc_get_stack, get_conflicts as btc_get_conflicts, get_current_posture as btc_get_posture
from app.btc_history import get_history as btc_get_history
from app.judge_demo import build_full_demo

load_dotenv()

DEMO_MODE = os.environ.get("DEMO_MODE", "offline")

app = FastAPI(
    title="Pantheon Research — BUIDL_QUESTS 2026",
    description="Dual-LLM equity qualitative overlay: Qwen Cloud vs DeepSeek",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Root & health
# ---------------------------------------------------------------------------

@app.get("/")
async def root():
    return {
        "project": "Pantheon Research — BUIDL_QUESTS 2026",
        "version": "1.0.0",
        "demo_mode": DEMO_MODE,
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "demo_mode": DEMO_MODE,
        "tickers": list_available_tickers(),
    }


# ---------------------------------------------------------------------------
# Project info
# ---------------------------------------------------------------------------

@app.get("/api/project")
async def project_info():
    info = ProjectInfo(demo_mode=DEMO_MODE)
    return info


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------

@app.get("/api/evidence/{ticker}")
async def get_evidence(ticker: str):
    try:
        evidence = load_evidence(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No evidence data for ticker: {ticker}")
    # Return the provenance-committed evidence pack (evidence + content hash).
    return build_evidence_pack(evidence)


# ---------------------------------------------------------------------------
# Overlays
# ---------------------------------------------------------------------------

@app.get("/api/overlay/qwen/{ticker}")
async def overlay_qwen(ticker: str):
    try:
        evidence = load_evidence(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No evidence data for ticker: {ticker}")
    overlay = await run_qwen_overlay(evidence)
    return overlay


@app.get("/api/overlay/deepseek/{ticker}")
async def overlay_deepseek(ticker: str):
    try:
        evidence = load_evidence(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No evidence data for ticker: {ticker}")
    overlay = await run_deepseek_overlay(evidence)
    return overlay


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

@app.get("/api/comparison/{ticker}")
async def get_comparison(ticker: str):
    try:
        evidence = load_evidence(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No evidence data for ticker: {ticker}")
    pack = build_evidence_pack(evidence)
    result = await run_comparison(
        evidence, evidence_hash=pack.provenance.evidence_hash
    )
    return result


# ---------------------------------------------------------------------------
# Demo flow
# ---------------------------------------------------------------------------

@app.get("/api/demo-flow")
async def demo_flow():
    return {
        "title": "Pantheon Research — Demo Flow",
        "steps": [
            {
                "step": 1,
                "title": "Select Ticker",
                "description": "Choose a demo ticker (MA or NVDA) from the ticker panel.",
            },
            {
                "step": 2,
                "title": "Load Evidence Pack",
                "description": "The backend loads structured quantitative evidence from data/*.json.",
            },
            {
                "step": 3,
                "title": "Qwen Cloud Overlay",
                "description": "Qwen Cloud (DashScope API) generates a qualitative overlay with 7 structured assessment fields.",
            },
            {
                "step": 4,
                "title": "DeepSeek Overlay",
                "description": "DeepSeek generates an independent qualitative overlay using the same evidence pack.",
            },
            {
                "step": 5,
                "title": "Model Comparison",
                "description": "The system compares both overlays: agreement score, tone classification, divergences, and evidence gaps.",
            },
            {
                "step": 6,
                "title": "Human Review Gate",
                "description": "If agreement is LOW or major divergences exist, human review is flagged. LLMs never execute trades.",
            },
        ],
        "architecture_layers": ["Strategy", "Information", "Signal", "Trading"],
        "safety_statement": (
            "Pantheon Research is not an autonomous trading bot. "
            "It is a framework-first, data-governed, human-in-the-loop "
            "AI research operating system."
        ),
    }


# ---------------------------------------------------------------------------
# Alibaba Cloud proof
# ---------------------------------------------------------------------------

@app.get("/api/proof/alibaba-cloud")
async def alibaba_cloud_proof():
    """Canonical deployment-proof path (matches the production backend)."""
    return get_alibaba_proof()


@app.get("/api/alibaba/proof")
async def alibaba_proof():
    """Back-compat alias for the deployment proof."""
    return get_alibaba_proof()


@app.get("/api/alibaba/qwen-config")
async def qwen_config():
    return get_qwen_config()


# ---------------------------------------------------------------------------
# Research-Ops mini: data quality & validation methodology
# ---------------------------------------------------------------------------

@app.get("/api/data-quality")
async def data_quality():
    """Public-safe Research-Ops / data-quality governance snapshot."""
    return get_data_quality_report()


@app.get("/api/validation")
async def validation():
    """Forward-validation methodology + clearly-labelled illustrative summary."""
    return get_validation_methodology()


@app.get("/api/modules")
async def modules():
    """Module snapshot grid — full research-system scope (context-only samples)."""
    return get_module_snapshots()


# ---------------------------------------------------------------------------
# Ticker profile (production-feel demo)
# ---------------------------------------------------------------------------

@app.get("/api/ticker-profile/{ticker}")
async def ticker_profile(ticker: str):
    """Production-feel ticker profile with KPI cards (sample-backed only)."""
    try:
        return load_ticker_profile(ticker)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No ticker profile for: {ticker}")


@app.get("/api/ticker-profiles")
async def ticker_profiles_list():
    """List available ticker profiles."""
    return {"tickers": list_profile_tickers()}


# ---------------------------------------------------------------------------
# Provider health
# ---------------------------------------------------------------------------

@app.get("/api/provider-health")
async def provider_health():
    """Public-safe provider health snapshot (no secrets)."""
    return get_provider_health()


# ---------------------------------------------------------------------------
# Validation timeline
# ---------------------------------------------------------------------------

@app.get("/api/validation-timeline")
async def validation_timeline():
    """Signal lifecycle timeline (illustrative, no alpha claims)."""
    return get_validation_timeline()


# ---------------------------------------------------------------------------
# Mini panels: Macro / Market Pulse / FICC
# ---------------------------------------------------------------------------

@app.get("/api/mini/macro")
async def mini_macro():
    """Macro regime mini panel (context-only, no live feed)."""
    return get_macro_mini_panel()


@app.get("/api/mini/market-pulse")
async def mini_market_pulse():
    """Market Pulse / TA mini panel (context-only, no trade signal)."""
    return get_market_pulse_mini_panel()


@app.get("/api/mini/ficc")
async def mini_ficc():
    """FICC mini panel (context-only, no position)."""
    return get_ficc_mini_panel()


# ===========================================================================
# P0-1 — Five-Model LLM Research Cockpit
# ===========================================================================

@app.get("/api/llm/providers")
async def llm_providers():
    """Public-safe registry of the five providers + provider status."""
    return {"providers": llm_list_providers(), "status": llm_provider_status()}


@app.get("/api/llm/cases")
async def llm_cases():
    return llm_get_cases()


@app.get("/api/llm/case/{case_id}")
async def llm_case(case_id: str):
    result = llm_get_case(case_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No LLM case: {case_id}")
    return result


@app.get("/api/llm/comparison/{case_id}")
async def llm_comparison(case_id: str):
    result = llm_get_comparison(case_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No LLM case: {case_id}")
    return result


@app.get("/api/llm/agreement/{case_id}")
async def llm_agreement(case_id: str):
    result = llm_get_agreement(case_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"No LLM case: {case_id}")
    return result


# ===========================================================================
# P0-2 — Macro Risk Budget
# ===========================================================================

@app.get("/api/macro/risk-budget")
async def macro_risk_budget():
    """Current deterministic macro risk budget (offline, fail-closed)."""
    return extract_risk_budget(load_current_snapshot(), load_history())


@app.get("/api/macro/history")
async def macro_history():
    """Historical risk budgets extracted from bundled snapshots."""
    history = load_history()
    out = []
    for i in range(len(history)):
        prior = history[:i]
        out.append(extract_risk_budget(history[i], prior))
    return {"count": len(out), "history": out}


@app.get("/api/macro/scenarios")
async def macro_scenarios():
    """Deterministic scenarios: valid / stress-hard-stop / stale / missing."""
    scenarios = load_scenarios().get("scenarios", [])
    history = load_history()
    return {
        "scenarios": [
            {
                "id": s["id"],
                "label": s.get("label", ""),
                "risk_budget": extract_risk_budget(s["snapshot"], history),
            }
            for s in scenarios
        ]
    }


# ===========================================================================
# P0-3 — Research Ops / Validation Console
# ===========================================================================

@app.get("/api/research-ops/readiness")
async def research_ops_readiness():
    return research_get_readiness()


@app.get("/api/research-ops/validation")
async def research_ops_validation():
    return research_get_validation()


@app.get("/api/research-ops/outcomes")
async def research_ops_outcomes():
    return research_get_outcomes()


@app.get("/api/research-ops/summary")
async def research_ops_summary():
    return research_get_summary()


# ===========================================================================
# P1-1 — Canonical Data Platform + Vintage Provenance
# ===========================================================================

@app.get("/api/data-platform/ingest-runs")
async def dp_ingest_runs():
    return {"ingest_runs": dp_get_store().ingest_runs()}


@app.get("/api/data-platform/provider-health")
async def dp_provider_health():
    return {"provider_health": dp_get_store().provider_health()}


@app.get("/api/data-platform/observations")
async def dp_observations(domain: str | None = None):
    return {"observations": dp_get_store().observations(domain)}


@app.get("/api/data-platform/observation/{observation_id}")
async def dp_observation(observation_id: int):
    obs = dp_get_store().observation(observation_id)
    if obs is None:
        raise HTTPException(status_code=404, detail=f"No observation: {observation_id}")
    return obs


@app.get("/api/data-platform/versions/{observation_id}")
async def dp_versions(observation_id: int):
    store = dp_get_store()
    if store.observation(observation_id) is None:
        raise HTTPException(status_code=404, detail=f"No observation: {observation_id}")
    return {"observation_id": observation_id, "versions": store.observation_versions(observation_id)}


@app.get("/api/data-platform/lineage/{evidence_hash}")
async def dp_lineage(evidence_hash: str):
    trace = dp_trace_evidence(dp_get_store(), evidence_hash)
    return trace.model_dump()


# ===========================================================================
# P1-2 — Paper / Shadow Trading Gateway (paper-only, LIVE disabled)
# ===========================================================================

@app.get("/api/paper-gateway/status")
async def pg_status():
    return pg_get_service().status().model_dump()


@app.get("/api/paper-gateway/provenance-completeness")
async def pg_provenance_completeness():
    return pg_get_service().provenance_completeness_report()


@app.get("/api/paper-gateway/audit")
async def pg_audit(intent_id: str | None = None):
    return {"events": pg_get_service().audit_events(intent_id)}


@app.get("/api/paper-gateway/live-disabled-proof")
async def pg_live_disabled():
    return pg_get_service().live_disabled_proof()


@app.get("/api/paper-gateway/intents")
async def pg_intents():
    return {"intents": [i.model_dump() for i in pg_get_service().list_intents()]}


@app.get("/api/paper-gateway/intent/{intent_id}")
async def pg_intent(intent_id: str):
    intent = pg_get_service().get(intent_id)
    if intent is None:
        raise HTTPException(status_code=404, detail=f"No intent: {intent_id}")
    card = pg_get_service().approval_card(intent_id)
    return {"intent": intent.model_dump(), "approval_card": card.model_dump() if card else None}


@app.post("/api/paper-gateway/intent")
async def pg_create_intent(payload: dict):
    intent = pg_get_service().create_intent(payload)
    return intent.model_dump()


@app.post("/api/paper-gateway/intent/{intent_id}/approve")
async def pg_approve(intent_id: str, payload: dict | None = None):
    svc = pg_get_service()
    if svc.get(intent_id) is None:
        raise HTTPException(status_code=404, detail=f"No intent: {intent_id}")
    operator = (payload or {}).get("operator", "operator_demo")
    return svc.approve(intent_id, operator=operator).model_dump()


@app.post("/api/paper-gateway/intent/{intent_id}/reject")
async def pg_reject(intent_id: str, payload: dict | None = None):
    svc = pg_get_service()
    if svc.get(intent_id) is None:
        raise HTTPException(status_code=404, detail=f"No intent: {intent_id}")
    payload = payload or {}
    return svc.reject(intent_id, operator=payload.get("operator", "operator_demo"),
                      note=payload.get("note", "")).model_dump()


@app.post("/api/paper-gateway/intent/{intent_id}/simulate")
async def pg_simulate(intent_id: str):
    svc = pg_get_service()
    if svc.get(intent_id) is None:
        raise HTTPException(status_code=404, detail=f"No intent: {intent_id}")
    return svc.simulate(intent_id).model_dump()


# ===========================================================================
# P1-3 — BTC Three-Layer Decision Stack
# ===========================================================================

@app.get("/api/btc/stack")
async def btc_stack():
    return btc_get_stack()


@app.get("/api/btc/history")
async def btc_history(limit: int | None = None):
    return btc_get_history(limit)


@app.get("/api/btc/conflicts")
async def btc_conflicts():
    return btc_get_conflicts()


@app.get("/api/btc/current-posture")
async def btc_current_posture():
    return btc_get_posture()


# ===========================================================================
# Unified judge demo flow
# ===========================================================================

@app.get("/api/judge/full-demo")
async def judge_full_demo():
    return build_full_demo()
