#!/usr/bin/env bash
set -euo pipefail

# prune_cache.sh - clear local caches (pip, poetry, npm) and docker prune suggestion.
# Usage: ./scripts/prune_cache.sh [--yes]

YES="false"
if [[ ${1:-} == "--yes" ]]; then YES="true"; fi

echo "Pruning local caches. This only deletes local cache directories."
if [[ "$YES" != "true" ]]; then
  read -p "Continue? [y/N] " yn
  case $yn in
    [Yy]* ) ;;
    * ) echo "Aborted"; exit 1;;
  esac
fi

PIP_CACHE=$(python3 -c 'import site, os; path = os.path.expanduser("~/.cache/pip"); print(path)')
echo "Clearing pip cache: $PIP_CACHE"
rm -rf "$PIP_CACHE" || true

POETRY_CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/pypoetry"
echo "Clearing poetry cache: $POETRY_CACHE"
rm -rf "$POETRY_CACHE" || true

NPM_CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/npm"
echo "Clearing npm cache: $NPM_CACHE"
rm -rf "$NPM_CACHE" || true

echo "If you use Docker, consider running 'docker system prune -a' to free space (requires Docker CLI)."

echo "Done."
