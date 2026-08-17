#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE_USER="${BASE_USER:-http://localhost:8001}"
BASE_PRODUCT="${BASE_PRODUCT:-http://localhost:8002}"
BASE_ORDER="${BASE_ORDER:-http://localhost:8003}"
BASE_NOTIFY="${BASE_NOTIFY:-http://localhost:8004}"
BASE_INV="${BASE_INV:-http://localhost:8005}"

echo "=== Capstone Option 1 — E-Commerce demo ==="
for url in "$BASE_USER/health" "$BASE_PRODUCT/health" "$BASE_ORDER/health" "$BASE_NOTIFY/health" "$BASE_INV/health"; do
  curl -sf "$url" | jq -c .
done

echo "=== Inventory before order ==="
curl -sf "$BASE_INV/inventory" | jq .

EMAIL="cap1-$(date +%s)@example.com"
USER=$(curl -sf -X POST "$BASE_USER/users" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"name\":\"Capstone One\",\"password\":\"learn12345\"}")
USER_ID=$(echo "$USER" | jq -r .id)
PRODUCT_ID=$(curl -sf "$BASE_PRODUCT/products" | jq -r '.[0].id')

echo "=== Place order (reserves inventory) ==="
ORDER=$(curl -sf -X POST "$BASE_ORDER/orders" -H "Content-Type: application/json" \
  -d "{\"user_id\":\"$USER_ID\",\"items\":[{\"product_id\":\"$PRODUCT_ID\",\"quantity\":1}]}")
echo "$ORDER" | jq .

echo "=== Inventory after order ==="
curl -sf "$BASE_INV/inventory/$PRODUCT_ID" | jq .

echo "=== Events ==="
sleep 1
curl -sf "$BASE_NOTIFY/events" | jq .

echo "=== Option 1 demo complete ==="
