#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

pass() { echo "  [PASS] $*"; }
fail() { echo "  [FAIL] $*" >&2; exit 1; }

echo "Capstone Option 1 verification"

for port in 8001 8002 8003 8004 8005; do
  curl -sf "http://localhost:${port}/health" >/dev/null || fail "health :${port} — run: docker compose up -d --build"
  pass "health :${port}"
done

INV_BEFORE=$(curl -sf "http://localhost:8005/inventory" | jq 'length')
[[ "$INV_BEFORE" -ge 1 ]] || fail "inventory empty — product seed may not have synced"
pass "inventory seeded (${INV_BEFORE} rows)"

"${ROOT}/scripts/demo.sh" >/tmp/capstone-opt1-demo.out
grep -q "Option 1 demo complete" /tmp/capstone-opt1-demo.out || fail "demo failed"
pass "end-to-end demo"

EVENTS=$(curl -sf "http://localhost:8004/events")
echo "$EVENTS" | jq -e '.events | map(select(.detail_type == "OrderPlaced")) | length >= 1' >/dev/null \
  || fail "OrderPlaced missing"
pass "OrderPlaced event"

[[ -f "${ROOT}/contracts/inventory-service.yaml" ]] || fail "OpenAPI missing"
pass "inventory OpenAPI present"

echo "Option 1 PASSED"
