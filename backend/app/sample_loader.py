"""Load sample equity evidence and LLM output data from the data/ directory."""

from __future__ import annotations

import json
from pathlib import Path

from .models import EquityEvidence

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

SUPPORTED_TICKERS = ["MA", "NVDA"]


def _load_json(filename: str) -> dict:
    filepath = DATA_DIR / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Sample data file not found: {filepath}")
    with open(filepath, encoding="utf-8") as f:
        return json.load(f)


def list_available_tickers() -> list[str]:
    """Return supported demo tickers."""
    return SUPPORTED_TICKERS


def load_evidence(ticker: str) -> EquityEvidence:
    """Load sample equity evidence for a given ticker."""
    data = _load_json(f"sample_equity_evidence_{ticker.lower()}.json")
    return EquityEvidence(**data)


def load_qwen_sample(ticker: str) -> dict:
    """Load raw Qwen sample data for a ticker."""
    return _load_json(f"sample_qwen_output_{ticker.lower()}.json")


def load_deepseek_sample(ticker: str) -> dict:
    """Load raw DeepSeek sample data for a ticker."""
    return _load_json(f"sample_deepseek_output_{ticker.lower()}.json")
