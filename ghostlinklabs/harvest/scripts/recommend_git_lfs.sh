#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

echo "Scanning repo for large files to recommend Git LFS usage..."
find . -type f -not -path './.git/*' -printf '%s %p\n' | sort -nr | head -n 50 | awk '{printf "%s MB - %s\n", $1/1024/1024, $2}'

echo
echo "If you have large binaries to track, consider installing git-lfs and running:"
echo "  git lfs install"
echo "  git lfs track \"*.bin\""  # Example
echo
echo "Consider a per-path approach and coordinate with your team before converting history to LFS."
