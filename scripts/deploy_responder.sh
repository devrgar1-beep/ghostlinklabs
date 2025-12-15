#!/usr/bin/env bash
set -euo pipefail

# Deploy gl_peer_responder.py to backbone hosts and start it
# Requirements: SSH access via key auth to each host
#
# Usage:
#   scripts/deploy_responder.sh [inventory_file]
# Env:
#   BACKBONE_USER   SSH user (default: $USER)
#   REMOTE_DIR      Remote dir to place files (default: ~/ghostlink)
#   PORT            Responder port (default: 7422)
#   START_MODE      one of: nohup|systemd (default: nohup)
#
# The script will:
#   - Ensure Python 3 is present (attempt apt/yum/dnf install if sudo available)
#   - Create REMOTE_DIR and copy gl_peer_responder.py
#   - Optionally open firewall port 7422 if ufw/firewalld present (best effort)
#   - Start responder (nohup, or systemd if chosen and sudo permitted)
#   - Verify local TCP connect to port 7422

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
INV_FILE="${1:-$ROOT_DIR/backbone_hosts.txt}"
USER_NAME="${BACKBONE_USER:-$USER}"
REMOTE_DIR="${REMOTE_DIR:-~/ghostlink}"
RESP_PORT="${PORT:-7422}"
START_MODE="${START_MODE:-nohup}"

if [[ ! -f "$INV_FILE" ]]; then
  echo "[deploy] Inventory file not found: $INV_FILE" >&2
  exit 1
fi

mapfile -t HOSTS < <(grep -Ev '^(#|\s*$)' "$INV_FILE")
if [[ ${#HOSTS[@]} -eq 0 ]]; then
  echo "[deploy] No hosts in inventory: $INV_FILE" >&2
  exit 1
fi

copy_and_start_nohup() {
  local host="$1"
  ssh -o BatchMode=yes -o ConnectTimeout=5 "$USER_NAME@$host" "mkdir -p $REMOTE_DIR"
  scp -o BatchMode=yes "$ROOT_DIR/gl_peer_responder.py" "$USER_NAME@$host:$REMOTE_DIR/"
  ssh -o BatchMode=yes "$USER_NAME@$host" "\
    p3=python3; command -v python3 >/dev/null || p3=python; \
    nohup \"$p3\" \"$REMOTE_DIR/gl_peer_responder.py\" > \"$REMOTE_DIR/responder.log\" 2>&1 & disown; sleep 0.5; pgrep -f gl_peer_responder.py >/dev/null && echo OK || echo FAIL"
}

try_install_python() {
  local host="$1"
  ssh -o BatchMode=yes "$USER_NAME@$host" "\
    if command -v python3 >/dev/null; then exit 0; fi; \
    if command -v sudo >/dev/null; then \
      if command -v apt-get >/dev/null; then sudo apt-get update -y && sudo apt-get install -y python3; exit 0; fi; \
      if command -v dnf >/dev/null; then sudo dnf install -y python3; exit 0; fi; \
      if command -v yum >/dev/null; then sudo yum install -y python3; exit 0; fi; \
    fi; exit 0"
}

open_firewall() {
  local host="$1"
  ssh -o BatchMode=yes "$USER_NAME@$host" "\
    if command -v sudo >/dev/null; then \
      if command -v ufw >/dev/null; then sudo ufw allow $RESP_PORT/tcp || true; fi; \
      if command -v firewall-cmd >/dev/null; then sudo firewall-cmd --add-port=$RESP_PORT/tcp --permanent || true; sudo firewall-cmd --reload || true; fi; \
    fi; true"
}

verify_local() {
  local host="$1"
  python3 - "$host" "$RESP_PORT" <<'PY'
import socket, sys
host, port = sys.argv[1], int(sys.argv[2])
s=socket.socket(); s.settimeout(1.0)
try:
    s.connect((host, port))
    print('OK')
except Exception as e:
    print('FAIL:', e)
finally:
    s.close()
PY
}

echo "[deploy] Deploying responder to ${#HOSTS[@]} host(s) from $INV_FILE as $USER_NAME"
FAILS=()
for h in "${HOSTS[@]}"; do
  echo "[deploy] Host: $h"
  try_install_python "$h" || true
  open_firewall "$h" || true
  if [[ "$START_MODE" == "nohup" ]]; then
    res=$(copy_and_start_nohup "$h" || true)
    echo "[deploy] start: $res"
  else
    echo "[deploy] systemd mode not implemented; using nohup"
    res=$(copy_and_start_nohup "$h" || true)
  fi
  v=$(verify_local "$h")
  echo "[deploy] verify: $v"
  if [[ "$v" != "OK" ]]; then FAILS+=("$h"); fi
  echo
done

if [[ ${#FAILS[@]} -gt 0 ]]; then
  echo "[deploy] Completed with failures on: ${FAILS[*]}" >&2
  exit 2
fi

echo "[deploy] All responders deployed and reachable."
