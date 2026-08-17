#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

pass() { echo "  [PASS] $*"; }
fail() { echo "  [FAIL] $*" >&2; exit 1; }

echo "Capstone Option 2 verification"

for port in 8011 8012 8013 8014; do
  curl -sf "http://localhost:${port}/health" >/dev/null || fail "health :${port} — run: docker compose up -d --build"
  pass "health :${port}"
done

"${ROOT}/scripts/demo.sh" >/tmp/capstone-opt2-demo.out
grep -q "Option 2 demo complete" /tmp/capstone-opt2-demo.out || fail "demo failed"
pass "end-to-end demo"

EVENTS=$(curl -sf "http://localhost:8014/events")
echo "$EVENTS" | jq -e '.events | map(select(.detail_type == "PaymentPlaced")) | length >= 1' >/dev/null \
  || fail "PaymentPlaced missing"
pass "PaymentPlaced event"

echo "$EVENTS" | jq -e '.events | map(select(.detail_type == "FraudAlert")) | length >= 1' >/dev/null \
  || fail "FraudAlert missing (high-value transfer)"
pass "FraudAlert event"

SCORES=$(curl -sf "http://localhost:8013/scores")
echo "$SCORES" | jq -e '.scores | map(select(.decision == "REVIEW")) | length >= 1' >/dev/null \
  || fail "fraud REVIEW score missing"
pass "fraud REVIEW score"

[[ -f "${ROOT}/contracts/payment-service.yaml" ]] || fail "payment OpenAPI missing"
pass "payment OpenAPI present"

echo "Option 2 PASSED"
