"""Context-only mini panels: Macro, Market Pulse (TA), FICC.

Public-safe, sample-backed, stale-safe panels that show the *shape* of Pantheon
Research's multi-asset context without exposing any proprietary engine, live
feed, or secret. Each panel:

- Is clearly marked CONTEXT_ONLY / illustrative
- Carries a stale-safe timestamp so no false freshness is implied
- Includes "no investment advice" disclosure
- Never makes a trade recommendation
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict


_DISCLAIMER = (
    "Context-only illustrative data. Not investment advice. No trade "
    "recommendation. Stale-safe: values are bundled samples, not live feeds."
)


def get_macro_mini_panel() -> Dict[str, Any]:
    """Macro regime mini panel — context-only, no live feed."""
    return {
        "schema_version": "macro-mini-1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_state": "CONTEXT_ONLY",
        "disclaimer": _DISCLAIMER,
        "regime": {
            "growth": "Late-cycle / disinflationary",
            "inflation": "Cooling — core PCE trending down (illustrative)",
            "liquidity": "Neutral-to-accommodative",
            "policy": "Fed on hold; market pricing cuts (illustrative)",
        },
        "indicators": [
            {"name": "PMI Composite", "value": "51.2", "signal": "neutral", "note": "illustrative"},
            {"name": "CPI YoY", "value": "2.8%", "signal": "cooling", "note": "illustrative"},
            {"name": "Yield Curve (10Y-2Y)", "value": "+15bp", "signal": "normalizing", "note": "illustrative"},
            {"name": "VIX", "value": "14.5", "signal": "low", "note": "illustrative"},
        ],
        "headline": "Regime: Late-cycle / disinflationary (illustrative)",
        "what_not_to_infer": (
            "This is not a live macro nowcast. Values are bundled illustrative "
            "samples, not the production regime model output."
        ),
    }


def get_market_pulse_mini_panel() -> Dict[str, Any]:
    """Market Pulse / TA mini panel — context-only, no trade signal."""
    return {
        "schema_version": "market-pulse-mini-1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_state": "CONTEXT_ONLY",
        "disclaimer": _DISCLAIMER,
        "market": {
            "trend": "Mixed — large-cap uptrend, small-cap range-bound (illustrative)",
            "breadth": "Neutral — advance/decline balanced (illustrative)",
            "momentum": "Cooling — RSI divergence on S&P (illustrative)",
            "sentiment": "Mildly bullish — put/call ratio declining (illustrative)",
        },
        "indicators": [
            {"name": "S&P 500 50d MA", "value": "above", "signal": "bullish", "note": "illustrative"},
            {"name": "NYSE Breadth", "value": "52% advancing", "signal": "neutral", "note": "illustrative"},
            {"name": "RSI (14) S&P", "value": "58", "signal": "neutral-to-strong", "note": "illustrative"},
            {"name": "AAII Bull %", "value": "42%", "signal": "mildly bullish", "note": "illustrative"},
        ],
        "headline": "Breadth neutral, momentum cooling (illustrative)",
        "what_not_to_infer": (
            "Not a trading signal. TA context only for names inside the "
            "production universe. No buy/sell recommendation."
        ),
    }


def get_ficc_mini_panel() -> Dict[str, Any]:
    """FICC (FI / FX / Commodity) mini panel — context-only, no position."""
    return {
        "schema_version": "ficc-mini-1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "data_state": "CONTEXT_ONLY",
        "disclaimer": _DISCLAIMER,
        "fixed_income": {
            "stance": "Duration: neutral-to-long bias (illustrative)",
            "curve": "Normalizing — 10Y-2Y positive (illustrative)",
            "credit": "Tight spreads — HY OAS ~300bp (illustrative)",
            "validation": "FORWARD_VALIDATION_PENDING",
        },
        "fx": {
            "stance": "USD bias: mild-strong (illustrative)",
            "carry": "SIGNAL_ONLY — forward outcome not yet joined",
            "dxy": "103.5 (illustrative)",
            "validation": "SIGNAL_ONLY",
        },
        "commodity": {
            "stance": "Energy: balanced; gold: bid on rate-cut expectations (illustrative)",
            "crude_wti": "$78/bbl (illustrative)",
            "gold": "$2,420/oz (illustrative)",
            "validation": "FORWARD_VALIDATION_PROSPECTIVE",
        },
        "headline": "FI neutral-long · FX USD mild-strong · Commodity balanced (illustrative)",
        "what_not_to_infer": (
            "No fair-value band is published. Stance is context, not a price "
            "target. Carry legs can be blocked upstream."
        ),
    }
