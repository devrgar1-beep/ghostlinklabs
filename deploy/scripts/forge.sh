#!/bin/bash
# GhostLink Toolbox Forge Launcher for Unix/Linux

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/toolbox_forge.py" "$@"
