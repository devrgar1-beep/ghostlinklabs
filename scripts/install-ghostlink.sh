#!/usr/bin/env bash
# GhostLink Unix Installation Script
# Installs GhostLink to system paths and configures integrations

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALL_PREFIX="${INSTALL_PREFIX:-/usr/local}"

print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_ok() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check if running as root (for system-wide installation)
    if [[ "$INSTALL_PREFIX" == "/usr"* ]] && [[ "$EUID" != 0 ]]; then
        print_error "System-wide installation requires root privileges"
        echo "Re-run with sudo or use INSTALL_PREFIX=\$HOME/.local to install locally"
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        exit 1
    fi
    print_ok "Python 3 found: $(python3 --version)"

    # Check bash version (need 4+)
    if [[ "${BASH_VERSINFO[0]}" -lt 4 ]]; then
        print_error "Bash 4.0+ required (current: ${BASH_VERSION})"
        exit 1
    fi
    print_ok "Bash version: ${BASH_VERSION}"
}

# Setup Python environment
setup_python_env() {
    print_header "Setting up Python Environment"

    local venv_path="$PROJECT_ROOT/.venv"

    if [[ ! -f "$venv_path/bin/python" ]]; then
        print_info "Creating virtual environment..."
        python3 -m venv "$venv_path"
        print_ok "Virtual environment created"
    else
        print_ok "Virtual environment already exists"
    fi

    # Upgrade pip
    print_info "Upgrading pip..."
    "$venv_path/bin/pip" install -q --upgrade pip setuptools wheel

    # Install requirements
    if [[ -f "$PROJECT_ROOT/requirements.txt" ]]; then
        print_info "Installing dependencies..."
        "$venv_path/bin/pip" install -q -r "$PROJECT_ROOT/requirements.txt"
        print_ok "Dependencies installed"
    fi

    # Install Click if needed for CLI
    "$venv_path/bin/pip" install -q click
    print_ok "CLI dependencies ready"
}

# Install main executable
install_executable() {
    print_header "Installing Executables"

    local bin_dir="$INSTALL_PREFIX/bin"
    mkdir -p "$bin_dir"

    # Install main ghostlink command
    install -m 755 "$PROJECT_ROOT/bin/ghostlink" "$bin_dir/ghostlink"
    print_ok "Installed: $bin_dir/ghostlink"

    # Create symlink for legacy glctl command
    ln -sf "$bin_dir/ghostlink" "$bin_dir/glctl" || true
    print_ok "Symlink created: $bin_dir/glctl → ghostlink"
}

# Install shell completions
install_completions() {
    print_header "Installing Shell Completions"

    local bash_comp_dir
    local zsh_comp_dir

    # Detect bash completion directory
    if [[ -d /etc/bash_completion.d ]]; then
        bash_comp_dir="/etc/bash_completion.d"
    elif [[ -d /usr/local/etc/bash_completion.d ]]; then
        bash_comp_dir="/usr/local/etc/bash_completion.d"
    elif [[ -d /opt/homebrew/etc/bash_completion.d ]]; then
        bash_comp_dir="/opt/homebrew/etc/bash_completion.d"
    fi

    if [[ -n "$bash_comp_dir" && -d "$bash_comp_dir" ]]; then
        install -m 644 "$PROJECT_ROOT/bin/ghostlink.bash-completion.sh" "$bash_comp_dir/ghostlink"
        print_ok "Bash completion installed"
    else
        print_warning "Bash completion directory not found - skipping"
    fi

    # Detect zsh completion directory
    if [[ -d /usr/share/zsh/site-functions ]]; then
        zsh_comp_dir="/usr/share/zsh/site-functions"
    elif [[ -d /usr/local/share/zsh/site-functions ]]; then
        zsh_comp_dir="/usr/local/share/zsh/site-functions"
    elif [[ -d /opt/homebrew/share/zsh/site-functions ]]; then
        zsh_comp_dir="/opt/homebrew/share/zsh/site-functions"
    fi

    if [[ -n "$zsh_comp_dir" && -d "$zsh_comp_dir" ]]; then
        install -m 644 "$PROJECT_ROOT/bin/_ghostlink" "$zsh_comp_dir/_ghostlink"
        print_ok "Zsh completion installed"
    else
        print_warning "Zsh completion directory not found - skipping"
    fi
}

# Install man pages
install_man_pages() {
    print_header "Installing Manual Pages"

    local man_dir="$INSTALL_PREFIX/share/man/man1"
    mkdir -p "$man_dir"

    if [[ -f "$PROJECT_ROOT/man/man1/ghostlink.1" ]]; then
        install -m 644 "$PROJECT_ROOT/man/man1/ghostlink.1" "$man_dir/ghostlink.1"
        print_ok "Man page installed: $man_dir/ghostlink.1"

        # Create symlink for legacy command
        ln -sf "$man_dir/ghostlink.1" "$man_dir/glctl.1" || true
        print_ok "Man symlink created: $man_dir/glctl.1 → ghostlink.1"
    else
        print_warning "Man page not found"
    fi
}

