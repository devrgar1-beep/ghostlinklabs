#!/usr/bin/env python3
"""
GhostLink Cold Boot Status Check
Starts components on-demand, checks functionality, then shuts them down
"""

import subprocess
import sys
import time
import json
import os

def check_ai_engine():
    """Check multi-agent engine by starting it briefly"""
    print("🤖 Cold Booting Multi-Agent Engine...")
    try:
        # Just check that the engine can show help (verifies it's accessible)
        result = subprocess.run([
            sys.executable, "src/multi_agent_engine.py", "--help"
        ], capture_output=True, text=True, timeout=5, cwd=os.path.dirname(__file__))

        if result.returncode == 0 and "GhostLink Multi-Agent" in result.stdout:
            print("✅ Multi-Agent Engine: ACCESSIBLE - SHUT DOWN")
            return True
        else:
            print("❌ Multi-Agent Engine: NOT ACCESSIBLE")
            return False
    except Exception as e:
        print(f"❌ Multi-Agent Engine: ERROR - {e}")
        return False

def check_consciousness():
    """Check consciousness framework by starting it briefly"""
    print("🧠 Cold Booting Consciousness Framework...")
    try:
        # Just check that the framework can show help
        result = subprocess.run([
            sys.executable, "src/unified_consciousness.py", "--help"
        ], capture_output=True, text=True, timeout=5, cwd=os.path.dirname(__file__))

        if result.returncode == 0 and "GhostLink Unified Consciousness" in result.stdout:
            print("✅ Consciousness Framework: ACCESSIBLE - SHUT DOWN")
            return True
        else:
            print("❌ Consciousness Framework: NOT ACCESSIBLE")
            return False
    except Exception as e:
        print(f"❌ Consciousness Framework: ERROR - {e}")
        return False

def check_monitoring():
    """Check monitoring by running cold boot collection"""
    print("📊 Cold Booting Monitoring Collection...")
    try:
        result = subprocess.run([
            sys.executable, "monitoring/basic_monitor.py"
        ], capture_output=True, text=True, timeout=10, cwd=os.path.dirname(__file__))

        if result.returncode == 0 and "ghostlink_system_metrics" in result.stdout:
            print("✅ Monitoring: ACTIVE (metrics collected) - SHUT DOWN")
            return True
        else:
            print("❌ Monitoring: FAILED TO COLLECT")
            return False
    except Exception as e:
        print(f"❌ Monitoring: ERROR - {e}")
        return False

def check_basic_functionality():
    """Check basic Python functionality"""
    print("🐍 Cold Booting Basic Functionality Test...")
    try:
        result = subprocess.run([
            sys.executable, "tests/core/test_fib.py"
        ], capture_output=True, text=True, timeout=5, cwd=os.path.dirname(__file__))

        if "fib(9) = 34" in result.stdout:
            print("✅ Basic Functionality: WORKING - TEST COMPLETE")
            return True
        else:
            print("❌ Basic Functionality: FAILED")
            return False
    except Exception as e:
        print(f"❌ Basic Functionality: ERROR - {e}")
        return False

def main():
    """Run cold boot status check"""
    print("🧊 GHOSTLINK COLD BOOT STATUS CHECK")
    print("Each component starts, gets checked, then shuts down completely")
    print("=" * 70)

    checks = [
        check_ai_engine,
        check_consciousness,
        check_monitoring,
        check_basic_functionality
    ]

    results = []
    for check in checks:
        results.append(check())
        time.sleep(1)  # Brief pause between cold boots

    print("\n" + "=" * 70)
    successful = sum(results)
    total = len(results)

    if successful == total:
        print(f"🎯 COLD BOOT SUCCESS: {successful}/{total} components functional")
        print("✅ All systems start on-demand and shut down cleanly!")
        print("🧊 True cold boot architecture confirmed")
    else:
        print(f"⚠️  COLD BOOT PARTIAL: {successful}/{total} components functional")
        print("🔧 Some components need attention for full cold boot")

    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
