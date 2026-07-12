"""Research Ops — outcome maturity view.

Every performance field is null with an explicit reason unless a module has
genuinely matured, eligible outcomes. Sample counts and record kinds are
preserved; returns/Sharpe/hit-rate are never invented.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "research_ops"


def get_outcomes() -> dict[str, Any]:
    path = DATA_DIR / "outcomes.json"
    if not path.exists():
        return {"modules": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)
