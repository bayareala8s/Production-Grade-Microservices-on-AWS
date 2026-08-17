#!/usr/bin/env bash
# Start local Docker labs and/or AWS platform for teaching
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
START_LOCAL=true
START_AWS=false
VERIFY=false
SKIP_BUILD=false

usage() {
  cat <<'EOF'
Usage: ./scripts/labs-start.sh [OPTIONS]

Start the course lab environment (local Docker and/or AWS).

Options:
  --all           Start local Docker + AWS (default for instructors teaching AWS labs)
  --local         Start local Docker only (Labs 01-03, 05-07, 09) [default]
  --aws           Also start AWS platform (Labs 04, 06, 08) — ~15-20 min first time
  --aws-only      Start AWS only (skip local Docker)
  --skip-build    Skip Docker image rebuild/push on AWS (faster restart, same-day)
  --verify        Run ./scripts/verify-all-labs.sh after start
  -h, --help      Show this help

Examples:
  ./scripts/labs-start.sh                  # local Docker only
  ./scripts/labs-start.sh --all            # local + AWS for full course
  ./scripts/labs-start.sh --aws-only         # AWS labs only
  ./scripts/labs-start.sh --all --verify   # start everything and verify

Stop to avoid charges:
  ./scripts/labs-stop.sh                   # stop local + AWS (minimize cost)
  ./scripts/labs-stop.sh --destroy         # delete all AWS resources ($0)
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all) START_LOCAL=true; START_AWS=true ;;
    --local) START_LOCAL=true; START_AWS=false ;;
    --aws) START_AWS=true ;;
    --aws-only) START_LOCAL=false; START_AWS=true ;;
    --skip-build) SKIP_BUILD=true ;;
    --verify) VERIFY=true ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1"; usage; exit 1 ;;
  esac
  shift
done

echo "=============================================="
echo "  LABS START"
echo "=============================================="

if $START_LOCAL; then
  echo ""
  echo "==> Starting local Docker platform (Labs 02-03, 05-07, 09)..."
  cd "${ROOT}"
  if [[ ! -f .env ]]; then
    cp .env.example .env
    echo "    Created .env from .env.example"
  fi
  docker compose up -d --build
  echo ""
  echo "Local services:"
  echo "  user-service         http://localhost:8001/docs"
  echo "  product-service      http://localhost:8002/docs"
  echo "  order-service        http://localhost:8003/docs"
  echo "  notification-service http://localhost:8004/  (welcome page)"
  echo ""
  echo "  Demo: ./scripts/demo-platform.sh"
fi

if $START_AWS; then
  echo ""
  if $SKIP_BUILD; then
    export SKIP_IMAGE_BUILD=true
  fi
  "${ROOT}/scripts/aws-start.sh"
fi

if $VERIFY; then
  echo ""
  echo "==> Verifying labs..."
  "${ROOT}/scripts/verify-all-labs.sh"
fi

echo ""
echo "Labs environment ready."
if $START_AWS; then
  echo "  Stop AWS billing: ./scripts/labs-stop.sh"
fi
if $START_LOCAL; then
  echo "  Stop local Docker:  ./scripts/labs-stop.sh --local-only"
fi
echo "  Check status:         ./scripts/labs-status.sh"
