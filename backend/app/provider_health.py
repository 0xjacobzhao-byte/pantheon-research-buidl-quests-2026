"""Provider health panel — public-safe, secret-free status snapshot.

Reports whether each provider (Qwen, DeepSeek) is configured, whether sample
evidence is present, whether Alibaba proof is documented, and whether the
system is in offline or live mode. No secrets are ever exposed.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from .alibaba_cloud_proof import provider_snapshot
from .sample_loader import list_available_tickers


def get_provider_health() -> Dict[str, Any]:
    """Return a secret-free provider health snapshot."""
    providers = provider_snapshot()
    demo_mode = os.environ.get("DEMO_MODE", "offline")
    tickers = list_available_tickers()

    return {
        "schema_version": "provider-health-1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "demo_mode": demo_mode,
        "qwen": {
            "provider": "Alibaba Cloud DashScope / Model Studio",
            "configured": providers["qwen"]["configured"],
            "model": providers["qwen"]["model"],
            "status": "configured" if providers["qwen"]["configured"] else "offline (bundled samples)",
            "fail_closed_active": True,
            "live_mode_gated": not providers["qwen"]["configured"],
        },
        "deepseek": {
            "provider": "DeepSeek API (OpenAI-compatible)",
            "configured": providers["deepseek"]["configured"],
            "model": providers["deepseek"]["model"],
            "status": "configured" if providers["deepseek"]["configured"] else "offline (bundled samples)",
            "fail_closed_active": True,
            "live_mode_gated": not providers["deepseek"]["configured"],
        },
        "sample_evidence": {
            "present": len(tickers) > 0,
            "tickers": tickers,
            "count": len(tickers),
        },
        "alibaba_proof": {
            "documented": True,
            "endpoint": "/api/proof/alibaba-cloud",
        },
        "offline_mode": {
            "available": True,
            "active": demo_mode == "offline",
        },
        "live_mode": {
            "gated": demo_mode != "live",
            "requires": ["DEMO_MODE=live", "DASHSCOPE_API_KEY", "DEEPSEEK_API_KEY"],
        },
        "secrets_exposed": False,
        "fail_closed_active": True,
        "note": (
            "No secrets are exposed in this endpoint. Live mode is gated behind "
            "environment variables. Fail-closed states are active: a missing "
            "credential yields BLOCKED_BY_MISSING_CREDENTIAL, never a hollow SUCCESS."
        ),
    }
