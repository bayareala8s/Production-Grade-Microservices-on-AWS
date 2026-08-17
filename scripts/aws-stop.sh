#!/usr/bin/env bash
# Stop course platform on AWS — scales ECS to 0, removes NAT and ALB (main cost drivers)
set -euo pipefail
source "$(dirname "$0")/aws/lib.sh"

require_tools

echo "=============================================="
echo "  AWS STOP — Minimizing idle cost"
echo "=============================================="
echo "Stops: ECS tasks, ALB, NAT Gateway"
echo "Keeps: VPC, ECR images, DynamoDB, EventBridge (low/no idle cost)"
echo ""

scale_ecs_to_zero
wait_for_ecs_zero

cd "${TF_DIR}"
terraform init -input=false

_apply_stop() {
  terraform apply -input=false -auto-approve \
    -var="platform_active=false" \
    -var="ecs_desired_count=0"
}

if ! _apply_stop; then
  echo "    WARN: first apply failed (often SG drift) — retrying once..."
  _apply_stop
fi

ACTIVE="$(platform_active_status)"
echo ""
if [[ "$ACTIVE" == "false" ]]; then
  echo 'Platform STOPPED - idle cost minimized (~$0-2/month).'
else
  echo "Platform STOP requested — verify with: ./scripts/labs-status.sh"
fi
echo "  Restart:       ./scripts/labs-start.sh --aws"
echo "  Zero AWS cost: ./scripts/labs-stop.sh --destroy"
