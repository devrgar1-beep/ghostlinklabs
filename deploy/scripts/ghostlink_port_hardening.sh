#!/usr/bin/env bash
set -euo pipefail

# Apply minimal port hardening for GhostLink
# This script configures UFW or firewalld to limit exposure to loopback only for control/metrics ports.

PORTS=(7420 7422 9108)

if command -v ufw >/dev/null 2>&1; then
  echo "[*] Configuring UFW rules..."
  ufw --force reset
  ufw default deny incoming
  ufw default allow outgoing
  for port in "${PORTS[@]}"; do
    ufw deny proto tcp from any to any port $port
    ufw allow proto tcp from 127.0.0.1 to any port $port
  done
  ufw --force enable
  echo "[✓] UFW rules applied. Listening ports restricted to loopback."
elif command -v firewall-cmd >/dev/null 2>&1; then
  echo "[*] Configuring firewalld rules..."
  # deny each port in public zone, add allow for 127.0.0.1 via rich rule
  for port in "${PORTS[@]}"; do
    firewall-cmd --permanent --zone=public --remove-port=${port}/tcp || true
    firewall-cmd --permanent --add-rich-rule "rule family=ipv4 source address=127.0.0.1/32 port port=${port} protocol=tcp accept"
  done
  firewall-cmd --reload
  echo "[✓] firewalld rules applied. Listening ports restricted to loopback."
else
  echo "[!] No ufw or firewalld detected. Please restrict ports manually."
  exit 2
fi
