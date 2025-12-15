#!/usr/bin/env bash
# GhostLink Shell Environment Configuration
# Source this in your ~/.bashrc or ~/.zshrc

# Colors
export GL_COLOR_SUCCESS='\033[0;32m'
export GL_COLOR_ERROR='\033[0;31m'
export GL_COLOR_INFO='\033[0;34m'
export GL_COLOR_WARN='\033[1;33m'
export GL_COLOR_RESET='\033[0m'

# GhostLink directory detection
detect_ghostlink_dir() {
    # Try common locations
    if [[ -d "$HOME/Library/Mobile Documents/com~apple~CloudDocs/ghostlinklabs" ]]; then
        echo "$HOME/Library/Mobile Documents/com~apple~CloudDocs/ghostlinklabs"
    elif [[ -d "$HOME/ghostlinklabs" ]]; then
        echo "$HOME/ghostlinklabs"
    elif [[ -d "/opt/ghostlink" ]]; then
        echo "/opt/ghostlink"
    elif [[ -d "/srv/ghostlink" ]]; then
        echo "/srv/ghostlink"
    else
        return 1
    fi
}

# Initialize GhostLink if available
init_ghostlink() {
    local gl_root
    gl_root=$(detect_ghostlink_dir) || return 0

    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$gl_root/bin:"* ]]; then
        export PATH="$gl_root/bin:$PATH"
    fi

    # XDG Base Directory support
    export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
    export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
    export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

    # GhostLink environment
    export GHOSTLINK_HOME="$gl_root"
    export GHOSTLINK_CONFIG_DIR="${GHOSTLINK_CONFIG_DIR:-$XDG_CONFIG_HOME/ghostlink}"
    export GHOSTLINK_DATA_DIR="${GHOSTLINK_DATA_DIR:-$XDG_DATA_HOME/ghostlink}"
    export GHOSTLINK_LOG_DIR="${GHOSTLINK_LOG_DIR:-$XDG_DATA_HOME/ghostlink/logs}"

    # Ensure directories exist
    mkdir -p "$GHOSTLINK_CONFIG_DIR" "$GHOSTLINK_DATA_DIR" "$GHOSTLINK_LOG_DIR" 2>/dev/null || true
}

# Alias definitions
alias gl='ghostlink'
alias glctx='ghostlink context'
alias glask='ghostlink task'
alias glgit='ghostlink git'
alias gldiag='ghostlink diagnostics'
alias gllearn='ghostlink learn'
alias glhistory='ghostlink history'

# Helpful functions
gl-status() {
    echo -e "${GL_COLOR_INFO}GhostLink Status:${GL_COLOR_RESET}"
    ghostlink status
}

gl-quick() {
    cat << 'EOF'
Quick Commands:
  gl status              - Check GhostLink status
  gl task list           - List tasks
  gl task add "desc"     - Add a task
  gl diagnostics health  - Run health check
  gl git status          - Git status
  gl git sync            - Sync with remote
  gl help                - Show full help

Aliases:
  gl          - ghostlink
  glctx       - context commands
  glask       - task commands
  glgit       - git commands
  gldiag      - diagnostics
  gllearn     - learning commands
EOF
}

# Initialize on shell startup
init_ghostlink

# Print welcome message if interactive shell
if [[ $- == *i* ]] && [[ "${GL_INIT_DONE:-}" != "1" ]]; then
    export GL_INIT_DONE=1
    # Uncomment to show welcome message
    # echo -e "${GL_COLOR_SUCCESS}✓ GhostLink initialized${GL_COLOR_RESET}"
fi
