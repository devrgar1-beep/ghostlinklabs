#!/bin/bash
set -e

# Build and run the Docker Compose stack
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR/docker" || exit 1

echo "🔧 Building and starting GhostLink Docker stack..."

docker compose build

docker compose up -d

echo "✅ Docker stack started. API: http://localhost:8000 | Dashboard: http://localhost:3000"

echo "Use: docker compose down to stop the stack"
