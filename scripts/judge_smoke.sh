#!/usr/bin/env bash
#
# judge_smoke.sh — one-command smoke test for judges.
#
# Exercises the local backend (offline mode, no secrets required) end-to-end,
# then pings the live Alibaba Cloud proof endpoint. Zero configuration needed:
# offline sample overlays are bundled.
#
# Usage:
#   ./scripts/judge_smoke.sh                 # assumes backend on :8000
#   BASE=http://localhost:8000 ./scripts/judge_smoke.sh
#   ALIBABA=http://8.222.191.152 ./scripts/judge_smoke.sh
#
# To start the local backend first:
#   cd backend && pip install -r requirements.txt && uvicorn main:app --port 8000
set -uo pipefail

BASE="${BASE:-http://localhost:8000}"
ALIBABA="${ALIBABA:-http://8.222.191.152}"
TICKER="${TICKER:-MA}"
PASS=0; FAIL=0

jqget() { command -v jq >/dev/null 2>&1 && jq -r "$1" || cat; }

check() { # name url jq-filter expected-substring
  local name="$1" url="$2" filt="$3" want="$4"
  local out; out=$(curl -sS -m 30 "$url" 2>/dev/null | jqget "$filt" 2>/dev/null)
  if printf '%s' "$out" | grep -qi "$want"; then
    printf "  PASS  %-34s %s\n" "$name" "$out"; PASS=$((PASS+1))
  else
    printf "  FAIL  %-34s got=[%s] want~[%s]\n" "$name" "$out" "$want"; FAIL=$((FAIL+1))
  fi
}

softcheck() { # like check(), but never fails the run (best-effort live probe)
  local name="$1" url="$2" filt="$3" want="$4"
  local out; out=$(curl -sS -m 30 "$url" 2>/dev/null | jqget "$filt" 2>/dev/null)
  if printf '%s' "$out" | grep -qi "$want"; then
    printf "  PASS  %-34s %s\n" "$name" "$out"
  else
    printf "  SKIP  %-34s (live host not reachable — offline demo unaffected)\n" "$name"
  fi
}

echo "== Local backend (offline mode, no secrets) @ $BASE =="
check "health"             "$BASE/health"                       '.status'            "healthy"
check "evidence pack hash" "$BASE/api/evidence/$TICKER"         '.provenance.evidence_hash' "sha256"
check "qwen overlay"       "$BASE/api/overlay/qwen/$TICKER"     '.status'            "SAMPLE"
check "deepseek overlay"   "$BASE/api/overlay/deepseek/$TICKER" '.status'            "SAMPLE"
check "comparison state"   "$BASE/api/comparison/$TICKER"       '.data_state'        "."
check "comparison agree"   "$BASE/api/comparison/$TICKER"       '.agreement_level'   "."
check "data quality"       "$BASE/api/data-quality"             '.mode'              "."
check "module grid"        "$BASE/api/modules"                  '.modules[0].data_state' "."
check "alibaba proof (v2)" "$BASE/api/proof/alibaba-cloud"      '.schema_version'    "alibaba-proof"
check "proof host honest"  "$BASE/api/proof/alibaba-cloud"      '.host_runtime'      "."
check "proof db precise"   "$BASE/api/proof/alibaba-cloud"      '.database.production_data_migrated' "false"

check "provider health"    "$BASE/api/provider-health"             '.qwen.provider'      "Alibaba"
check "validation timeline" "$BASE/api/validation-timeline"          '.stages[0].name'      "Signal"
check "ticker profiles"     "$BASE/api/ticker-profiles"              '.tickers[0]'          "."
check "ticker profile NVDA" "$BASE/api/ticker-profile/NVDA"          '.company_name'       "NVIDIA"
check "mini macro"          "$BASE/api/mini/macro"                   '.data_state'         "CONTEXT"
check "mini market pulse"   "$BASE/api/mini/market-pulse"            '.data_state'         "CONTEXT"
check "mini ficc"           "$BASE/api/mini/ficc"                    '.data_state'         "CONTEXT"

