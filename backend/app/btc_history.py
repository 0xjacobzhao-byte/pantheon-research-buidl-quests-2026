"""BTC weekly layer-signal history loader (bundled, public-safe)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "btc"


def load_weekly_history() -> list[dict]:
    path = DATA_DIR / "history_weekly.json"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_history(limit: Optional[int] = None) -> dict[str, Any]:
    rows = load_weekly_history()
    if limit is not None:
        rows = rows[-limit:]
    # Honest coverage: report per-layer quality distribution.
    def _dist(field: str) -> dict[str, int]:
        out: dict[str, int] = {}
        for r in rows:
            v = r.get(field, "MISSING")
            out[v] = out.get(v, 0) + 1
        return out

    return {
        "cadence": "weekly",
        "count": len(rows),
        "first": rows[0]["date"] if rows else None,
        "last": rows[-1]["date"] if rows else None,
        "rows": rows,
        "l1_quality_distribution": _dist("l1_quality"),
        "l3_state_distribution": _dist("risk_radar_state"),
        "disclaimer": (
            "Reconstructed weekly history for demonstration. Values are bundled "
            "illustrative samples; some layers are reconstructed, not native, and "
            "are labelled per row. Not trading advice."
        ),
    }
