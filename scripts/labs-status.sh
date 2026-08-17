#!/usr/bin/env bash
# Show local Docker and AWS platform status + estimated cost state
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TF_DIR="${ROOT}/infrastructure/terraform"
export AWS_REGION="${AWS_REGION:-us-east-1}"

echo "=============================================="
echo "  LABS STATUS"
echo "=============================================="

# --- Local Docker ---
echo ""
echo "Local Docker:"
if command -v docker >/dev/null 2>&1; then
  cd "${ROOT}"
  running=$(docker compose ps --status running -q 2>/dev/null | grep -c . || true)
  if [[ "$running" -ge 1 ]]; then
    echo "  State:  RUNNING (${running} container(s))"
    docker compose ps --format 'table {{.Service}}\t{{.Status}}\t{{.Ports}}' 2>/dev/null || docker compose ps
    echo ""
    echo "  URLs:"
    echo "    http://localhost:8001/docs  (user)"
    echo "    http://localhost:8002/docs  (product)"
    echo "    http://localhost:8004/      (welcome)"
  else
    echo "  State:  STOPPED"
    echo "  Start:  ./scripts/labs-start.sh --local"
  fi
else
  echo "  State:  Docker not installed"
fi

# --- AWS ---
echo ""
echo "AWS platform:"
if ! command -v terraform >/dev/null 2>&1 || ! command -v aws >/dev/null 2>&1; then
  echo "  State:  terraform/aws CLI not available"
  exit 0
fi

if [[ ! -d "${TF_DIR}" ]]; then
  echo "  State:  Terraform not initialized"
  exit 0
fi

ACTIVE="$(terraform -chdir="${TF_DIR}" output -raw platform_active 2>/dev/null || echo "unknown")"
PLATFORM_URL="$(terraform -chdir="${TF_DIR}" output -raw platform_url 2>/dev/null || echo "")"
CLUSTER="$(terraform -chdir="${TF_DIR}" output -raw ecs_cluster_name 2>/dev/null || echo "ms-course-dev-cluster")"

echo "  platform_active: ${ACTIVE}"

if [[ "$ACTIVE" == "true" ]]; then
  echo '  Cost:   ACTIVE (~$1.50-3/day - NAT Gateway + ALB + Fargate)'
  echo "  URL:    ${PLATFORM_URL}"
  if [[ -n "$PLATFORM_URL" ]]; then
    code="$(curl -sS -o /dev/null -w '%{http_code}' --max-time 5 "${PLATFORM_URL}/" 2>/dev/null || echo "000")"
    echo "  Health: GET / -> HTTP ${code}"
  fi
  echo ""
  echo "  ECS tasks:"
  for svc in user-service product-service order-service notification-service; do
    counts="$(aws ecs describe-services --cluster "$CLUSTER" --services "$svc" \
      --region "$AWS_REGION" \
      --query 'services[0].[runningCount,desiredCount]' --output text 2>/dev/null || echo "? ?")"
    echo "    ${svc}: ${counts}"
  done
  echo ""
  echo "  Stop billing: ./scripts/labs-stop.sh --aws-only"
elif [[ "$ACTIVE" == "false" ]]; then
  echo '  Cost:   STOPPED (~$0-2/month - ECR images + idle DynamoDB)'
  echo "  Start:  ./scripts/labs-start.sh --aws"
else
  echo "  Cost:   unknown (run terraform init in infrastructure/terraform)"
fi

echo ""
echo "Commands:"
echo "  Start all:    ./scripts/labs-start.sh --all"
echo "  Stop all:     ./scripts/labs-stop.sh"
echo '  Zero AWS $:   ./scripts/labs-stop.sh --destroy'
echo "  Verify labs:  ./scripts/verify-all-labs.sh"
