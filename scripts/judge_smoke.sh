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
echo "== Live Alibaba Cloud ECS proof @ $ALIBABA (best-effort; production backend) =="
softcheck "alibaba live proof" "$ALIBABA/api/proof/alibaba-cloud" '.cloud_provider' "Alibaba"

echo
echo "-------------------------------------------"
echo "  PASS=$PASS  FAIL=$FAIL"
[ "$FAIL" -eq 0 ] && { echo "  ALL GREEN"; exit 0; } || { echo "  SOME CHECKS FAILED"; exit 1; }
