"""Fail-closed guarantees for the Qwen overlay.

A missing credential must BLOCK (never a hollow SUCCESS); a non-JSON model
response must surface as PARSE_ERROR; offline mode must serve bundled samples.
"""

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import qwen_overlay
from app.models import OverlayStatus
from app.sample_loader import load_evidence


@pytest.mark.asyncio
async def test_missing_credential_fails_closed(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "live")
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("QWEN_API_KEY", raising=False)

    overlay = await qwen_overlay.run_qwen_overlay(load_evidence("MA"))
    assert overlay.status == OverlayStatus.BLOCKED_BY_MISSING_CREDENTIAL
    assert overlay.assessment is None
    assert overlay.error_message and "blocked" in overlay.error_message.lower()


def test_invalid_json_raises_parse_error():
    with pytest.raises(ValueError):
        qwen_overlay._parse_json_response("definitely not json {")


def test_fenced_json_still_parses():
    out = qwen_overlay._parse_json_response('```json\n{"takeaway": "ok"}\n```')
    assert out["takeaway"] == "ok"


@pytest.mark.asyncio
async def test_offline_sample_works(monkeypatch):
    monkeypatch.setenv("DEMO_MODE", "offline")
    overlay = await qwen_overlay.run_qwen_overlay(load_evidence("NVDA"))
    assert overlay.status == OverlayStatus.OFFLINE_SAMPLE
    assert overlay.assessment is not None
    assert overlay.prompt_version and overlay.output_schema_version


def test_missing_sample_is_not_generated():
    # A ticker with no bundled sample must not silently succeed.
    overlay = qwen_overlay._load_sample_overlay("ZZZZ")
    assert overlay.status == OverlayStatus.QWEN_NOT_GENERATED
    assert overlay.assessment is None


def test_overlay_carries_prompt_and_schema_version():
    overlay = qwen_overlay._load_sample_overlay("MA")
    assert overlay.prompt_version == qwen_overlay.PROMPT_VERSION
    assert overlay.output_schema_version == qwen_overlay.OUTPUT_SCHEMA_VERSION
