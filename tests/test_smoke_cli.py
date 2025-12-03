import subprocess
import sys


def run(cmd):
    return subprocess.run(
        cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )


def test_link_cli_status():
    res = run(
        [sys.executable, "-m", "ghostlink.link_cli", "status"]
    )  # Should run even if not active
    assert res.returncode == 0
    assert "Status" in res.stdout or "Link Status" in res.stdout or res.stdout.strip() != ""


def test_link_cli_diagnostics_health():
    res = run([sys.executable, "-m", "ghostlink.link_cli", "diagnostics", "health"])
    # diagnostics may show different statuses; we just need it to return successfully
    assert res.returncode == 0
