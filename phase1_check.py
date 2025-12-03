#!/usr/bin/env python3
"""
GhostLink Phase 1 Status Check
Verifies all Phase 1 components are operational
"""

import subprocess
import sys
import time
import requests
import os

def check_ai_engine():
    """Check if multi-agent engine is responsive"""
    print("🤖 Checking Multi-Agent Engine...")
    try:
        result = subprocess.run([
            sys.executable, "src/multi_agent_engine.py"
        ], capture_output=True, text=True, timeout=10, cwd=os.path.dirname(__file__))

        if "GhostLink Multi-Agent" in result.stdout and "Active Agents: 6" in result.stdout:
            print("✅ Multi-Agent Engine: ACTIVE (6 agents)")
            return True
        else:
            print("❌ Multi-Agent Engine: NOT RESPONDING")
            return False
    except Exception as e:
        print(f"❌ Multi-Agent Engine: ERROR - {e}")
        return False

def check_consciousness():
    """Check if consciousness framework is active"""
    print("🧠 Checking Consciousness Framework...")
    try:
        result = subprocess.run([
            sys.executable, "src/unified_consciousness.py"
        ], capture_output=True, text=True, timeout=15, cwd=os.path.dirname(__file__))

        if "Unified consciousness framework active" in result.stdout and "moderate_awareness" in result.stdout:
            print("✅ Consciousness Framework: ACTIVE (moderate awareness)")
            return True
        else:
            print("❌ Consciousness Framework: NOT RESPONDING")
            return False
    except Exception as e:
        print(f"❌ Consciousness Framework: ERROR - {e}")
        return False

def check_monitoring():
    """Check if monitoring server is running"""
    print("📊 Checking Monitoring Server...")
    try:
        response = requests.get("http://localhost:8000/metrics", timeout=5)
        if response.status_code == 200 and "ghostlink" in response.text:
            print("✅ Monitoring Server: ACTIVE (metrics exposed)")
            return True
        else:
            print("❌ Monitoring Server: NOT RESPONDING")
            return False
    except Exception as e:
        print(f"❌ Monitoring Server: ERROR - {e}")
        return False

def check_basic_functionality():
    """Check basic Python functionality"""
    print("🐍 Checking Basic Functionality...")
    try:
        result = subprocess.run([
            sys.executable, "tests/core/test_fib.py"
        ], capture_output=True, text=True, timeout=5, cwd=os.path.dirname(__file__))

        if "fib(9) = 34" in result.stdout:
            print("✅ Basic Functionality: WORKING")
            return True
        else:
            print("❌ Basic Functionality: FAILED")
            return False
    except Exception as e:
        print(f"❌ Basic Functionality: ERROR - {e}")
        return False

def main():
    """Run Phase 1 status check"""
    print("🚀 GHOSTLINK PHASE 1 STATUS CHECK")
    print("=" * 50)

    checks = [
        check_ai_engine,
        check_consciousness,
        check_monitoring,
        check_basic_functionality
    ]

    results = []
    for check in checks:
        results.append(check())
        time.sleep(1)  # Brief pause between checks

    print("\n" + "=" * 50)
    successful = sum(results)
    total = len(results)

    if successful == total:
        print(f"🎯 PHASE 1 SUCCESS: {successful}/{total} components active")
        print("✅ GhostLink system is ready for Phase 2!")
    else:
        print(f"⚠️  PHASE 1 PARTIAL: {successful}/{total} components active")
        print("🔧 Some components need attention before proceeding")

    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)