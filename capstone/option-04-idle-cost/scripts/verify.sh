#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

pass() { echo "  [PASS] $*"; }
fail() { echo "  [FAIL] $*" >&2; exit 1; }

echo "Capstone Option 4 verification"

wait_health() {
  local port="$1"
  local i
  for i in $(seq 1 30); do
    if curl -sf "http://localhost:${port}/health" >/dev/null; then
      return 0
    fi
    sleep 1
  done
  return 1
}

for port in 8031 8032 8033 8034 8035; do
  wait_health "$port" || fail "health :${port} — run: docker compose up -d --build"
  pass "health :${port}"
done

"${ROOT}/scripts/demo.sh" >/tmp/capstone-opt4-demo.out
grep -q "Option 4 demo complete" /tmp/capstone-opt4-demo.out || fail "demo failed"
pass "end-to-end demo"

SCAN_ID=$(cat /tmp/capstone-opt4-scan-id)
FINDINGS=$(curl -sf "http://localhost:8033/findings/$SCAN_ID")
COUNT=$(echo "$FINDINGS" | jq '.findings | length')
[[ "$COUNT" -ge 3 ]] || fail "expected >=3 idle findings, got $COUNT"
pass "idle findings ($COUNT)"

TOTAL=$(echo "$FINDINGS" | jq '.estimated_monthly_usd_total')
python3 -c "import sys; t=float('$TOTAL'); sys.exit(0 if t>0 else 1)" || fail "idle \$ total should be > 0"
pass "estimated monthly idle \$${TOTAL}"

RECS=$(curl -sf "http://localhost:8034/recommendations")
echo "$RECS" | jq -e '.recommendations | length >= 1' >/dev/null || fail "no recommendations"
echo "$RECS" | jq -e '[.recommendations[].auto_destroy] | all(. == false)' >/dev/null \
  || fail "auto_destroy must be false (recommend-only)"
pass "recommendations are recommend-only"

EVENTS=$(curl -sf "http://localhost:8035/events")
echo "$EVENTS" | jq -e '.events | map(select(.detail_type == "IdleCostFinding")) | length >= 1' >/dev/null \
  || fail "IdleCostFinding missing"
pass "IdleCostFinding events"

[[ -f "${ROOT}/contracts/inventory-service.yaml" ]] || fail "OpenAPI missing"
pass "inventory OpenAPI present"

echo "Option 4 PASSED"
