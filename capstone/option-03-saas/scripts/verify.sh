#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

pass() { echo "  [PASS] $*"; }
fail() { echo "  [FAIL] $*" >&2; exit 1; }

echo "Capstone Option 3 verification"

for port in 8025 8022 8023 8024; do
  curl -sf "http://localhost:${port}/health" >/dev/null || fail "health :${port} — run: docker compose up -d --build"
  pass "health :${port}"
done

"${ROOT}/scripts/demo.sh" >/tmp/capstone-opt3-demo.out
grep -q "Option 3 demo complete" /tmp/capstone-opt3-demo.out || fail "demo failed"
pass "end-to-end demo"

grep -q "cross-tenant usage HTTP 403" /tmp/capstone-opt3-demo.out || fail "cross-tenant isolation not enforced"
pass "cross-tenant isolation (403)"

TID=$(cat /tmp/capstone-opt3-tenant-id)
COUNT=$(curl -sf "http://localhost:8022/tenants/$TID/invoices" | jq 'length')
[[ "$COUNT" -ge 2 ]] || fail "expected base + overage invoices, got $COUNT"
pass "subscription + usage overage invoices ($COUNT)"

[[ -f "${ROOT}/contracts/billing-service.yaml" ]] || fail "billing OpenAPI missing"
pass "billing OpenAPI present"

echo "Option 3 PASSED"
