#!/usr/bin/env bash
set -euo pipefail

# setup_light_env.sh - set up a minimal environment with base requirements in a virtualenv
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"

VENV=${1:-venv}
python3 -m venv "$VENV"
source "$VENV/bin/activate"
pip install -U pip
pip install -r ghostlink_gui/backend/requirements-base.txt

echo "Minimal environment ready: activate with 'source $VENV/bin/activate'"
