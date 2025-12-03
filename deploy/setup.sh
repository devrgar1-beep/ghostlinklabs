#!/usr/bin/env bash
set -euo pipefail

# GhostLink System Setup Script
# Installs systemd services and configures the system

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
USER="ghostlink"
GROUP="ghostlink"
INSTALL_DIR="/opt/ghostlink"
LOG_DIR="/var/log/ghostlink"

echo "=== GhostLink System Setup ==="

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: This script must be run as root"
    exit 1
fi

# Create user and group
if ! id "$USER" &>/dev/null; then
    echo "Creating user ${USER}..."
    useradd -r -s /usr/sbin/nologin -d "${INSTALL_DIR}" "${USER}"
fi

# Create directories
echo "Creating directories..."
mkdir -p "${INSTALL_DIR}"
mkdir -p "${LOG_DIR}"

# Copy project files
echo "Copying project files..."
rsync -av --exclude='.git' --exclude='__pycache__' --exclude='.venv' \
    "${PROJECT_ROOT}/" "${INSTALL_DIR}/"

# Set ownership
chown -R "${USER}:${GROUP}" "${INSTALL_DIR}"
chown -R "${USER}:${GROUP}" "${LOG_DIR}"

# Create virtualenv
echo "Setting up Python virtualenv..."
sudo -u "${USER}" python3 -m venv "${INSTALL_DIR}/.venv"
sudo -u "${USER}" "${INSTALL_DIR}/.venv/bin/pip" install --upgrade pip
sudo -u "${USER}" "${INSTALL_DIR}/.venv/bin/pip" install -r "${INSTALL_DIR}/requirements.txt" || true
sudo -u "${USER}" "${INSTALL_DIR}/.venv/bin/pip" install -r "${INSTALL_DIR}/backend/requirements.txt"
sudo -u "${USER}" "${INSTALL_DIR}/.venv/bin/pip" install prometheus-client

# Install systemd services
echo "Installing systemd services..."
cp "${SCRIPT_DIR}/systemd/ghostlink-controller.service" /etc/systemd/system/
cp "${SCRIPT_DIR}/systemd/ghostlink-backend.service" /etc/systemd/system/

# Reload systemd
systemctl daemon-reload

# Enable services
echo "Enabling services..."
systemctl enable ghostlink-controller.service
systemctl enable ghostlink-backend.service

# Start services
echo "Starting services..."
systemctl start ghostlink-controller.service
systemctl start ghostlink-backend.service

# Check status
echo ""
echo "=== Service Status ==="
systemctl status ghostlink-controller.service --no-pager || true
systemctl status ghostlink-backend.service --no-pager || true

echo ""
echo "✓ Setup complete!"
echo ""
echo "Useful commands:"
echo "  systemctl status ghostlink-controller"
echo "  systemctl status ghostlink-backend"
echo "  journalctl -u ghostlink-controller -f"
echo "  journalctl -u ghostlink-backend -f"
