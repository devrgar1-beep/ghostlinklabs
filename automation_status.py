#!/usr/bin/env python3
"""
GhostLink Automation Status Dashboard
"""

import subprocess
import json
import os
from pathlib import Path

def run_link_cmd(args):
    """Run Link CLI command"""
    cmd = ["/Users/ghost-link-labs/ghostlinklabs/.venv/bin/python3", "-m", "ghostlink.link_cli"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/Users/ghost-link-labs/ghostlinklabs")
    return result

def show_status():
    """Show automation status"""
    print("🤖 GhostLink Automation Status")
    print("=" * 50)

    # Link status
    result = run_link_cmd(["status"])
    if result.returncode == 0:
        try:
            status = json.loads(result.stdout)
            print(f"🔗 Link Active: {'✅' if status.get('active', False) else '❌'}")
            print(f"📋 Pending Tasks: {status.get('pending_tasks', 0)}")
            print(f"✅ Completed Tasks: {status.get('completed_tasks', 0)}")
            print(f"❌ Failed Tasks: {status.get('failed_tasks', 0)}")
        except:
            print("🔗 Link Status: Unknown")
    else:
        print("🔗 Link Status: ❌ Not responding")

    # Shell integration
    result = subprocess.run(["/Users/ghost-link-labs/ghostlinklabs/.venv/bin/python3", "src/enable_shell_integration.py", "status"],
                          capture_output=True, text=True, cwd="/Users/ghost-link-labs/ghostlinklabs")
    if "ACTIVE" in result.stdout:
        print("🐚 Shell Integration: ✅ ACTIVE")
    else:
        print("🐚 Shell Integration: ❌ INACTIVE")

    # Environment variables
    auto_interact = os.getenv("GHOSTLINK_AUTO_INTERACT", "false")
    print(f"⚙️  Auto Interact: {'✅' if auto_interact == 'true' else '❌'}")

    print("\n🎯 Automation Rules:")
    result = run_link_cmd(["learn", "list"])
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print("❌ Could not retrieve learning data")

if __name__ == "__main__":
    show_status()
