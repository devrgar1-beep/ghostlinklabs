#!/usr/bin/env bash
set -euo pipefail

# Quick repo secret scan helper
ROOT_DIR="/Users/ghostlink"
echo "Running ripgrep for common secret patterns..."
rg --hidden --no-ignore-vcs "(AKIA|aws_secret|AWS_SECRET_ACCESS_KEY|PRIVATE_KEY|SECRET|PASSWORD|pass|passwd|token|api_key|apikey)" "$ROOT_DIR" || true

if command -v gitleaks >/dev/null 2>&1; then
  echo "Running gitleaks..."
  gitleaks detect --source "$ROOT_DIR" --config "/Users/ghostlink/.gitleaks.toml" --report-format json --report-path /tmp/gitleaks-report.json || true
  echo "gitleaks report: /tmp/gitleaks-report.json"
else
  echo "gitleaks not installed. Install with: brew install gitleaks (macOS) or refer to https://github.com/zricethezav/gitleaks"
fi

echo "Done. Review /tmp/gitleaks-report.json if present."