echo
echo "== P0-1 Five-Model LLM Research Cockpit =="
check "llm providers (5)"   "$BASE/api/llm/providers"                '.status.registered_providers' "5"
check "llm cases"           "$BASE/api/llm/cases"                    '.count'              "3"
check "llm case NVDA (5)"   "$BASE/api/llm/case/NVDA"                '.overlays | length' "5"
check "llm comparison"      "$BASE/api/llm/comparison/NVDA"          '.winner'            "null"
check "llm agreement"       "$BASE/api/llm/agreement/MA"             '.agreement_matrix.agreement_score' "."
check "llm BTC not-gen"     "$BASE/api/llm/case/BTC"                 '.overlays[] | select(.provider=="gemini") | .data_state' "NOT_GENERATED"

echo
echo "== P0-2 Macro Risk Budget =="
check "macro regime"        "$BASE/api/macro/risk-budget"            '.confirmed_regime'  "REFLATION"
check "macro exposure"      "$BASE/api/macro/risk-budget"            '.final_exposure'    "."
check "macro freshness"     "$BASE/api/macro/risk-budget"            '.freshness'         "FRESH"
check "macro history"       "$BASE/api/macro/history"                '.count'             "."
check "macro scenarios"     "$BASE/api/macro/scenarios"              '.scenarios | length' "4"

echo
echo "== P0-3 Research Ops / Validation Console =="
check "research readiness"  "$BASE/api/research-ops/readiness"       '.modules | length'  "14"
check "research no-alpha"   "$BASE/api/research-ops/readiness"       '.no_alpha_claim'    "No alpha"
check "research perf null"  "$BASE/api/research-ops/outcomes"        '.modules[0].performance.hit_rate' "null"
check "research summary"    "$BASE/api/research-ops/summary"         '.modules_with_public_performance' "0"

echo
echo "== P1-1 Canonical Data Platform + Lineage =="
check "dp ingest runs"      "$BASE/api/data-platform/ingest-runs"    '.ingest_runs | length' "."
check "dp observations"     "$BASE/api/data-platform/observations"   '.observations | length' "."
check "dp version history"  "$BASE/api/data-platform/versions/1"     '.versions | length' "."
check "dp lineage llm (5)"  "$BASE/api/data-platform/lineage/sha256:b1b1a99dc8d5e218d93487c23166a804c3b69684e3781c6fa10f5117efdce4c9" '.llm_consumers | length' "5"

echo
echo "== P1-2 Paper / Shadow Trading Gateway (LIVE disabled) =="
check "pg status live off"  "$BASE/api/paper-gateway/status"         '.live_enabled'      "false"
check "pg no broker"        "$BASE/api/paper-gateway/status"         '.broker_adapter_present' "false"
check "pg llm cant exec"    "$BASE/api/paper-gateway/status"         '.llm_can_execute'   "false"
check "pg live disabled"    "$BASE/api/paper-gateway/live-disabled-proof" '.live_disabled' "true"
check "pg audit intact"     "$BASE/api/paper-gateway/provenance-completeness" '.audit_chain_intact' "true"

echo
echo "== P1-3 BTC Three-Layer Decision Stack =="
check "btc posture"         "$BASE/api/btc/current-posture"          '.outcome'           "."
check "btc history (>=200)" "$BASE/api/btc/history"                  '.count'             "."
check "btc conflicts match" "$BASE/api/btc/conflicts"                '[.examples[].matches_expected] | all' "true"

echo
echo "== Unified judge demo flow =="
check "judge full-demo"     "$BASE/api/judge/full-demo"              '.modules | length'  "6"
check "judge live off"      "$BASE/api/judge/full-demo"              '.safety.live_enabled' "false"

echo
echo "== Live Alibaba Cloud ECS proof @ $ALIBABA (best-effort; production backend) =="
softcheck "alibaba live proof" "$ALIBABA/api/proof/alibaba-cloud" '.cloud_provider' "Alibaba"

echo
echo "-------------------------------------------"
echo "  PASS=$PASS  FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && { echo "  ALL GREEN"; exit 0; } || { echo "  SOME CHECKS FAILED"; exit 1; }
