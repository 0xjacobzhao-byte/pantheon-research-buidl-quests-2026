"""Paper fill simulator — deterministic, offline, never a broker.

Produces a *simulated* fill for an APPROVED intent. There is no network call,
no broker adapter, and no real-order path. The venue is always
``PAPER_SIMULATOR`` and ``is_paper`` is always True.
"""

from __future__ import annotations

import hashlib

from .models import PaperFill, PaperIntent

# Illustrative modeled slippage band (bps). Deterministic per intent so the demo
# is reproducible.
_MIN_SLIPPAGE_BPS = 1.0
_MAX_SLIPPAGE_BPS = 8.0


def _deterministic_slippage_bps(intent_id: str) -> float:
    """A stable pseudo-slippage derived from the intent id (no randomness)."""
    h = int(hashlib.sha256(intent_id.encode("utf-8")).hexdigest(), 16)
    span = _MAX_SLIPPAGE_BPS - _MIN_SLIPPAGE_BPS
    return round(_MIN_SLIPPAGE_BPS + (h % 1000) / 1000.0 * span, 2)


def simulate_fill(intent: PaperIntent, at: str) -> PaperFill:
    """Simulate a paper fill for an approved intent."""
    ref_price = intent.limit_price if intent.limit_price is not None else 100.0
    slippage_bps = _deterministic_slippage_bps(intent.intent_id)
    # Buys fill slightly above ref, sells slightly below — modeled slippage only.
    direction = 1.0 if intent.side.value == "buy" else -1.0
    fill_price = round(ref_price * (1.0 + direction * slippage_bps / 10_000.0), 4)
    return PaperFill(
        fill_id=f"paperfill_{intent.intent_id}",
        intent_id=intent.intent_id,
        filled_quantity=intent.quantity,
        fill_price=fill_price,
        slippage_bps=slippage_bps,
        venue="PAPER_SIMULATOR",
        is_paper=True,
        filled_at=at,
    )
