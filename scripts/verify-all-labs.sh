#!/usr/bin/env bash
# Run all lab verification scripts (local + AWS if platform is active)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TF_DIR="${ROOT}/infrastructure/terraform"
FAILED=0

platform_active() {
  terraform -chdir="$TF_DIR" output -raw platform_active 2>/dev/null || echo "false"
}

run_lab() {
  local i="$1"
  local script="${ROOT}/labs/module-${i}/verify.sh"
  if [[ ! -x "$script" ]]; then
    echo "WARN: missing ${script}"
    return 1
  fi
  echo ""
  echo "##############################"
  echo "# Lab Module ${i}"
  echo "##############################"
  "$script"
}

ACTIVE="$(platform_active)"
if [[ "$ACTIVE" == "true" ]]; then
  export PLATFORM_URL="$(terraform -chdir="$TF_DIR" output -raw platform_url 2>/dev/null || true)"
fi

# Always local / design labs
for i in 01 02 03 09; do
  run_lab "$i" || FAILED=1
done

# Event, data, security labs — use ALB when AWS platform is active
if [[ "$ACTIVE" == "true" ]]; then
  for i in 04 05 06 07 08; do
    run_lab "$i" || FAILED=1
  done
else
  for i in 05 06 07; do
    run_lab "$i" || FAILED=1
  done
  echo ""
  echo "SKIP: AWS labs 04 and 08 require active platform."
  echo "      Run: ./scripts/labs-start.sh --aws"
fi

if [[ $FAILED -eq 0 ]]; then
  echo ""
  echo "All applicable lab verifications PASSED"
  exit 0
fi
echo "Some lab verifications FAILED"
exit 1
