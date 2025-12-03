#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/ghostlink"
FILES=("$ROOT/ghostlink.ini" "$ROOT/triad_synergy.ini" "$ROOT/docker-compose.yml" "$ROOT/Dockerfile")

echo "Creating .example copies with secrets replaced by placeholders"
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    out="$f.example"
    echo "Processing $f -> $out"
    sed -E \
      -e 's/([A-Za-z_]*PASSWORD[A-Za-z_]*\s*[=:]\s*).*/\1REPLACE_ME/gI' \
      -e 's/([A-Za-z_]*SECRET[A-Za-z_]*\s*[=:]\s*).*/\1REPLACE_ME/gI' \
      -e 's/(AWS_ACCESS_KEY_ID\s*[=:]\s*).*/\1REPLACE_ME/g' \
      -e 's/(AWS_SECRET_ACCESS_KEY\s*[=:]\s*).*/\1REPLACE_ME/g' \
      -e 's/(api[_-]?key\s*[=:]\s*).*/\1REPLACE_ME/gi' \
      "$f" > "$out" || true
  fi
done

echo "Created .example files. Please review and replace REPLACE_ME placeholders with runtime secret injection. Originals left untouched."
