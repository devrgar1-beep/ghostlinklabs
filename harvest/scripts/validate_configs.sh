#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/ghostlink"
PATTERNS=("PASSWORD" "SECRET" "AWS_SECRET_ACCESS_KEY" "AWS_ACCESS_KEY_ID" "api_key" "apikey" "TOKEN")
FOUND=0

echo "Validating config files for plaintext secrets..."
for f in "$ROOT"/*.ini "$ROOT"/*.yml "$ROOT"/*.yaml "$ROOT"/docker-compose*.yml; do
  [ -f "$f" ] || continue
  for p in "${PATTERNS[@]}"; do
    if rg -n --hidden -i "$p" "$f" >/dev/null 2>&1; then
      echo "[WARN] Possible secret pattern '$p' found in $f"
      FOUND=1
    fi
  done
done

if [ "$FOUND" -ne 0 ]; then
  echo "Validation failed: plaintext secrets detected in configs. Review and remediate before committing."
  exit 2
fi

echo "No plaintext secret patterns detected in top-level configs. Note: this is not exhaustive."
