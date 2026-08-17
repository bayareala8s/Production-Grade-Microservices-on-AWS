#!/usr/bin/env bash
set -euo pipefail
ACCT="${ACCT:-http://localhost:8031}"
INV="${INV:-http://localhost:8032}"
ANL="${ANL:-http://localhost:8033}"
REC="${REC:-http://localhost:8034}"
NTF="${NTF:-http://localhost:8035}"

echo "=== Capstone Option 4 — Idle Cost Advisor demo ==="
for url in "$ACCT/health" "$INV/health" "$ANL/health" "$REC/health" "$NTF/health"; do
  curl -sf "$url" | jq -c .
done

EMAIL="finops-$(date +%s)@example.com"
echo "=== Register + link AWS account (read-only) ==="
curl -sf -X POST "$ACCT/users" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"password123\",\"org_id\":\"bayareala8s\"}" | jq -c .
curl -sf -X POST "$ACCT/auth/login" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"password123\"}" | jq -c '{org_id,token_type}'
curl -sf -X POST "$ACCT/accounts/link?org_id=bayareala8s" -H "Content-Type: application/json" \
  -d '{"aws_account_id":"123456789012","role_arn":"arn:aws:iam::123456789012:role/FinOpsReadOnly"}' | jq .

echo "=== Start inventory scan (mock fixtures) ==="
SCAN=$(curl -sf -X POST "$INV/scans" -H "Content-Type: application/json" \
  -d '{"aws_account_id":"123456789012"}')
echo "$SCAN" | jq .
SCAN_ID=$(echo "$SCAN" | jq -r .id)
echo "$SCAN_ID" > /tmp/capstone-opt4-scan-id

sleep 2
echo "=== Analyzer findings ==="
curl -sf "$ANL/findings/$SCAN_ID" | jq .

echo "=== Recommendations (auto_destroy always false) ==="
curl -sf "$REC/recommendations" | jq .

echo "=== Notification IdleCostFinding events ==="
curl -sf "$NTF/events" | jq .

TOTAL=$(curl -sf "$ANL/findings/$SCAN_ID" | jq '.estimated_monthly_usd_total')
echo "Estimated idle cost: \$${TOTAL}/month (rate-card estimate)"
echo "=== Option 4 demo complete ==="
