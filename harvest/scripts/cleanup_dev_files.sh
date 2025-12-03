#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$REPO_ROOT"

echo "Cleaning development files: __pycache__, .pyc, .venv, dist/"
find . -type d -name __pycache__ -print0 | xargs -0 rm -rf || true
find . -type f -name '*.pyc' -print0 | xargs -0 rm -f || true
rm -rf .venv venv dist build '*.egg-info' || true
echo "Cleaned."
