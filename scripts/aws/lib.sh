#!/usr/bin/env bash
# Shared AWS course platform helpers (source from bash scripts only — do not source from zsh)
set -euo pipefail

_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${_LIB_DIR}/../.." && pwd)"
TF_DIR="${ROOT_DIR}/infrastructure/terraform"
export AWS_REGION="${AWS_REGION:-us-east-1}"
export PROJECT_NAME="${PROJECT_NAME:-ms-course}"
export ENVIRONMENT="${ENVIRONMENT:-dev}"

ECS_SERVICES=(user-service product-service order-service notification-service)

tf() {
  terraform -chdir="${TF_DIR}" "$@"
}

tf_output() {
  tf output -raw "$1" 2>/dev/null || true
}

require_tools() {
  for cmd in terraform aws docker; do
    command -v "$cmd" >/dev/null || { echo "Missing required command: $cmd"; exit 1; }
  done
}

ecs_cluster_name() {
  local cluster
  cluster="$(tf_output ecs_cluster_name)"
  if [[ -n "$cluster" ]]; then
    echo "$cluster"
  else
    echo "${PROJECT_NAME}-${ENVIRONMENT}-cluster"
  fi
}

ecr_login() {
  local account region registry
  account="$(aws sts get-caller-identity --query Account --output text)"
  region="${AWS_REGION}"
  registry="${account}.dkr.ecr.${region}.amazonaws.com"
  aws ecr get-login-password --region "$region" | \
    docker login --username AWS --password-stdin "$registry" >/dev/null
  echo "$registry"
}

build_and_push_images() {
  local registry prefix tag
  registry="$(ecr_login | tail -1)"
  prefix="${PROJECT_NAME}-${ENVIRONMENT}"
  tag="${IMAGE_TAG:-latest}"

  for svc in "${ECS_SERVICES[@]}"; do
    local repo="${registry}/${prefix}-${svc}"
    echo "==> Building and pushing ${svc} -> ${repo}:${tag}"
    docker build --platform linux/amd64 -t "${repo}:${tag}" "${ROOT_DIR}/starters/python/${svc}"
    docker push "${repo}:${tag}"
  done
}

scale_ecs_to_zero() {
  local cluster
  cluster="$(ecs_cluster_name)"
  echo "==> Scaling ECS services to 0 in cluster ${cluster}..."
  for svc in "${ECS_SERVICES[@]}"; do
    aws ecs update-service --cluster "$cluster" --service "$svc" \
      --desired-count 0 --region "$AWS_REGION" >/dev/null 2>&1 || true
  done
}

wait_for_ecs_zero() {
  local cluster max attempt running
  cluster="$(ecs_cluster_name)"
  max=40
  echo "==> Waiting for ECS tasks to stop..."
  for svc in "${ECS_SERVICES[@]}"; do
    attempt=0
    while true; do
      running="$(aws ecs describe-services --cluster "$cluster" --services "$svc" \
        --region "$AWS_REGION" \
        --query 'services[0].runningCount' --output text 2>/dev/null || echo "0")"
      if [[ "$running" == "0" || "$running" == "None" ]]; then
        echo "    ${svc}: stopped"
        break
      fi
      attempt=$((attempt + 1))
      if [[ $attempt -ge $max ]]; then
        echo "    WARN: ${svc} still has ${running} running task(s)"
        break
      fi
      sleep 10
    done
  done
}

wait_for_ecs_steady() {
  local cluster max attempt running desired
  cluster="$(ecs_cluster_name)"
  max=40
  echo "==> Waiting for ECS services to stabilize in cluster ${cluster}..."
  for svc in "${ECS_SERVICES[@]}"; do
    attempt=0
    while true; do
      read -r running desired <<< "$(aws ecs describe-services --cluster "$cluster" --services "$svc" \
        --region "$AWS_REGION" \
        --query 'services[0].[runningCount,desiredCount]' --output text 2>/dev/null || echo "0 0")"
      if [[ "$running" == "$desired" && "$desired" -ge 1 ]]; then
        echo "    ${svc} ready (${running}/${desired})"
        break
      fi
      attempt=$((attempt + 1))
      if [[ $attempt -ge $max ]]; then
        echo "    WARN: ${svc} not stable (${running}/${desired}) — check CloudWatch /ecs/${PROJECT_NAME}-${ENVIRONMENT}"
        break
      fi
      sleep 15
    done
  done
}

wait_for_alb_healthy() {
  local url max attempts
  url="$(tf_output platform_url)"
  if [[ -z "$url" ]]; then
    echo "ALB URL not available (platform may be stopped)"
    return 1
  fi
  max=30
  attempts=0
  echo "==> Waiting for ALB at ${url}..."
  until curl -sf "${url}/products" >/dev/null 2>&1; do
    attempts=$((attempts + 1))
    if [[ $attempts -ge $max ]]; then
      echo "ALB not ready after ${max} attempts — attempting SG repair..."
      ensure_alb_ecs_security_group
      attempts=0
      max=10
      until curl -sf "${url}/products" >/dev/null 2>&1; do
        attempts=$((attempts + 1))
        if [[ $attempts -ge $max ]]; then
          echo "ALB not ready after SG repair"
          return 1
        fi
        sleep 10
      done
      echo "==> ALB is serving traffic (after SG repair)"
      return 0
    fi
    sleep 10
  done
  echo "==> ALB is serving traffic"
}

# Recreate ALB→ECS SG rule if Terraform state drifted (prevents 504 on /products)
ensure_alb_ecs_security_group() {
  echo "==> Ensuring ALB→ECS security group rule exists..."
  cd "${TF_DIR}"
  terraform apply -input=false -auto-approve \
    -var="platform_active=true" \
    -var="ecs_desired_count=${ECS_DESIRED_COUNT:-1}" \
    -target=aws_security_group_rule.ecs_tasks_from_alb >/dev/null 2>&1 || true
}

platform_active_status() {
  terraform -chdir="${TF_DIR}" output -raw platform_active 2>/dev/null || echo "false"
}

print_aws_cost_state() {
  local active
  active="$(platform_active_status)"
  if [[ "$active" == "true" ]]; then
    echo '  AWS cost state: ACTIVE (~$1.50-3/day - NAT + ALB + Fargate)'
  else
    echo '  AWS cost state: STOPPED (~$0-2/month - ECR + DynamoDB idle only)'
  fi
}
