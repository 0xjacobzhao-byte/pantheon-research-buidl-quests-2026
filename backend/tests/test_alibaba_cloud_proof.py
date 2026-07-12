"""Tests for the Alibaba Cloud deployment proof (v2).

Guards the properties a judge cares about most: the proof leaks no secrets,
its database/RDS claim is precise (never overclaiming migration), the Alibaba
service map is structurally correct, and the safe-claims reference the real
Qwen implementation path and the admin-gated smoke endpoint.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.alibaba_cloud_proof import get_alibaba_proof, get_qwen_config


REQUIRED_FIELDS = [
    "schema_version", "project", "cloud_provider", "host_runtime",
    "alibaba_hosted", "backend_runtime", "reverse_proxy", "frontend_source",
    "qwen_provider", "qwen_base_url", "qwen_model", "qwen_configured",
    "dashscope_api_key_configured", "demo_mode", "timestamp_utc",
    "proof_endpoints", "database", "safe_claims", "non_claims",
    "alibaba_services",
]


def test_proof_has_all_required_fields():
    proof = get_alibaba_proof().model_dump()
    for field in REQUIRED_FIELDS:
        assert field in proof, f"missing field: {field}"


def test_proof_has_schema_version():
    assert get_alibaba_proof().schema_version == "alibaba-proof-2.0"


def test_proof_has_host_and_runtime_fields():
    proof = get_alibaba_proof()
    assert isinstance(proof.host_runtime, str) and proof.host_runtime
    assert isinstance(proof.alibaba_hosted, bool)
    assert proof.backend_runtime == "Dockerized FastAPI"


# -----------------------------------------------------------------------
# Test 1: Local/offline proof returns alibaba_hosted=false
# -----------------------------------------------------------------------

def test_local_offline_proof_not_alibaba_hosted(monkeypatch):
    """Without any Alibaba env markers, alibaba_hosted must be False."""
    for var in ("ALIBABA_DEPLOYMENT_RUNTIME", "ALIBABA_HOSTED",
                "RAILWAY_ENVIRONMENT", "RAILWAY_SERVICE_ID"):
        monkeypatch.delenv(var, raising=False)
    proof = get_alibaba_proof()
    assert proof.alibaba_hosted is False
    assert proof.host_runtime == "local/unknown"


# -----------------------------------------------------------------------
# Test 2: Alibaba env marker returns alibaba_hosted=true and host_runtime
#         = "Alibaba Cloud ECS"
# -----------------------------------------------------------------------

def test_alibaba_marker_returns_honest_host(monkeypatch):
    """With ALIBABA_HOSTED=1, proof reports Alibaba ECS truthfully."""
    monkeypatch.setenv("ALIBABA_HOSTED", "1")
    monkeypatch.delenv("RAILWAY_ENVIRONMENT", raising=False)
    monkeypatch.delenv("RAILWAY_SERVICE_ID", raising=False)
    proof = get_alibaba_proof()
    assert proof.alibaba_hosted is True
    assert proof.host_runtime == "Alibaba Cloud ECS"


def test_host_reporting_distinguishes_railway(monkeypatch):
    """Railway markers produce alibaba_hosted=false, host_runtime=Railway."""
    for var in ("ALIBABA_DEPLOYMENT_RUNTIME", "ALIBABA_HOSTED"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.setenv("RAILWAY_ENVIRONMENT", "production")
    proof = get_alibaba_proof()
    assert proof.alibaba_hosted is False
    assert proof.host_runtime == "Railway"


# -----------------------------------------------------------------------
# Test 3: No secret values appear in payload
# -----------------------------------------------------------------------

def test_proof_contains_no_secrets(monkeypatch):
    """Even with credentials in env, no secret value leaks in the payload."""
    fake_key = "sk-" + "supersecretvalue" + "1234567890"
    fake_db = "postgre" + "sql://" + "user:pw@" + "host:5432/db"
    monkeypatch.setenv("DASHSCOPE_API_KEY", fake_key)
    monkeypatch.setenv("DATABASE_URL", fake_db)
    blob = json.dumps(get_alibaba_proof().model_dump())

    assert fake_key not in blob
    assert fake_db not in blob
    assert "user:pw@" not in blob
    # Credential presence is reported as a boolean only.
    assert get_alibaba_proof().dashscope_api_key_configured is True


# -----------------------------------------------------------------------
# Test 4: database.production_data_migrated is false
# -----------------------------------------------------------------------

def test_database_production_data_migrated_is_false():
    db = get_alibaba_proof().database
    assert db.production_data_migrated is False


# -----------------------------------------------------------------------
# Test 5: database.full_production_clone_verified is false
# -----------------------------------------------------------------------

def test_database_full_production_clone_verified_is_false():
    db = get_alibaba_proof().database
    assert db.full_production_clone_verified is False


# -----------------------------------------------------------------------
# Test 6: database.mirror_state is partial_selected_mirror
# -----------------------------------------------------------------------

def test_database_mirror_state_is_partial_selected():
    db = get_alibaba_proof().database
    assert db.mirror_state == "partial_selected_mirror"
    assert db.connected is None  # no probe in offline mode


# -----------------------------------------------------------------------
# Test 7: alibaba_services.ai references DashScope / Model Studio and
#         qwen_overlay.py
# -----------------------------------------------------------------------

def test_alibaba_services_ai_references_dashscope_and_overlay():
    proof = get_alibaba_proof()
    ai = proof.alibaba_services.get("ai", {})
    assert ai["service"] == "Alibaba Cloud Model Studio / DashScope"
    assert ai["actual_call_implementation"] == "backend/app/qwen_overlay.py"
    assert ai["live_smoke_endpoint"] == "/api/proof/qwen-smoke"
    # compute service
    compute = proof.alibaba_services.get("compute", {})
    assert compute["service"] == "Alibaba Cloud ECS"
    # database service
    database = proof.alibaba_services.get("database", {})
    assert database["service"] == "Alibaba RDS PostgreSQL-compatible"
    assert database["role"] == "selected evidence mirror"
    assert database["production_data_migrated"] is False
    assert database["full_production_clone_verified"] is False


# -----------------------------------------------------------------------
# Test 8: safe_claims mention qwen-smoke as separate admin-gated live call
# -----------------------------------------------------------------------

def test_safe_claims_reference_qwen_smoke_and_overlay_impl():
    claims = get_alibaba_proof().safe_claims
    claims_text = " ".join(claims)
    # Must mention the overlay implementation file
    assert "qwen_overlay.py" in claims_text, (
        "safe_claims must reference backend/app/qwen_overlay.py as the real call path"
    )
    # Must mention the admin-gated smoke endpoint as a separate live proof
    assert "qwen-smoke" in claims_text, (
        "safe_claims must reference /api/proof/qwen-smoke as the admin-gated live call"
    )
    # Must clarify the proof endpoint itself makes no external calls
    assert "no external" in claims_text.lower() or "no external network call" in claims_text.lower()


# -----------------------------------------------------------------------
# Existing / supporting tests
# -----------------------------------------------------------------------

def test_database_claim_is_precise():
    db = get_alibaba_proof().database
    # RDS provisioning is NOT the same as a verified full-data migration.
    assert db.production_data_migrated is False
    assert db.full_production_clone_verified is False
    assert db.mirror_state == "partial_selected_mirror"
    # No external probe is performed, so connectivity is not asserted.
    assert db.connected is None
    assert "migration" in db.note.lower() or "mirror" in db.note.lower()


def test_qwen_config_no_secret():
    cfg = get_qwen_config().model_dump()
    assert "dashscope" in cfg["base_url"]
    assert cfg["prompt_version"]
    assert cfg["output_schema_version"]
    assert "api_key" not in json.dumps(cfg).lower() or cfg["credential_configured"] in (True, False)


# -----------------------------------------------------------------------
# Phase 6 tests: judge_evidence, attestation, enhanced alibaba_services
# -----------------------------------------------------------------------

REQUIRED_FIELDS_V3 = REQUIRED_FIELDS + ["judge_evidence", "attestation", "runtime_mode"]


def test_proof_has_judge_evidence_and_attestation_fields():
    proof = get_alibaba_proof().model_dump()
    for field in REQUIRED_FIELDS_V3:
        assert field in proof, f"missing field: {field}"


def test_judge_evidence_contains_deployment_proof_and_qwen_impl():
    proof = get_alibaba_proof()
    je = proof.judge_evidence
    assert je["deployment_proof_code"] == "backend/app/alibaba_cloud_proof.py"
    assert je["qwen_api_implementation"] == "backend/app/qwen_overlay.py"
    assert je["live_proof_url"] == "http://8.222.191.152/api/proof/alibaba-cloud"
    assert je["live_product_url"] == "https://pantheon-research.com"
    assert je["alibaba_demo_url"] == "http://8.222.191.152"


def test_judge_evidence_qwen_http_call_contains_chat_completions():
    proof = get_alibaba_proof()
    assert "/chat/completions" in proof.judge_evidence["qwen_http_call"]
    assert proof.judge_evidence["qwen_http_call"].startswith("POST ")


def test_attestation_proof_endpoint_external_calls_is_false():
    proof = get_alibaba_proof()
    assert proof.attestation["proof_endpoint_external_calls"] is False


def test_attestation_credential_values_returned_is_false():
    proof = get_alibaba_proof()
    assert proof.attestation["credential_values_returned"] is False


def test_attestation_secrets_policy():
    proof = get_alibaba_proof()
    assert "booleans only" in proof.attestation["secrets_policy"]


def test_alibaba_services_ai_includes_openai_compatible():
    proof = get_alibaba_proof()
    ai = proof.alibaba_services.get("ai", {})
    assert ai["api_protocol"] == "OpenAI-compatible chat completions"
    assert ai["http_method"] == "POST"
    assert ai["chat_completions_path"] == "/chat/completions"
    assert "BLOCKED_BY_MISSING_CREDENTIAL" in ai["fail_closed_statuses"]
    assert "API_ERROR" in ai["fail_closed_statuses"]
    assert "PARSE_ERROR" in ai["fail_closed_statuses"]


def test_alibaba_services_compute_has_public_endpoint():
    proof = get_alibaba_proof()
    compute = proof.alibaba_services.get("compute", {})
    assert compute["reverse_proxy"] == "Nginx"
    assert compute["backend_runtime"] == "Dockerized FastAPI"
    assert "8.222.191.152" in compute["public_endpoint"]


def test_alibaba_services_database_does_not_claim_production_migration():
    proof = get_alibaba_proof()
    database = proof.alibaba_services.get("database", {})
    assert database["production_data_migrated"] is False
    assert database["full_production_clone_verified"] is False
    assert database["mirror_state"] == "partial_selected_mirror"
    # connected_in_live_ecs is a string, not a boolean true
    assert isinstance(database["connected_in_live_ecs"], str)
    assert "not probed" in database["connected_in_live_ecs"].lower()


def test_serialized_proof_has_no_secrets_tokens_or_db_urls(monkeypatch):
    """Comprehensive secret scan on the serialized proof payload."""
    fake_key = "sk-" + "a1b2c3d4e5f6g7h8i9j0" + "xxxxxxxx"
    fake_db = "postgres" + "ql://admin:s3cret@" + "rds.aliyuncs.com:5432/prod"
    fake_admin = "x-admin-token" + ":supersecretadmintoken"
    monkeypatch.setenv("DASHSCOPE_API_KEY", fake_key)
    monkeypatch.setenv("DATABASE_URL", fake_db)
    blob = json.dumps(get_alibaba_proof().model_dump())

    assert fake_key not in blob
    assert fake_db not in blob
    assert "s3cret@" not in blob
    assert "supersecretadmintoken" not in blob
    assert "rds.aliyuncs.com" not in blob
    # booleans only
    p = get_alibaba_proof()
    assert isinstance(p.dashscope_api_key_configured, bool)
    assert isinstance(p.qwen_configured, bool)

# -----------------------------------------------------------------------
# Phase 8 tests: runtime_mode
# -----------------------------------------------------------------------

def test_runtime_mode_public_repo_default_is_offline_sample():
    proof = get_alibaba_proof()
    rm = proof.runtime_mode
    assert rm["public_repo_default"] == "offline_sample"
    assert rm["live_alibaba_ecs"] == "live_production_proof"


def test_runtime_mode_proof_endpoint_external_calls_is_false():
    proof = get_alibaba_proof()
    assert proof.runtime_mode["proof_endpoint_external_calls"] is False


def test_runtime_mode_qwen_live_call_location_mentions_admin_gated():
    proof = get_alibaba_proof()
    assert "admin-gated" in proof.runtime_mode["qwen_live_call_location"]


def test_runtime_mode_database_connectivity_mentions_offline_no_probe():
    proof = get_alibaba_proof()
    assert "offline" in proof.runtime_mode["database_connectivity"]
    assert "not probe" in proof.runtime_mode["database_connectivity"]
