#!/usr/bin/env bash
# Stop local Docker and/or AWS platform to minimize or eliminate cost
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STOP_LOCAL=true
STOP_AWS=true
DESTROY=false

usage() {
  cat <<'EOF'
Usage: ./scripts/labs-stop.sh [OPTIONS]

Stop the course lab environment to avoid ongoing charges.

Options:
  --all           Stop local Docker + AWS minimize-cost mode [default]
  --local         Stop local Docker only
  --aws           Stop AWS only (ECS, NAT, ALB destroyed — ~$0-2/month idle)
  --local-only    Alias for --local
  --aws-only      Alias for --aws
  --destroy       Delete ALL AWS resources ($0/month — requires confirmation)
  -h, --help      Show this help

Cost modes:
  Default stop    Removes NAT, ALB, Fargate tasks. Keeps VPC, ECR, DynamoDB.
  --destroy       Full teardown via terraform destroy (type 'destroy' to confirm).

Examples:
  ./scripts/labs-stop.sh                # stop everything, minimize AWS cost
  ./scripts/labs-stop.sh --local-only   # stop Docker only
  ./scripts/labs-stop.sh --aws-only     # stop AWS billing drivers only
  ./scripts/labs-stop.sh --destroy      # zero AWS cost (must re-run aws-start)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) STOP_LOCAL=true; STOP_AWS=true ;;
    --local|--local-only) STOP_LOCAL=true; STOP_AWS=false ;;
    --aws|--aws-only) STOP_LOCAL=false; STOP_AWS=true ;;
    --destroy) STOP_LOCAL=false; STOP_AWS=true; DESTROY=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
  shift
done

echo "=============================================="
echo "  LABS STOP"
echo "=============================================="

if $STOP_LOCAL; then
  echo ""
  echo "==> Stopping local Docker platform..."
  cd "${ROOT}"
  docker compose down
  echo "    Local Docker stopped (no local resource cost)"
fi

if $DESTROY; then
  echo ""
  "${ROOT}/scripts/aws-destroy.sh"
elif $STOP_AWS; then
  echo ""
  "${ROOT}/scripts/aws-stop.sh"
fi

echo ""
echo "Labs environment stopped."
if ! $DESTROY && $STOP_AWS; then
  echo '  AWS idle cost: ~$0-2/month (ECR storage + empty DynamoDB)'
  echo "  Restart:       ./scripts/labs-start.sh --aws"
fi
if $DESTROY; then
  echo '  AWS cost:      $0 (all resources destroyed)'
  echo "  Restart:       ./scripts/labs-start.sh --aws  (~15-20 min)"
fi
echo "  Status:          ./scripts/labs-status.sh"