# Install systemd units (user-level)
install_systemd_units() {
    print_header "Installing Systemd Units"

    local systemd_user_dir="$HOME/.config/systemd/user"
    mkdir -p "$systemd_user_dir"

    if [[ -d "$PROJECT_ROOT/systemd" ]]; then
        for unit_file in "$PROJECT_ROOT/systemd"/*.{service,socket,timer}; do
            if [[ -f "$unit_file" ]]; then
                local filename=$(basename "$unit_file")
                # Replace paths for user
                sed "s|%h|$HOME|g; s|%C|$HOME/.config|g; s|%t|/run/user/$(id -u)|g" \
                    "$unit_file" > "$systemd_user_dir/$filename"
                chmod 644 "$systemd_user_dir/$filename"
                print_ok "Installed unit: $systemd_user_dir/$filename"
            fi
        done

        print_info "Run: systemctl --user daemon-reload"
        print_info "Then: systemctl --user enable ghostlink.service"
    else
        print_warning "Systemd directory not found"
    fi
}

# Create configuration
create_config() {
    print_header "Creating Configuration"

    local config_dir="$HOME/.config/ghostlink"
    mkdir -p "$config_dir"

    if [[ ! -f "$config_dir/ghostlink.conf" ]]; then
        cat > "$config_dir/ghostlink.conf" << 'EOF'
# GhostLink Configuration
# Created by installation script

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Performance
WORKERS=auto
TIMEOUT=30

# Networking
BIND_HOST=127.0.0.1
BIND_PORT=8000

# Storage (will be expanded with actual paths)
# DB_PATH will be set to ~/.local/share/ghostlink/ghostlink.db
# STATE_FILE will be set to ~/.local/share/ghostlink/state.json
EOF
        print_ok "Configuration created: $config_dir/ghostlink.conf"
    else
        print_ok "Configuration already exists: $config_dir/ghostlink.conf"
    fi

    # Create data directories
    mkdir -p "$HOME/.local/share/ghostlink/logs"
    mkdir -p "$HOME/.cache/ghostlink"
    print_ok "Data directories created"
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"

    # Check if ghostlink command is available
    if command -v ghostlink &> /dev/null; then
        print_ok "ghostlink command available"
    else
        print_error "ghostlink command not found - ensure $INSTALL_PREFIX/bin is in PATH"
    fi

    # Test ghostlink
    if ghostlink version &> /dev/null; then
        print_ok "ghostlink version: $(ghostlink version | head -1)"
    else
        print_error "Failed to run ghostlink"
    fi

    # Check man page
    if man -k ghostlink &> /dev/null || man ghostlink &> /dev/null 2>&1; then
        print_ok "Man page available"
    else
        print_warning "Man page not accessible - this is OK if installed locally"
    fi
}

# Print post-installation info
print_post_install_info() {
    print_header "Installation Complete!"

    echo ""
    echo -e "${GREEN}GhostLink has been successfully installed.${NC}"
    echo ""

    echo "Quick Start:"
    echo "  • Check status:  ${BLUE}ghostlink status${NC}"
    echo "  • List tasks:    ${BLUE}ghostlink task list${NC}"
    echo "  • View help:     ${BLUE}ghostlink help${NC}"
    echo "  • View manual:   ${BLUE}man ghostlink${NC}"
    echo ""

    echo "Systemd Integration (Linux):"
    echo "  • Enable:        ${BLUE}systemctl --user enable ghostlink${NC}"
    echo "  • Start:         ${BLUE}systemctl --user start ghostlink${NC}"
    echo "  • Status:        ${BLUE}systemctl --user status ghostlink${NC}"
    echo "  • Logs:          ${BLUE}journalctl --user -u ghostlink${NC}"
    echo ""

    echo "Environment:"
    echo "  • Config:        ~/.config/ghostlink/"
    echo "  • Data:          ~/.local/share/ghostlink/"
    echo "  • Logs:          ~/.local/share/ghostlink/logs/"
    echo "  • Cache:         ~/.cache/ghostlink/"
    echo ""

    if [[ "$INSTALL_PREFIX" == "/usr/local" ]]; then
        echo "Note: Installed to $INSTALL_PREFIX"
        echo "Ensure $INSTALL_PREFIX/bin is in your PATH"
    fi

    echo ""
}

# Main installation flow
main() {
    print_header "GhostLink Unix Installation"
    echo "Version: 0.1.0"
    echo "Install Prefix: $INSTALL_PREFIX"
    echo ""

    check_prerequisites
    setup_python_env
    install_executable
    install_completions
    install_man_pages
    install_systemd_units
    create_config
    verify_installation
    print_post_install_info

    print_ok "Installation finished successfully!"
}

# Run main
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
