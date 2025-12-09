#!/usr/bin/env bash
set -euo pipefail

# package_light.sh - create a minimal distribution with only core files and base requirements
# Usage: ./scripts/package_light.sh [output-filename]

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OUT_DIR=${1:-$REPO_ROOT/dist}
TIMESTAMP=$(date +%Y%m%d%H%M%S)
TMP_DIR=$(mktemp -d -t ghostlink-light-XXXX)

echo "Building light package..."
echo "repo: $REPO_ROOT"
echo "out dir: $OUT_DIR"

mkdir -p "$OUT_DIR"

# Copy minimal files and directories
mkdir -p "$TMP_DIR/ghostlink"
cp -R "$REPO_ROOT/ghostlink_gui" "$TMP_DIR/ghostlink/" 2>/dev/null || true
cp -R "$REPO_ROOT/ghostlink_ide" "$TMP_DIR/ghostlink/" 2>/dev/null || true
cp -R "$REPO_ROOT/docs" "$TMP_DIR/ghostlink/" 2>/dev/null || true
cp -R "$REPO_ROOT/scripts" "$TMP_DIR/ghostlink/" 2>/dev/null || true
cp -R "$REPO_ROOT/README.md" "$TMP_DIR/ghostlink/" 2>/dev/null || true

# Keep only base requirements
if [ -f "$REPO_ROOT/ghostlink_gui/backend/requirements-base.txt" ]; then
  mkdir -p "$TMP_DIR/ghostlink/ghostlink_gui/backend"
  cp "$REPO_ROOT/ghostlink_gui/backend/requirements-base.txt" "$TMP_DIR/ghostlink/ghostlink_gui/backend/requirements.txt"
fi

pushd "$TMP_DIR" >/dev/null
tar -czf "$OUT_DIR/ghostlink-light-$TIMESTAMP.tar.gz" ghostlink
popd >/dev/null

echo "Package created: $OUT_DIR/ghostlink-light-$TIMESTAMP.tar.gz"

rm -rf "$TMP_DIR"

echo "Done."
