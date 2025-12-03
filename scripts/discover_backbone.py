#!/usr/bin/env python3
"""Discover GhostLink responders (port 7422) on given CIDR(s).

Usage:
  python3 scripts/discover_backbone.py 192.168.4.0/22 [10.10.0.0/24 ...]

Outputs discovered IPs to stdout and writes creds/neighbors.txt by default.
Env:
  OUT_FILE   Path to output file (default: ./creds/neighbors.txt)
  PORT       TCP port to probe (default: 7422)
  TIMEOUT    Connect timeout seconds (default: 0.5)
  WORKERS    Parallel workers (default: 256)
"""
from __future__ import annotations
import ipaddress
import os
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

PORT = int(os.getenv("PORT", "7422"))
TIMEOUT = float(os.getenv("TIMEOUT", "0.5"))
WORKERS = int(os.getenv("WORKERS", "256"))
OUT_FILE = os.getenv("OUT_FILE", os.path.join(os.path.dirname(__file__), "..", "creds", "neighbors.txt"))


def probe(ip: str) -> tuple[str, bool]:
    s = socket.socket()
    s.settimeout(TIMEOUT)
    try:
        s.connect((ip, PORT))
        return ip, True
    except Exception:
        return ip, False
    finally:
        s.close()


def ips_from_cidr(cidr: str):
    net = ipaddress.ip_network(cidr, strict=False)
    for ip in net.hosts():
        yield str(ip)


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
            print(f"[discover] Skipping invalid CIDR {c}: {e}")

    if not to_scan:
        print("[discover] No IPs to scan.")
        return 1

    print(f"[discover] Scanning {len(to_scan)} hosts on port {PORT} with {WORKERS} workers, timeout={TIMEOUT}s")

    found = []
    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futs = [ex.submit(probe, ip) for ip in to_scan]
        for fut in as_completed(futs):
            ip, ok = fut.result()
            if ok:
                found.append(ip)
                print(ip)

    if found:
        out_path = os.path.abspath(OUT_FILE)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            for ip in sorted(found, key=lambda s: tuple(int(p) for p in s.split('.'))):
                f.write(ip + "\n")
        print(f"[discover] Wrote {len(found)} neighbors to {out_path}")
    else:
        print("[discover] No responders discovered.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
