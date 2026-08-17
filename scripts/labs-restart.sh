#!/usr/bin/env bash
# Restart labs: stop then start
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STOP_ARGS=(--all)
START_ARGS=(--all)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) STOP_ARGS=(--all); START_ARGS=(--all) ;;
    --local|--local-only) STOP_ARGS=(--local-only); START_ARGS=(--local) ;;
    --aws|--aws-only) STOP_ARGS=(--aws-only); START_ARGS=(--aws-only) ;;
    --skip-build) START_ARGS+=(--skip-build) ;;
    --verify) START_ARGS+=(--verify) ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
  shift
done

echo "==> Stopping labs..."
"${ROOT}/scripts/labs-stop.sh" "${STOP_ARGS[@]}"

echo ""
echo "==> Starting labs..."
"${ROOT}/scripts/labs-start.sh" "${START_ARGS[@]}"
