#!/bin/bash
# ======================================================
# Build frontend from this repository's frontend directory by default.
# Optional override:
#   QUANTDINGER_FRONTEND_DIR=/path/to/other/frontend ./scripts/build-frontend.sh
#
# Prerequisites:
#   - Node.js >= 16 in PATH
# ======================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_FRONTEND_DIR="$PROJECT_ROOT/frontend"
DIST_TARGET="$PROJECT_ROOT/frontend/dist"

FRONTEND_DIR="${QUANTDINGER_FRONTEND_DIR:-$REPO_FRONTEND_DIR}"

echo "============================================"
echo "  QuantDinger — build frontend"
echo "============================================"

if [ ! -d "$FRONTEND_DIR" ]; then
  echo "ERROR: Frontend directory not found: $FRONTEND_DIR"
  echo "Set QUANTDINGER_FRONTEND_DIR or use default: $REPO_FRONTEND_DIR"
  exit 1
fi

FRONTEND_DIR="$(cd "$FRONTEND_DIR" && pwd)"
REPO_FRONTEND_DIR="$(cd "$REPO_FRONTEND_DIR" && pwd)"
echo "Frontend dir: $FRONTEND_DIR"

echo "[1/3] Installing dependencies..."
cd "$FRONTEND_DIR"
npm install --legacy-peer-deps

echo "[2/3] Building production bundle..."
npm run build

if [ "$FRONTEND_DIR" = "$REPO_FRONTEND_DIR" ]; then
  echo "[3/3] Sync skipped (build already outputs to frontend/dist)."
else
  echo "[3/3] Syncing dist -> frontend/dist/..."
  mkdir -p "$DIST_TARGET"
  rm -rf "$DIST_TARGET"/*
  cp -r "$FRONTEND_DIR/dist/"* "$DIST_TARGET/"
fi

echo ""
echo "============================================"
echo "  Done. Output: frontend/dist/"
echo "  Files: $(find "$DIST_TARGET" -type f | wc -l)"
echo "  Size:  $(du -sh "$DIST_TARGET" | cut -f1)"
echo "============================================"
