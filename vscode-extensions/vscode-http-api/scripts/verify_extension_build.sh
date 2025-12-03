#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm not found. Install Node.js/npm and re-run this script."
  exit 2
fi

echo "Installing npm deps..."
npm install --no-audit --no-fund

echo "Compiling TypeScript..."
npm run compile

echo "All good: TypeScript compiled. Check extension package with VSIX or run on a dev host." 
