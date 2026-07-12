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
