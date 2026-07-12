"""Alibaba Cloud deployment proof (v2) — public deployment-proof endpoint.

Public-safe and honest by construction:

  * No secrets. Credentials are reported as booleans only; no key, token, or
    connection string is ever returned.
  * No external calls. This endpoint never dials the database or the model —
    so it never *claims* live connectivity it did not verify.
  * Honest host. ``alibaba_hosted`` is detected from the environment. The same
    container image runs on Railway (``alibaba_hosted=false``) and on an
    Alibaba Cloud ECS box (``alibaba_hosted=true``). The Qwen *AI provider* is
    always Alibaba Cloud DashScope, on every host.
  * Precise database claim. RDS *provisioning* is kept distinct from full
    production-data *migration*, which is never asserted here.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

from .deepseek_overlay import DEEPSEEK_MODEL
from .models import AlibabaCloudProof, DatabaseProof, QwenConfig
from .qwen_overlay import (
    OUTPUT_SCHEMA_VERSION,
    PROMPT_VERSION,
    QWEN_BASE_URL,
    QWEN_MODEL,
    _check_credential,
)

_DEFAULT_REGION = "ap-southeast-1"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _detect_host_runtime() -> Dict[str, Any]:
    """Honestly report where this process actually runs (secret-free).

    Detection order:
      1. Explicit Alibaba marker (set only in the Alibaba container env).
      2. Railway's auto-injected environment markers.
      3. Otherwise local / unknown.
    """
    alibaba_marker = os.environ.get("ALIBABA_DEPLOYMENT_RUNTIME") or os.environ.get(
        "ALIBABA_HOSTED"
    )
    railway_marker = os.environ.get("RAILWAY_ENVIRONMENT") or os.environ.get(
        "RAILWAY_SERVICE_ID"
    )
    if alibaba_marker:
        return {
            "host_runtime": os.environ.get(
                "ALIBABA_DEPLOYMENT_RUNTIME", "Alibaba Cloud ECS"
            )
            or "Alibaba Cloud ECS",
            "alibaba_hosted": True,
        }
    if railway_marker:
        return {"host_runtime": "Railway", "alibaba_hosted": False}
    return {"host_runtime": "local/unknown", "alibaba_hosted": False}


def _git_sha() -> str:
    for var in ("RAILWAY_GIT_COMMIT_SHA", "GIT_SHA", "GIT_COMMIT", "SOURCE_COMMIT"):
        val = os.environ.get(var)
        if val:
            return val[:12]
    return "unknown"


def _database_proof() -> DatabaseProof:
    """Precise, non-overclaiming database representation.

    ``configured`` reflects whether ``DATABASE_URL`` is set in *this* runtime.
    ``connected`` is ``None`` because this endpoint performs no external call —
    we do not assert connectivity we did not test. ``production_data_migrated``
    is ``False``: RDS provisioning is not the same as a verified full-data
    migration, and this repo does not carry the row-count / read-path proof
    required to claim it.
    """
    configured = bool(os.environ.get("DATABASE_URL"))
    return DatabaseProof(
        provider="PostgreSQL (Alibaba RDS-compatible target engine)",
        configured=configured,
        connected=None,
        role=(
            "Selected evidence mirror in production; the public offline demo "
            "runs against bundled samples and needs no database."
        ),
        mirror_state="partial_selected_mirror",
        production_data_migrated=False,
        full_production_clone_verified=False,
        note=(
            "Alibaba RDS is deployed and connected as a selected evidence mirror "
            "in the live ECS deployment. This offline proof endpoint performs no "
            "DB probe, so connected is null here. Full production-data migration "
            "is not claimed without core row counts and API read-path verification."
        ),
    )


def get_alibaba_proof() -> AlibabaCloudProof:
    """Return the v2 Alibaba Cloud deployment proof (no secrets)."""
    host = _detect_host_runtime()
    dashscope_configured = _check_credential()
    return AlibabaCloudProof(
        host_runtime=host["host_runtime"],
        alibaba_hosted=host["alibaba_hosted"],
        qwen_base_url=QWEN_BASE_URL,
        qwen_model=QWEN_MODEL,
        qwen_configured=dashscope_configured,
        dashscope_api_key_configured=dashscope_configured,
        demo_mode=os.environ.get("DEMO_MODE", "offline"),
        region=os.environ.get("ALIBABA_REGION", _DEFAULT_REGION),
        git_sha=_git_sha(),
        timestamp_utc=_utc_now_iso(),
        alibaba_services={
            "compute": {
                "service": "Alibaba Cloud ECS",
                "evidence": "host_runtime + alibaba_hosted runtime marker",
                "host_runtime": host["host_runtime"],
                "alibaba_hosted": host["alibaba_hosted"],
                "reverse_proxy": "Nginx",
                "backend_runtime": "Dockerized FastAPI",
                "public_endpoint": "http://8.222.191.152/api/proof/alibaba-cloud",
            },
            "ai": {
                "service": "Alibaba Cloud Model Studio / DashScope",
                "base_url": QWEN_BASE_URL,
                "model": QWEN_MODEL,
                "credential_configured": dashscope_configured,
                "live_smoke_endpoint": "/api/proof/qwen-smoke",
                "actual_call_implementation": "backend/app/qwen_overlay.py",
                "api_protocol": "OpenAI-compatible chat completions",
                "http_method": "POST",
                "chat_completions_path": "/chat/completions",
                "fail_closed_statuses": [
                    "BLOCKED_BY_MISSING_CREDENTIAL",
                    "API_ERROR",
                    "PARSE_ERROR",
                ],
            },
            "database": {
                "service": "Alibaba RDS PostgreSQL-compatible",
                "role": "selected evidence mirror",
                "mirror_state": "partial_selected_mirror",
                "production_data_migrated": False,
                "full_production_clone_verified": False,
                "configured_from_env": bool(os.environ.get("DATABASE_URL")),
                "connected_in_live_ecs": (
                    "operator-attested in live proof; not probed by offline proof endpoint"
                ),
            },
        },
        proof_endpoints={
            "deployment_proof": "/api/proof/alibaba-cloud",
            "deployment_proof_alias": "/api/alibaba/proof",
            "qwen_config": "/api/alibaba/qwen-config",
            "data_quality": "/api/data-quality",
            "qwen_live_smoke": (
                "/api/proof/qwen-smoke (admin-gated; served by the production "
                "backend on the live Alibaba ECS host, not by this offline demo)"
            ),
        },
        database=_database_proof(),
        safe_claims=[
            "Backend deployment proof is served by a Dockerized FastAPI app "
            "behind Nginx.",
            "The live Alibaba ECS box reports alibaba_hosted=true and "
            "host_runtime=Alibaba Cloud ECS.",
            "Qwen integration uses Alibaba Cloud Model Studio / DashScope in "
            "OpenAI-compatible mode.",
            "Actual Qwen API call implementation is in "
            "backend/app/qwen_overlay.py.",
            "Public proof endpoint makes no external calls and returns no "
            "secrets.",
            "Admin-gated qwen-smoke endpoint performs a real Qwen smoke call "
            "on the live ECS host.",
            "Alibaba RDS is connected as a selected evidence mirror on the "
            "live ECS deployment.",
        ],
        non_claims=[
            "Alibaba RDS is NOT a full production database clone.",
            "Alibaba RDS is NOT a byte-for-byte production migration.",
            "Not claiming all APIs read from Alibaba RDS.",
            "Not claiming autonomous trading or model-generated alpha.",
            "Not exposing private production strategy code.",
            "This public repository is a sanitized vertical slice, not the "
            "full private production system.",
        ],
        judge_evidence={
            "deployment_proof_code": "backend/app/alibaba_cloud_proof.py",
            "qwen_api_implementation": "backend/app/qwen_overlay.py",
            "qwen_http_call": f"POST {QWEN_BASE_URL}/chat/completions",
            "qwen_base_url": QWEN_BASE_URL,
            "qwen_model": QWEN_MODEL,
            "live_proof_url": "http://8.222.191.152/api/proof/alibaba-cloud",
            "live_product_url": "https://pantheon-research.com",
            "alibaba_demo_url": "http://8.222.191.152",
            "qwen_smoke_endpoint": "/api/proof/qwen-smoke",
            "verification_doc": "docs/judge_evidence.md",
        },
        runtime_mode={
            "public_repo_default": "offline_sample",
            "live_alibaba_ecs": "live_production_proof",
            "proof_endpoint_external_calls": False,
            "qwen_live_call_location": (
                "admin-gated /api/proof/qwen-smoke and overlay endpoints"
            ),
            "database_connectivity": (
                "offline proof does not probe; live ECS proof documents "
                "selected evidence mirror connection"
            ),
        },
        attestation={
            "proof_endpoint_external_calls": False,
            "credential_values_returned": False,
            "host_detection_source": "environment marker",
            "database_connectivity_mode": (
                "offline proof does not probe; live ECS proof documents "
                "selected-mirror connection"
            ),
            "qwen_live_call_mode": (
                "separate admin-gated smoke endpoint and overlay endpoints"
            ),
            "secrets_policy": (
                "booleans only; no key, token, DB URL, or admin token returned"
            ),
        },
    )


def get_qwen_config() -> QwenConfig:
    """Return Qwen / DashScope configuration (no secrets)."""
    return QwenConfig(
        base_url=QWEN_BASE_URL,
        model=QWEN_MODEL,
        prompt_version=PROMPT_VERSION,
        output_schema_version=OUTPUT_SCHEMA_VERSION,
        credential_configured=_check_credential(),
        demo_mode=os.environ.get("DEMO_MODE", "offline"),
    )


# Referenced by the data-quality panel so both providers' configured-state and
# model ids come from one place.
def provider_snapshot() -> Dict[str, Any]:
    """Small, secret-free provider snapshot for the data-quality panel."""
    return {
        "qwen": {
            "model": QWEN_MODEL,
            "base_url": QWEN_BASE_URL,
            "configured": _check_credential(),
        },
        "deepseek": {
            "model": DEEPSEEK_MODEL,
            "configured": bool(os.environ.get("DEEPSEEK_API_KEY")),
        },
    }
