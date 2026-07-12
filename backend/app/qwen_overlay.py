"""Qwen Cloud (Alibaba Cloud DashScope) qualitative overlay integration.

Fail-closed by design: a missing credential, an HTTP error, or a non-JSON model
response each map to an explicit, distinct status — never a hollow SUCCESS with
empty fields. Offline mode (the default) serves bundled sample overlays so the
demo runs end-to-end with no secrets.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Optional

import httpx

from .models import (
    EquityEvidence,
    LLMProvider,
    OverlayAssessment,
    OverlayStatus,
    QualitativeOverlay,
    TokenUsage,
)

QWEN_BASE_URL = os.environ.get(
    "ALIBABA_MODELSTUDIO_BASE_URL",
    "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
)
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen-plus")

# Versioned so a judge (or a downstream diff) can tell which prompt/contract a
# stored overlay was produced under. Bump these when the prompt or output
# contract changes.
PROMPT_VERSION = "qwen-overlay-v1.1"
OUTPUT_SCHEMA_VERSION = "overlay-assessment-1.0"

# Bounded retry for transient upstream failures (never for auth/parse errors).
MAX_ATTEMPTS = int(os.environ.get("QWEN_MAX_ATTEMPTS", "3"))
BACKOFF_BASE_SECONDS = float(os.environ.get("QWEN_BACKOFF_BASE_SECONDS", "0.5"))

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"


def _check_credential() -> bool:
    return bool(os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("QWEN_API_KEY"))


def _api_key() -> Optional[str]:
    return os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("QWEN_API_KEY")


def _build_prompt(evidence: EquityEvidence) -> str:
    metrics = []
    if evidence.pe_ratio is not None:
        metrics.append(f"P/E (TTM): {evidence.pe_ratio}")
    if evidence.pb_ratio is not None:
        metrics.append(f"P/B: {evidence.pb_ratio}")
    if evidence.roic_pct is not None:
        metrics.append(f"ROIC: {evidence.roic_pct}%")
    if evidence.fcf_ttm_usd is not None:
        metrics.append(f"FCF (TTM): ${evidence.fcf_ttm_usd:,.0f}")
    if evidence.revenue_growth_yoy_pct is not None:
        metrics.append(f"Revenue Growth YoY: {evidence.revenue_growth_yoy_pct}%")
    if evidence.gross_margin_pct is not None:
        metrics.append(f"Gross Margin: {evidence.gross_margin_pct}%")
    if evidence.net_margin_pct is not None:
        metrics.append(f"Net Margin: {evidence.net_margin_pct}%")
    if evidence.debt_to_equity is not None:
        metrics.append(f"D/E: {evidence.debt_to_equity}")

    return f"""You are a senior equity research analyst. Based on the following quantitative evidence, produce a structured qualitative overlay for {evidence.company_name} ({evidence.ticker}).

Company: {evidence.company_name}
Ticker: {evidence.ticker}
Exchange: {evidence.exchange}
Sector: {evidence.sector}
Industry: {evidence.industry}
Market Cap: ${evidence.market_cap_usd:,.0f}
Summary: {evidence.summary}

Key Metrics:
{chr(10).join(metrics)}

Respond as JSON with these exact fields:
- takeaway: one-paragraph summary
- business_quality: assessment text
- moat: assessment text
- pricing_power: assessment text
- capital_allocation: assessment text
- red_flags: assessment text
- confidence: float 0-1
- missing_evidence: list of strings

