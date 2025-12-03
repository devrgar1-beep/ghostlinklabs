#!/usr/bin/env python3
"""
GhostLink Hybrid Triad Setup Script
Automates the complete system setup for sovereign operation
"""

import argparse
import os
from pathlib import Path
import subprocess
import sys


def run_command(cmd, cwd=None, check=True):
    """Run a shell command"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {result.stderr}")
        return False
    return True

def setup_virtual_environment():
    """Create and setup virtual environment"""
    print("Setting up virtual environment...")

    if not run_command([sys.executable, "-m", "venv", ".venv"]):
        return False

    # Activate and upgrade pip
    pip_path = ".venv/bin/pip" if os.name != 'nt' else ".venv/Scripts/pip"
    if not run_command([pip_path, "install", "--upgrade", "pip"]):
        return False

    print("Virtual environment created successfully")
    return True

def install_dependencies(mode="minimal"):
    """Install dependencies based on mode"""
    print(f"Installing dependencies in {mode} mode...")

    pip_path = ".venv/bin/pip" if os.name != 'nt' else ".venv/Scripts/pip"

    if mode == "minimal":
        # Install with no optional dependencies
        cmd = [pip_path, "install", "-e", "."]

    return run_command(cmd)

def setup_mathematica():
    """Setup Mathematica integration"""
    print("Setting up Mathematica integration...")

    mathematica_dir = Path("mathematica")
    mathematica_dir.mkdir(exist_ok=True)

    # Check if Mathematica/Wolfram Engine is available
    try:
        result = subprocess.run(["wolframscript", "-code", "Print[$Version]"],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"Mathematica detected: {result.stdout.strip()}")
            return True
        else:
            print("Mathematica not found - symbolic features will use fallback mode")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("Mathematica not available - system will operate in fallback mode")
        return True

def setup_docker():
    """Setup Docker integration"""
    print("Setting up Docker integration...")

    # Check if Docker is available
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Docker detected: {result.stdout.strip()}")

            # Build Docker image
            if run_command(["docker", "build", "-t", "ghostlink:local", "."]):
                print("Docker image built successfully")
                return True
        else:
            print("Docker not available - container features disabled")
            return True
    except FileNotFoundError:
        print("Docker not found - container features will be unavailable")
        return True

def setup_github_integration():
    """Setup GitHub integration"""
    print("Setting up GitHub integration...")

    # Check if git is available and this is a git repository
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Git repository detected")

            # Setup GitHub Actions if not already configured
            workflows_dir = Path(".github/workflows")
            if workflows_dir.exists():
                print("GitHub Actions workflows already configured")
            else:
                print("GitHub Actions workflows not found")
                return False

            return True
        else:
            print("Not a git repository - GitHub integration skipped")
            return True
    except FileNotFoundError:
        print("Git not found - GitHub integration unavailable")
        return True

def create_default_config():
    """Create default configuration"""
    print("Creating default configuration...")

    config_content = """# GhostLink Hybrid Triad Configuration
# This file contains default settings for sovereign operation

[core]
experimental_mode = true
hybrid_triad = true
local_first = true
sovereign = true

[logging]
level = INFO
file = ghostlink.log

[api]
host = 0.0.0.0
port = 8000
cors_origins = ["*"]

[storage]
type = file
path = data/

[ai]
fallback_mode = true
mathematica_enabled = false
ml_enabled = false

[security]
token_required = true
allow_insecure = false
"""

    config_file = Path("ghostlink.ini")
    if not config_file.exists():
        config_file.write_text(config_content)
        print("Default configuration created")
    else:
        print("Configuration file already exists")

    return True

def main():
    parser = argparse.ArgumentParser(description="GhostLink Hybrid Triad Setup")
    parser.add_argument("--mode", choices=["minimal", "standard", "full"],
                       default="minimal",
                       help="Installation mode (default: minimal)")
    parser.add_argument("--skip-venv", action="store_true",
                       help="Skip virtual environment creation")
    parser.add_argument("--skip-docker", action="store_true",
                       help="Skip Docker setup")
    parser.add_argument("--skip-mathematica", action="store_true",
                       help="Skip Mathematica setup")

    args = parser.parse_args()

    print("🧬 GhostLink Hybrid Triad Setup")
    print("=" * 40)

    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    success = True

    # Setup virtual environment
    if not args.skip_venv:
        success &= setup_virtual_environment()

    # Install dependencies
    success &= install_dependencies(args.mode)

    # Setup integrations
    if not args.skip_mathematica:
        success &= setup_mathematica()

    if not args.skip_docker:
        success &= setup_docker()

    success &= setup_github_integration()

    # Create default config
    success &= create_default_config()

    print("\n" + "=" * 40)
    if success:
        print("✅ GhostLink Hybrid Triad setup completed successfully!")
        print("\nTo activate the environment:")
        print("  source .venv/bin/activate")
        print("\nTo run GhostLink:")
        print("  ghostlink")
        print("\nTo run with Docker:")
        print("  docker-compose up")
        print("\nFor more information, see README.md")
    else:
        print("❌ Setup completed with errors. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
