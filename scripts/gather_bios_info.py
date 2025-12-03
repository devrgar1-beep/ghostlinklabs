#!/usr/bin/env python3
"""
Gather BIOS and system info via the BIOS bridge in a safe, read-only mode.
This script only reads data and writes a JSON report to `bios_report.json`.
"""
import json
from pathlib import Path

import bios_bridge

REPORT_FILE = Path("bios_report.json")


def main():
    ok = bios_bridge.initialize_bios_bridge()
    report = {"initialized": ok}
    try:
        status = bios_bridge.get_bios_status()
        report["status"] = status
    except Exception as e:
        report["status_error"] = str(e)

    try:
        # Find vendor tools (non-destructive)
        # Access global supergrok_bios instance
        bridge = bios_bridge.supergrok_bios.bridge
        if bridge:
            tools = bridge._find_vendor_tools()
            report["vendor_tools"] = tools
    except Exception as e:
        report["vendor_tools_error"] = str(e)

    REPORT_FILE.write_text(json.dumps(report, indent=2))
    print(f"Report written to {REPORT_FILE}")


if __name__ == "__main__":
    main()
