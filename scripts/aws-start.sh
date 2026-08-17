#!/usr/bin/env bash
# Start course platform on AWS (creates NAT/ALB/ECS, builds and deploys images)
set -euo pipefail
source "$(dirname "$0")/aws/lib.sh"

require_tools

echo "=============================================="
echo "  AWS START — Production Microservices Course"
echo "=============================================="

cd "${TF_DIR}"
terraform init -input=false

echo "==> Phase 1: Ensure base infrastructure + ECR exist"
CURRENT_ACTIVE="$(platform_active_status)"
if [[ "$CURRENT_ACTIVE" == "true" ]]; then
  echo "    Platform currently active — scaling down before image push"
  scale_ecs_to_zero
  wait_for_ecs_zero
fi
terraform apply -input=false -auto-approve \
  -var="platform_active=false" \
  -var="ecs_desired_count=0"

if [[ "${SKIP_IMAGE_BUILD:-false}" != "true" ]]; then
  echo "==> Phase 2: Build and push container images"
  build_and_push_images
else
  echo "==> Phase 2: Skipping image build (SKIP_IMAGE_BUILD=true)"
fi

echo "==> Phase 3: Activate platform (NAT, ALB, ECS tasks)"
export ECS_DESIRED_COUNT=1
terraform apply -input=false -auto-approve \
  -var="platform_active=true" \
  -var="ecs_desired_count=1"

ensure_alb_ecs_security_group
wait_for_ecs_steady
wait_for_alb_healthy

PLATFORM_URL="$(tf_output platform_url)"
echo ""
echo "Platform STARTED"
echo "  URL: ${PLATFORM_URL}"
echo "  Welcome: ${PLATFORM_URL}/"
echo "  Products: ${PLATFORM_URL}/products"
echo "  Demo: PLATFORM_URL=${PLATFORM_URL} ./scripts/demo-platform.sh"
echo ""
print_aws_cost_state
echo "  Stop billing: ./scripts/labs-stop.sh --aws-only"
