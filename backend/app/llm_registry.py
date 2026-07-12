"""Public-safe provider registry for the five-model cockpit.

Records the five providers with PUBLIC model family names only. No credentials,
no internal model IDs, no pricing tables. In the public repo every provider runs
in offline/cached mode by default — no live paid LLM call is ever made.
"""

from __future__ import annotations

import os
from typing import Any

from .llm_schema import PROVIDER_ORDER, LLMProvider

# Public model family names only (no internal registry IDs).
_REGISTRY: dict[LLMProvider, dict[str, Any]] = {
    LLMProvider.CLAUDE: {
        "display_name": "Claude",
        "model": "claude-3-5-sonnet",
        "family": "anthropic_claude",
        "credential_env": "ANTHROPIC_API_KEY",
        "default_runs_live": False,
    },
    LLMProvider.CHATGPT: {
        "display_name": "ChatGPT",
        "model": "gpt-4o",
        "family": "openai_chatgpt",
        "credential_env": "OPENAI_API_KEY",
        "default_runs_live": False,
    },
    LLMProvider.GEMINI: {
        "display_name": "Gemini",
        "model": "gemini-2.5-pro",
        "family": "google_gemini",
        "credential_env": "GEMINI_API_KEY",
        "default_runs_live": False,
    },
    LLMProvider.DEEPSEEK: {
        "display_name": "DeepSeek",
        "model": "deepseek-chat",
        "family": "deepseek",
        "credential_env": "DEEPSEEK_API_KEY",
        "default_runs_live": False,
    },
    LLMProvider.QWEN: {
        "display_name": "Qwen",
        "model": "qwen-plus",
        "family": "alibaba_qwen",
        "credential_env": "DASHSCOPE_API_KEY",
        "default_runs_live": False,
    },
}


def list_providers() -> list[dict[str, Any]]:
    """Return the five registered providers with public-safe metadata."""
    out = []
    for p in PROVIDER_ORDER:
        meta = _REGISTRY[p]
        out.append({
            "provider": p.value,
            "display_name": meta["display_name"],
            "model": meta["model"],
            "family": meta["family"],
            "credential_configured": bool(os.environ.get(meta["credential_env"])),
            "default_runs_live": meta["default_runs_live"],
            "mode": "offline_cached",
        })
    return out


def provider_meta(provider: LLMProvider) -> dict[str, Any]:
    return _REGISTRY[provider]


def registered_count() -> int:
    return len(_REGISTRY)
