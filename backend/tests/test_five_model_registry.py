"""Five-model registry + provider status tests."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.llm_registry import list_providers, registered_count
from app.llm_provider_status import get_provider_status
from app.llm_schema import PROVIDER_ORDER, LLMProvider


def test_exactly_five_providers():
    assert registered_count() == 5
    assert len(list_providers()) == 5
    assert len(PROVIDER_ORDER) == 5


def test_all_five_providers_present():
    names = {p["provider"] for p in list_providers()}
    assert names == {"claude", "chatgpt", "gemini", "deepseek", "qwen"}


def test_providers_offline_by_default():
    for p in list_providers():
        assert p["default_runs_live"] is False
        assert p["mode"] == "offline_cached"


def test_provider_status_covers_all_cases():
    status = get_provider_status()
    assert status["registered_providers"] == 5
    # Every provider appears in the coverage map.
    for p in LLMProvider:
        assert p.value in status["case_coverage"]
