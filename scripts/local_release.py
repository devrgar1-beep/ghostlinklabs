#!/usr/bin/env python3
"""
GhostLink Local Release Helper

Automates the steps to prepare and verify a real‑world local installation:
- (optional) Guide for venv
- pip install .
- Run CLI smoke tests for status and diagnostics
"""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=str(ROOT))


def main() -> int:
    print("=== GhostLink Local Release Helper ===")
    print(f"Repo root: {ROOT}")

    # 1. Ensure we are in a virtualenv (optional but recommended)
    if sys.prefix == sys.base_prefix:
        print(
            "\n[WARN] You are not in a virtualenv.\n"
            "       It is strongly recommended to run inside .venv, e.g.:\n"
            "         python -m venv .venv\n"
            "         source .venv/bin/activate\n"
        )

    # 2. Install runtime requirements and the package locally
    print("\n[STEP] Installing runtime requirements from requirements.txt...")
    code = run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    if code != 0:
        print("[ERROR] pip install -r requirements.txt failed")
        return code
    print("\n[STEP] Installing ghostlink into current environment...")
    code = run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    if code != 0:
        return code
    code = run([sys.executable, "-m", "pip", "install", "."])
    if code != 0:
        print("[ERROR] pip install . failed")
        return code

    # 3. Smoke test the CLI
    print("\n[STEP] Running CLI smoke tests...")
    smoke_cmds = [
        [sys.executable, "-m", "ghostlink.link_cli", "status"],
        [sys.executable, "-m", "ghostlink.link_cli", "diagnostics", "health"],
    ]
    for cmd in smoke_cmds:
        code = run(cmd)
        if code != 0:
            print(f"[WARN] Command failed: {' '.join(cmd)} (exit {code})")

    # Check where console scripts were installed (if any)
    try:
        import shutil

        installed_cli = shutil.which("ghostlink") or shutil.which("ghostlink-link")
        if installed_cli:
            print(f"\n[OK] Console script found at: {installed_cli}")
        else:
            print(
                "\n[INFO] No console script found on PATH. If you want a short CLI command, ensure user script directory is on PATH.\n"
                "For example, add: $HOME/Library/Python/3.9/bin to your shell PATH on macOS."
            )
    except Exception:
        pass

    # 4. Optional: Run cold boot status/health checks (safe, quick status by default)
    run_cold_boot = False
    if "--cold-boot" in sys.argv:
        run_cold_boot = True

    if run_cold_boot:
        print("\n[STEP] Running cold boot status/health checks (fast mode)...")
        # Try to run package install version first, fallback to local script
        # Prefer package module if available
        cb_cmd = [sys.executable, "-m", "cold_boot_orchestrator", "status"]
        code = run(cb_cmd)
        if code != 0:
            cb_cmd = [sys.executable, "cold_boot_orchestrator.py", "status"]
            code = run(cb_cmd)
        if code != 0:
            print("[WARN] Cold boot status check failed or returned non-zero.")
        else:
            print("[OK] Cold boot status check succeeded.")

    print(
        "\n[OK] Local installation complete.\n"
        "You can now run, for example:\n"
        "  python -m ghostlink.link_cli start\n"
        "  python -m ghostlink.link_cli status\n"
        "  python -m ghostlink.link_cli stop\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
