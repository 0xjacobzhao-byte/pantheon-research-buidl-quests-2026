"""Ticker profile loader — production-feel demo for NVDA and MA.

Loads pre-built ticker profiles from bundled JSON. Each profile contains KPI
cards (Valuation, Quality, Growth, Anchors, Technical), evidence pack summary,
and human-review status. No live data, no private DB queries.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_PROFILES_FILE = DATA_DIR / "ticker_profiles.json"

_cache: Optional[Dict[str, Any]] = None


def _load_all() -> Dict[str, Any]:
    global _cache
    if _cache is None:
        with open(_PROFILES_FILE, encoding="utf-8") as f:
            _cache = json.load(f)
    return _cache


def list_profile_tickers() -> list[str]:
    """Return tickers that have a profile."""
    data = _load_all()
    return [p["ticker"] for p in data.get("profiles", [])]


def load_ticker_profile(ticker: str) -> Dict[str, Any]:
    """Load a single ticker profile by ticker symbol."""
    data = _load_all()
    for p in data.get("profiles", []):
        if p["ticker"] == ticker:
            return p
    raise FileNotFoundError(f"No ticker profile for: {ticker}")
