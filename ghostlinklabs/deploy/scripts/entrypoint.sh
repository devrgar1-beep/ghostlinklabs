#!/usr/bin/env bash
set -euo pipefail

# Modern GhostLink entrypoint script
# Runs the unified GhostLink system with proper environment setup

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

# 90s Style ASCII Banner
banner() {
    echo -e "\e[1;32m"  # Bright green
    cat << 'EOF'
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   _____ _           _   _      _     _     _                  ║
║  / ____| |         | | | |    (_)   | |   | |                 ║
║ | |  __| |__   ___ | |_| | ___ _ ___| | __| |                 ║
║ | | |_ | '_ \ / _ \| __| |/ _ \ | / _ \ |/ _` |                ║
║ | |__| | | | | (_) | |_| |  __/ ||  __/ | (_| |               ║
║  \_____|_| |_|\___/ \__|_|\___|_| \___|_|\__,_|               ║
║                                                              ║
║                 GHOSTLINK LABS - 2025                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
EOF
    echo -e "\e[0m"  # Reset colors
}

# Set default environment variables
export HOST="${HOST:-0.0.0.0}"
export PORT="${PORT:-8000}"
export LOG_LEVEL="${LOG_LEVEL:-INFO}"
export DEBUG="${DEBUG:-false}"
export PYTHONPATH="${PYTHONPATH:-/app}"

# Create necessary directories
mkdir -p /app/logs /app/data /app/models

# Database setup
if [[ "${DATABASE_URL:-}" == sqlite* ]]; then
    DB_PATH=$(echo "$DATABASE_URL" | sed 's|sqlite:///\./|/app/|')
    mkdir -p "$(dirname "$DB_PATH")"
fi

# Redis connection check (if enabled)
if [[ "${REDIS_URL:-}" ]]; then
    log "Checking Redis connection..."
    if ! timeout 10 bash -c "</dev/tcp/$(echo "$REDIS_URL" | sed 's|redis://||' | sed 's|:.*||')/$(echo "$REDIS_URL" | sed 's|.*:||')" 2>/dev/null; then
        log "WARN: Redis not available at $REDIS_URL"
    else
        log "Redis connection successful"
    fi
fi

# Health check function
health_check() {
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "http://localhost:$PORT/health" > /dev/null 2>&1; then
            log "Health check passed"
            return 0
        fi

        log "Health check attempt $attempt/$max_attempts failed, retrying..."
        sleep 2
        ((attempt++))
    done

    log "Health check failed after $max_attempts attempts"
    return 1
}

# Pre-flight checks
log "Running pre-flight checks..."

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "/opt/venv" ]]; then
    log "WARN: Not running in expected virtual environment"
fi

# Check Python availability
if ! python --version >/dev/null 2>&1; then
    log "ERROR: Python not found"
    exit 1
fi

log "Python version: $(python --version)"

# Check if ghostlink module is available
if ! python -c "import ghostlink" >/dev/null 2>&1; then
    log "ERROR: ghostlink module not found"
    exit 1
fi

log "Starting GhostLink unified system..."

# Display 90s style banner
banner

# Set Python environment
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Start the main application
if [[ "${DEBUG:-false}" == "true" ]]; then
    log "Starting in DEBUG mode"
    exec python -m ghostlink.main
else
    log "Starting GhostLink system on $HOST:$PORT"
    exec python -m ghostlink.main
fi
