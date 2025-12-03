#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/Users/ghostlink"

echo "This script prepares commands to scrub git history of secrets. DO NOT RUN without team coordination."

if ! git -C "$REPO_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Not a git repo: $REPO_DIR"
  exit 1
fi

echo "Recommended steps:"
echo "1) Backup your repo: git clone --mirror file://$REPO_DIR /tmp/ghostlink-mirror.git"
echo "2) Install git-filter-repo: https://github.com/newren/git-filter-repo"
echo "3) Run git-filter-repo to remove files or patterns. Example to remove secrets by path:"
echo "   git -C /tmp/ghostlink-mirror.git filter-repo --invert-paths --paths 'path/to/secret.file'"
echo "4) Force-push cleaned mirror to origin after coordinating with team."

echo
echo "Example BFG usage (alternative):"
echo "  java -jar bfg.jar --delete-files YOUR_SECRET_FILE --no-blob-protection /tmp/ghostlink-mirror.git"

echo
echo "If you want, create a timestamped backup tarball now? (yes/no)"
read -r ans || true
if [ "$ans" = "yes" ]; then
  tar -czf /tmp/ghostlink-backup-$(date +%Y%m%d%H%M%S).tar.gz -C "$REPO_DIR" .
  echo "Backup created."
fi

echo "Script complete. Follow outlined steps carefully."
