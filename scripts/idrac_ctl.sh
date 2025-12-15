#!/usr/bin/env bash
set -euo pipefail

# iDRAC Control Script - Power and provisioning operations via Redfish
#
# Usage:
#   scripts/idrac_ctl.sh <command> <idrac_host> [args...]
#
# Commands:
#   status <host>                   Show power state and health
#   power-on <host>                 Power on system
#   power-off <host> [graceful]     Power off (default: graceful shutdown)
#   power-cycle <host>              Hard power cycle (ForceRestart)
#   reset <host> [graceful]         Reboot (default: graceful)
#   boot-pxe <host>                 Set one-time PXE boot and power on
#   boot-hdd <host>                 Set persistent HDD boot
#   thermal <host>                  Show temperature sensors
#   health <host>                   Show health status and recent SEL entries
#   mount-iso <host> <iso_url>      Mount ISO to virtual media
#   unmount-iso <host>              Unmount virtual media
#
# Environment:
#   IDRAC_CREDS_FILE    Path to credentials JSON (default: creds/idrac_creds.json)
#
# Examples:
#   scripts/idrac_ctl.sh status 10.10.100.21
#   scripts/idrac_ctl.sh power-on 10.10.100.21
#   scripts/idrac_ctl.sh boot-pxe 10.10.100.22
#   scripts/idrac_ctl.sh thermal 10.10.100.23

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
CREDS_FILE="${IDRAC_CREDS_FILE:-$ROOT_DIR/creds/idrac_creds.json}"

if [[ ! -f "$ROOT_DIR/gl_idrac.py" ]]; then
  echo "[idrac_ctl] Error: gl_idrac.py not found in $ROOT_DIR" >&2
  exit 1
fi

if [[ ! -f "$CREDS_FILE" ]]; then
  echo "[idrac_ctl] Error: credentials file not found: $CREDS_FILE" >&2
  echo "[idrac_ctl] Create it with template: {\"hosts\": [{\"host\": \"...\", \"username\": \"root\", \"password\": \"...\"}]}" >&2
  exit 1
fi

usage() {
  sed -n '3,25p' "$0" | sed 's/^# //' | sed 's/^#//'
}

cmd="${1:-}"
host="${2:-}"

if [[ -z "$cmd" || -z "$host" ]]; then
  usage
  exit 2
fi

cd "$ROOT_DIR"

case "$cmd" in
  status)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys, json
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
info = client.get_system_info()
power = client.get_power_state()
health = client.get_health_status()
print(f"Host: {host}")
print(f"Model: {info.get('Model', 'Unknown')}")
print(f"Power: {power}")
print(f"Health: {health['health']} / State: {health['state']}")
PY
    ;;

  power-on)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
print(f"[idrac_ctl] Powering on {host}...")
client.power_on()
print("[idrac_ctl] Command sent. Wait 30s for boot.")
PY
    ;;

  power-off)
    graceful="${3:-graceful}"
    python3 - "$host" "$CREDS_FILE" "$graceful" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file, graceful = sys.argv[1], sys.argv[2], sys.argv[3]
client = get_client(host, creds_file)
is_graceful = graceful.lower() in ["graceful", "true", "1"]
print(f"[idrac_ctl] Powering off {host} ({'graceful' if is_graceful else 'force'})...")
client.power_off(graceful=is_graceful)
print("[idrac_ctl] Command sent.")
PY
    ;;

  power-cycle)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
print(f"[idrac_ctl] Power cycling {host} (hard reset)...")
client.power_cycle()
print("[idrac_ctl] Command sent. Wait 60s for reboot.")
PY
    ;;

  reset)
    graceful="${3:-graceful}"
    python3 - "$host" "$CREDS_FILE" "$graceful" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file, graceful = sys.argv[1], sys.argv[2], sys.argv[3]
client = get_client(host, creds_file)
is_graceful = graceful.lower() in ["graceful", "true", "1"]
print(f"[idrac_ctl] Resetting {host} ({'graceful' if is_graceful else 'force'})...")
client.power_reset(graceful=is_graceful)
print("[idrac_ctl] Command sent.")
PY
    ;;

  boot-pxe)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
print(f"[idrac_ctl] Setting one-time PXE boot on {host}...")
client.set_boot_once_pxe()
power = client.get_power_state()
if power.lower() != "on":
    print(f"[idrac_ctl] System is {power}, powering on...")
    client.power_on()
print("[idrac_ctl] PXE boot configured. System will boot from network.")
PY
    ;;

  boot-hdd)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
print(f"[idrac_ctl] Setting persistent HDD boot on {host}...")
client.set_boot_hdd()
print("[idrac_ctl] Boot order set to HDD.")
PY
    ;;

  thermal)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
temps = client.get_temperatures()
fans = client.get_fans()
print(f"Host: {host}")
print("Temperatures:")
for t in temps:
    status_mark = "✓" if t['status'] == "OK" else "⚠"
    print(f"  {status_mark} {t['name']}: {t['reading_c']}°C ({t['status']})")
print("Fans:")
for f in fans:
    status_mark = "✓" if f['status'] == "OK" else "⚠"
    print(f"  {status_mark} {f['name']}: {f['reading_rpm']} RPM ({f['status']})")
PY
    ;;

  health)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
health = client.get_health_status()
psus = client.get_power_supplies()
logs = client.get_log_entries(max_entries=10)
print(f"Host: {host}")
print(f"Health: {health['health']} / State: {health['state']}")
print("Power Supplies:")
for p in psus:
    status_mark = "✓" if p['status'] == "OK" else "⚠"
    print(f"  {status_mark} {p['name']}: {p['status']} ({p.get('power_output_watts', 'N/A')}W)")
print("Recent SEL Entries:")
for log in logs[:5]:
    print(f"  [{log['severity']}] {log['created']}: {log['message'][:60]}")
PY
    ;;

  mount-iso)
    iso_url="${3:-}"
    if [[ -z "$iso_url" ]]; then
      echo "[idrac_ctl] Error: ISO URL required" >&2
      echo "Usage: $0 mount-iso <host> <iso_url>" >&2
      exit 2
    fi
    python3 - "$host" "$CREDS_FILE" "$iso_url" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file, iso_url = sys.argv[1], sys.argv[2], sys.argv[3]
client = get_client(host, creds_file)
print(f"[idrac_ctl] Mounting ISO on {host}: {iso_url}")
client.mount_virtual_media("CD", iso_url)
print("[idrac_ctl] ISO mounted. Set boot to CD via boot-pxe or iDRAC console.")
PY
    ;;

  unmount-iso)
    python3 - "$host" "$CREDS_FILE" <<'PY'
import sys
from gl_idrac import get_client
host, creds_file = sys.argv[1], sys.argv[2]
client = get_client(host, creds_file)
print(f"[idrac_ctl] Unmounting virtual media on {host}...")
client.unmount_virtual_media("CD")
print("[idrac_ctl] Virtual media unmounted.")
PY
    ;;

  *)
    echo "[idrac_ctl] Unknown command: $cmd" >&2
    usage
    exit 2
    ;;
esac
