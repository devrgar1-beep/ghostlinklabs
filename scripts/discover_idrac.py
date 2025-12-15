#!/usr/bin/env python3
"""Discover iDRAC endpoints on management network via Redfish.

Scans given CIDR(s) for Dell iDRAC interfaces by probing HTTPS port 443
and validating Redfish service root. Writes discovered iDRACs to inventory.

Usage:
  python3 scripts/discover_idrac.py 10.10.100.0/24 [192.168.1.0/24 ...]

Outputs discovered iDRACs to stdout and updates idrac_inventory.txt.

Env:
  OUT_FILE       Path to output file (default: ./idrac_inventory.txt)
  PORT           HTTPS port to probe (default: 443)
  TIMEOUT        Connect timeout seconds (default: 2.0)
  WORKERS        Parallel workers (default: 128)
  VERIFY_SSL     Verify SSL certs (default: 0, skip verification)
"""
from __future__ import annotations
import ipaddress
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except ImportError:
    print("Error: requests library required. Install: pip install requests urllib3", file=sys.stderr)
    sys.exit(1)

PORT = int(os.getenv("PORT", "443"))
TIMEOUT = float(os.getenv("TIMEOUT", "2.0"))
WORKERS = int(os.getenv("WORKERS", "128"))
VERIFY_SSL = os.getenv("VERIFY_SSL", "0") == "1"
OUT_FILE = os.getenv("OUT_FILE", os.path.join(os.path.dirname(__file__), "..", "idrac_inventory.txt"))


def probe_idrac(ip: str) -> tuple[str, dict[str, Any] | None]:
    """Probe IP for Redfish service root and return iDRAC info if found."""
    url = f"https://{ip}:{PORT}/redfish/v1/"
    try:
        r = requests.get(url, timeout=TIMEOUT, verify=VERIFY_SSL)
        if r.status_code == 200:
            data = r.json()
            # Check for Dell/iDRAC signatures
            oem = data.get("Oem", {})
            if "Dell" in oem or "dell" in str(data).lower():
                return ip, {
                    "redfish_version": data.get("RedfishVersion", ""),
                    "product": data.get("Product", ""),
                    "uuid": data.get("UUID", ""),
                }
    except Exception:
        pass
    return ip, None


def ips_from_cidr(cidr: str):
    """Generate all host IPs from CIDR notation."""
    net = ipaddress.ip_network(cidr, strict=False)
    for ip in net.hosts():
        yield str(ip)


def load_existing_inventory(path: str) -> dict[str, str]:
    """Load existing inventory to preserve manual entries. Returns dict: idrac_ip -> full_line."""
    existing = {}
    if not os.path.exists(path):
        return existing
    with open(path, "r") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = stripped.split(",")
            if len(parts) >= 3:
                idrac_ip = parts[2].strip()
                existing[idrac_ip] = stripped
    return existing


def write_inventory(path: str, discovered: list[str], existing: dict[str, str]):
    """Write inventory file, preserving existing entries and appending new discoveries."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    
    # Read header lines
    header_lines = []
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                if line.strip().startswith("#") or not line.strip():
                    header_lines.append(line.rstrip())
                else:
                    break
    
    with open(path, "w") as f:
        # Write header
        for h in header_lines:
            f.write(h + "\n")
        if not header_lines:
            f.write("# iDRAC Management Network Inventory\n")
            f.write("# Format: hostname,data_ip,idrac_ip,idrac_user,location\n")
        
        # Write existing entries
        for line in existing.values():
            f.write(line + "\n")
        
        # Append newly discovered (not in existing)
        new_count = 0
        for idrac_ip in sorted(discovered, key=lambda s: tuple(int(p) for p in s.split('.'))):
            if idrac_ip not in existing:
                # Placeholder entry for manual completion
                f.write(f"r630-auto-{idrac_ip.replace('.', '-')},UNKNOWN,{idrac_ip},root,auto-discovered\n")
                new_count += 1
        
        if new_count:
            print(f"[discover_idrac] Added {new_count} new entries to {path}")


def main(argv: list[str]):
    if len(argv) < 2:
        print(__doc__)
        return 2
    
    cidrs = argv[1:]
    to_scan = []
    for c in cidrs:
        try:
            to_scan.extend(list(ips_from_cidr(c)))
        except Exception as e:
            print(f"[discover_idrac] Skipping invalid CIDR {c}: {e}", file=sys.stderr)
    
    if not to_scan:
        print("[discover_idrac] No IPs to scan.", file=sys.stderr)
        return 1
    
    print(f"[discover_idrac] Scanning {len(to_scan)} IPs on port {PORT} with {WORKERS} workers, timeout={TIMEOUT}s")
    
    found = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(probe_idrac, ip) for ip in to_scan]
        for fut in as_completed(futs):
            ip, info = fut.result()
            if info:
                found.append(ip)
                product = info.get("product", "Unknown")
                version = info.get("redfish_version", "")
                print(f"{ip}  [{product}] Redfish {version}")
    
    if found:
        existing = load_existing_inventory(OUT_FILE)
        write_inventory(OUT_FILE, found, existing)
        print(f"[discover_idrac] Discovered {len(found)} iDRAC(s), updated {OUT_FILE}")
    else:
        print("[discover_idrac] No iDRACs discovered.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