Use professional financial language. Be concise but specific."""


def _blocked_overlay(ticker: str) -> QualitativeOverlay:
    return QualitativeOverlay(
        provider=LLMProvider.QWEN,
        model=QWEN_MODEL,
        ticker=ticker,
        status=OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL,
        error_message="DASHSCOPE_API_KEY is not set — live Qwen call blocked (fail-closed).",
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
    )


def _usage_from_response(data: dict) -> Optional[TokenUsage]:
    usage = data.get("usage")
    if not isinstance(usage, dict):
        return None
    return TokenUsage(
        prompt_tokens=usage.get("prompt_tokens"),
        completion_tokens=usage.get("completion_tokens"),
        total_tokens=usage.get("total_tokens"),
        # Cost is a placeholder — real per-model pricing lives in the private repo.
        estimated_cost_usd=None,
    )


async def run_qwen_overlay(
    evidence: EquityEvidence, demo_mode: bool = False
) -> QualitativeOverlay:
    """Run the Qwen Cloud qualitative overlay (fail-closed)."""
    if demo_mode or os.environ.get("DEMO_MODE", "offline") == "offline":
        return _load_sample_overlay(evidence.ticker)

    if not _check_credential():
        return _blocked_overlay(evidence.ticker)

    prompt = _build_prompt(evidence)
    api_key = _api_key()
    start = time.monotonic()
    last_error: Optional[str] = None

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(
                    f"{QWEN_BASE_URL}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": QWEN_MODEL,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                    },
                )
                resp.raise_for_status()

            data = resp.json()
            raw = data["choices"][0]["message"]["content"]
            latency_ms = int((time.monotonic() - start) * 1000)

            try:
                parsed = _parse_json_response(raw)
            except ValueError as parse_exc:
                # Non-JSON model output — never report SUCCESS with empty fields.
                # A parse failure is NOT retried (the model is answering, just
                # not in contract), so we surface it immediately.
                return QualitativeOverlay(
                    provider=LLMProvider.QWEN,
                    model=QWEN_MODEL,
                    ticker=evidence.ticker,
                    status=OverlayStatus.PARSE_ERROR,
                    error_message=f"Invalid JSON from model: {parse_exc}",
                    latency_ms=latency_ms,
                    attempts=attempt,
                    prompt_version=PROMPT_VERSION,
                    output_schema_version=OUTPUT_SCHEMA_VERSION,
                )

            assessment = OverlayAssessment(
                business_quality=parsed.get("business_quality", ""),
                moat=parsed.get("moat", ""),
                pricing_power=parsed.get("pricing_power", ""),
                capital_allocation=parsed.get("capital_allocation", ""),
                red_flags=parsed.get("red_flags", ""),
                confidence=float(parsed.get("confidence", 0.5)),
                missing_evidence=parsed.get("missing_evidence", []),
            )

            return QualitativeOverlay(
                provider=LLMProvider.QWEN,
                model=QWEN_MODEL,
                ticker=evidence.ticker,
                status=OverlayStatus.SUCCESS,
                takeaway=parsed.get("takeaway", ""),
                assessment=assessment,
                latency_ms=latency_ms,
                attempts=attempt,
                prompt_version=PROMPT_VERSION,
                output_schema_version=OUTPUT_SCHEMA_VERSION,
                usage=_usage_from_response(data),
            )

        except Exception as exc:  # noqa: BLE001 — surfaced as API_ERROR below
            last_error = str(exc)
            if attempt < MAX_ATTEMPTS:
                await asyncio.sleep(BACKOFF_BASE_SECONDS * (2 ** (attempt - 1)))
                continue

    latency_ms = int((time.monotonic() - start) * 1000)
    return QualitativeOverlay(
        provider=LLMProvider.QWEN,
        model=QWEN_MODEL,
        ticker=evidence.ticker,
        status=OverlayStatus.API_ERROR,
        error_message=last_error or "Unknown upstream error",
        latency_ms=latency_ms,
        attempts=MAX_ATTEMPTS,
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
    )


def _parse_json_response(raw: str) -> dict:
    """Parse a JSON response from the LLM, handling markdown fences."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        # Signal the failure instead of masking it as an empty dict — the caller
        # turns this into an explicit PARSE_ERROR overlay, never a hollow SUCCESS.
        raise ValueError(str(exc)) from exc


def _load_sample_overlay(ticker: str) -> QualitativeOverlay:
    """Load a pre-generated Qwen sample overlay from data/."""
    filepath = DATA_DIR / f"sample_qwen_output_{ticker.lower()}.json"
    if not filepath.exists():
        return QualitativeOverlay(
            provider=LLMProvider.QWEN,
            model=QWEN_MODEL,
            ticker=ticker,
            status=OverlayStatus.QWEN_NOT_GENERATED,
            error_message=f"No bundled Qwen sample for ticker: {ticker}",
            prompt_version=PROMPT_VERSION,
            output_schema_version=OUTPUT_SCHEMA_VERSION,
        )
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    assessment = OverlayAssessment(**data.get("assessment", {}))
    return QualitativeOverlay(
        provider=LLMProvider.QWEN,
        model=data.get("model", QWEN_MODEL),
        ticker=data.get("ticker", ticker),
        status=OverlayStatus.OFFLINE_SAMPLE,
        takeaway=data.get("takeaway", ""),
        assessment=assessment,
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
    )
