#!/usr/bin/env bash
set -euo pipefail
AUTH="${AUTH:-http://localhost:8025}"
BILL="${BILL:-http://localhost:8022}"
UMGMT="${UMGMT:-http://localhost:8023}"
ANALYTICS="${ANALYTICS:-http://localhost:8024}"

echo "=== Capstone Option 3 — SaaS demo ==="
for url in "$AUTH/health" "$BILL/health" "$UMGMT/health" "$ANALYTICS/health"; do
  curl -sf "$url" | jq -c .
done

echo "=== Create tenant ==="
TENANT=$(curl -sf -X POST "$UMGMT/tenants" -H "Content-Type: application/json" \
  -d '{"name":"Acme SaaS"}')
TID=$(echo "$TENANT" | jq -r .id)
echo "$TENANT" | jq .

echo "=== Invite member + register/login (JWT with tenant_id) ==="
curl -sf -X POST "$UMGMT/tenants/$TID/invites" -H "Content-Type: application/json" \
  -d '{"email":"admin@acme.example","role":"admin"}' | jq -c .

EMAIL="admin-$(date +%s)@acme.example"
curl -sf -X POST "$AUTH/auth/register" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"password123\",\"tenant_id\":\"$TID\",\"role\":\"admin\"}" | jq -c .

LOGIN=$(curl -sf -X POST "$AUTH/auth/login" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"password123\"}")
TOKEN=$(echo "$LOGIN" | jq -r .access_token)
echo "$LOGIN" | jq -c '{tenant_id,role}'
echo "$TID" > /tmp/capstone-opt3-tenant-id

echo "=== Subscribe to starter plan ==="
curl -sf -X POST "$BILL/subscriptions" -H "Content-Type: application/json" \
  -d "{\"tenant_id\":\"$TID\",\"plan_name\":\"starter\"}" | jq .

echo "=== Record usage (1500 units → overage invoice) ==="
curl -sf -X POST "$ANALYTICS/usage" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"tenant_id\":\"$TID\",\"metric\":\"api_calls\",\"units\":1500}" | jq .

sleep 1
echo "=== Invoices for tenant ==="
curl -sf "$BILL/tenants/$TID/invoices" | jq .

echo "=== Cross-tenant blocked ==="
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$ANALYTICS/usage" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"tenant_id":"other-tenant","metric":"api_calls","units":1}')
echo "cross-tenant usage HTTP $CODE (expect 403)"

echo "=== Option 3 demo complete ==="
