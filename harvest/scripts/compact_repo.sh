#!/usr/bin/env bash
set -euo pipefail

# compact_repo.sh - Listing and optionally archiving large files in the repository
# Usage: ./scripts/compact_repo.sh [--list | --archive] [--threshold MB]

REPO_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$REPO_ROOT"

THRESHOLD_MB=10
ACTION="list"

while [[ $# -gt 0 ]]; do
  case $1 in
    --archive) ACTION="archive"; shift;;
    --list) ACTION="list"; shift;;
    --threshold) THRESHOLD_MB="$2"; shift 2;;
    *) echo "Unknown arg: $1"; exit 1;;
  esac
done

echo "Repo: $REPO_ROOT"
echo "Finding files > ${THRESHOLD_MB}MB..."

mkdir -p tmp-compact-report
REPORT=tmp-compact-report/large-files.txt
> "$REPORT"

# find files larger than threshold and list them
INCLUDE_PATHS=()
EXCLUDE_TOP=(".git" "Library" "Applications" "Desktop" "Downloads" "Pictures" "Movies" "Music")
for d in $(ls -1); do
  if [ -d "$d" ]; then
    skip=false
    for e in "${EXCLUDE_TOP[@]}"; do
      if [ "$d" = "$e" ]; then skip=true; break; fi
    done
    if [ "$skip" = false ]; then INCLUDE_PATHS+=("$d"); fi
  fi
done
echo "Scanning paths: ${INCLUDE_PATHS[*]}"

if command -v gfind >/dev/null 2>&1; then
  # GNU find (gfind) has -printf
  gfind ${INCLUDE_PATHS[@]:-./} -type f -size +${THRESHOLD_MB}M -not -path './.git/*' -printf '%s %p\n' | sort -nr | while read -r size path; do
    mb=$((size/1024/1024))
    echo "$mb MB - $path" | tee -a "$REPORT"
  done
else
  # BSD find (macOS): use stat
  for p in "${INCLUDE_PATHS[@]}"; do
    while IFS= read -r -d '' f; do
      s=$(stat -f "%z" "$f" 2>/dev/null || echo 0)
      MB=$((s/1024/1024))
      printf "%s MB - %s\n" "$MB" "$f" | tee -a "$REPORT"
    done < <(find "$p" -type f -size +${THRESHOLD_MB}M -not -path './.git/*' -print0)
  done
fi

echo
echo "Report saved to $REPORT"

if [ "$ACTION" = "archive" ]; then
  ARCHIVE_DIR=archives/compact-$(date +%Y%m%d%H%M%S)
  mkdir -p "$ARCHIVE_DIR"
  echo "Archiving large files (copying to $ARCHIVE_DIR) and replacing with .gz copies..."
  while IFS= read -r line; do
    if [[ "$line" =~ MB\ -\ (.*)$ ]]; then
      fpath=${BASH_REMATCH[1]}
      if [ -f "$fpath" ]; then
        cp -p "$fpath" "$ARCHIVE_DIR/"
        gzip -9 -c "$fpath" > "$fpath.gz"
        rm -f "$fpath"
        echo "Archived and compressed: $fpath -> $ARCHIVE_DIR/" | tee -a "$REPORT"
      fi
    fi
  done < "$REPORT"
  echo "Archiving complete. Check the archive directory and consider adding original paths to .gitignore or moving to external storage." | tee -a "$REPORT"
fi

echo "Done."
