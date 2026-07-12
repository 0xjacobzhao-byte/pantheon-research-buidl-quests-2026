"""Loader for bundled macro snapshots (current, history, scenarios)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "macro"


def _load(name: str, default: Any) -> Any:
    path = DATA_DIR / name
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_current_snapshot() -> dict:
    return _load("current_snapshot.json", {})


def load_history() -> list[dict]:
    return _load("history.json", [])


def load_scenarios() -> dict:
    return _load("scenarios.json", {})
