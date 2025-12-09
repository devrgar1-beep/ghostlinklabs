import subprocess
import sys


def run(cmd):
    return subprocess.run(
        cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )


def test_cold_boot_status_runs():
    # Run cold boot status check - ok if exit code 0 or 1 as it may report 'ISSUES'
    res = run([sys.executable, "cold_boot_orchestrator.py", "status"])
    assert res.returncode in (0, 1)
    assert res.stdout.strip() != ""
