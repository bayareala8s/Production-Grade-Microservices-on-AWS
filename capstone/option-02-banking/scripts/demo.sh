#!/usr/bin/env bash
set -euo pipefail
BASE_CUST="${BASE_CUST:-http://localhost:8011}"
BASE_PAY="${BASE_PAY:-http://localhost:8012}"
BASE_FRAUD="${BASE_FRAUD:-http://localhost:8013}"
BASE_NOTIFY="${BASE_NOTIFY:-http://localhost:8014}"

echo "=== Capstone Option 2 — Banking demo ==="
for url in "$BASE_CUST/health" "$BASE_PAY/health" "$BASE_FRAUD/health" "$BASE_NOTIFY/health"; do
  curl -sf "$url" | jq -c .
done

EMAIL="bank-$(date +%s)@example.com"
echo "=== Create + approve customers ==="
C1=$(curl -sf -X POST "$BASE_CUST/customers" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"full_name\":\"Alice Bank\"}")
C1_ID=$(echo "$C1" | jq -r .id)
curl -sf -X PATCH "$BASE_CUST/customers/$C1_ID/kyc" -H "Content-Type: application/json" \
  -d '{"kyc_status":"APPROVED"}' | jq -c .

C2=$(curl -sf -X POST "$BASE_CUST/customers" -H "Content-Type: application/json" \
  -d "{\"email\":\"bob-$(date +%s)@example.com\",\"full_name\":\"Bob Bank\"}")
C2_ID=$(echo "$C2" | jq -r .id)
curl -sf -X PATCH "$BASE_CUST/customers/$C2_ID/kyc" -H "Content-Type: application/json" \
  -d '{"kyc_status":"APPROVED"}' | jq -c .

echo "=== Open accounts ==="
A1=$(curl -sf -X POST "$BASE_PAY/accounts" -H "Content-Type: application/json" \
  -d "{\"customer_id\":\"$C1_ID\",\"currency\":\"USD\",\"initial_balance\":\"500.00\"}")
A2=$(curl -sf -X POST "$BASE_PAY/accounts" -H "Content-Type: application/json" \
  -d "{\"customer_id\":\"$C2_ID\",\"currency\":\"USD\",\"initial_balance\":\"0.00\"}")
A1_ID=$(echo "$A1" | jq -r .id)
A2_ID=$(echo "$A2" | jq -r .id)
echo "$A1" | jq -c '{id,balance}'
echo "$A2" | jq -c '{id,balance}'

echo "=== Normal transfer (\$50) ==="
T1=$(curl -sf -X POST "$BASE_PAY/transfers" -H "Content-Type: application/json" \
  -d "{\"from_account_id\":\"$A1_ID\",\"to_account_id\":\"$A2_ID\",\"amount\":\"50.00\"}")
echo "$T1" | jq .
curl -sf "$BASE_PAY/transfers/$(echo "$T1" | jq -r .id)/ledger" | jq .

echo "=== High-value transfer (\$15000) to trigger fraud REVIEW ==="
# Top up A1
curl -sf -X POST "$BASE_PAY/accounts" -H "Content-Type: application/json" \
  -d "{\"customer_id\":\"$C1_ID\",\"currency\":\"USD\",\"initial_balance\":\"20000.00\"}" >/tmp/a3.json
A3_ID=$(jq -r .id /tmp/a3.json)
T2=$(curl -sf -X POST "$BASE_PAY/transfers" -H "Content-Type: application/json" \
  -d "{\"from_account_id\":\"$A3_ID\",\"to_account_id\":\"$A2_ID\",\"amount\":\"15000.00\"}")
echo "$T2" | jq -c '{id,amount,status}'

sleep 1
echo "=== Fraud scores ==="
curl -sf "$BASE_FRAUD/scores" | jq .

echo "=== Notification events ==="
curl -sf "$BASE_NOTIFY/events" | jq .

echo "=== Option 2 demo complete ==="
