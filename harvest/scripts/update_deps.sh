#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/ghostlink"
cd "$ROOT"

echo "Checking outdated pip packages..."
python3 -m pip list --outdated --format=columns || true

if command -v pip-audit >/dev/null 2>&1; then
  echo "Running pip-audit (vulnerability scan)"
  python -m pip_audit --progress-spinner=off || true
else
  echo "pip-audit not installed. Install via: python -m pip install pip-audit"
fi

echo "If you use pip-tools, you can run: pip-compile --output-file=requirements.txt requirements.in"
