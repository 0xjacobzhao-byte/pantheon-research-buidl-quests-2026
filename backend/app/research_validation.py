"""Research Ops — validation policy view (PIT / record-kind / eligibility)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "research_ops"


def get_validation() -> dict[str, Any]:
    path = DATA_DIR / "validation.json"
    if not path.exists():
        return {"modules": []}
    with open(path, encoding="utf-8") as f:
        return json.load(f)
