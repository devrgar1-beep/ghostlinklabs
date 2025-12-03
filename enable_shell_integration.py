#!/usr/bin/env python3
"""
GhostLink Shell Integration Manager
Manages shell integration across PowerShell, Bash, and other shells
"""

import os
import sys
import subprocess
from pathlib import Path

GHOSTLINK_ROOT = Path(__file__).parent.absolute()

POWERSHELL_INTEGRATION = """
# GhostLink Shell Integration
. {integration_script}
"""

BASH_INTEGRATION = """
# GhostLink Shell Integration
export GHOSTLINK_ROOT="{ghostlink_root}"
export GHOSTLINK_ACTIVE="true"
export GHOSTLINK_SHELL="bash"
export PATH="$GHOSTLINK_ROOT:$GHOSTLINK_ROOT/ghostlink:$PATH"

# GhostLink aliases
alias gl='python -m ghostlink.link_cli'
alias link='python -m ghostlink.link_cli'
alias ghost='python -m ghostlink.link_cli'
alias void='python $GHOSTLINK_ROOT/void_activation.py'
alias gl-start='python -m ghostlink.link_cli start'
alias gl-stop='python -m ghostlink.link_cli stop'
alias gl-status='python -m ghostlink.link_cli status'
alias gl-health='python -m ghostlink.link_cli diagnostics health'
alias gl-server='python -m uvicorn ghostlink.main:app --host 127.0.0.1 --port 8001'
alias gl-bios='python $GHOSTLINK_ROOT/void_activation.py --admin-override --bridge-bios'

echo "🧠 GhostLink Shell Integration Loaded"
"""


def enable_powershell_integration():
    """Enable PowerShell integration."""
    try:
        # Get PowerShell profile path
        result = subprocess.run(
            ["powershell", "-Command", "$PROFILE"],
            capture_output=True,
            text=True,
            check=True
        )
        profile_path = Path(result.stdout.strip())
        
        integration_script = GHOSTLINK_ROOT / "ghostlink_shell_integration.ps1"
        
        # Create profile directory if it doesn't exist
        profile_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Read existing profile or create new
        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = ""
        
        # Add integration if not already present
        if "GhostLink Shell Integration" not in content:
            integration_line = f"\n# GhostLink Shell Integration\n. {integration_script}\n"
            with open(profile_path, 'a', encoding='utf-8') as f:
                f.write(integration_line)
            print(f"✅ PowerShell integration enabled: {profile_path}")
        else:
            print(f"ℹ️  PowerShell integration already enabled: {profile_path}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to enable PowerShell integration: {e}")
        return False


def enable_bash_integration():
    """Enable Bash integration."""
    try:
        home = Path.home()
        bashrc = home / ".bashrc"
        
        if bashrc.exists():
            with open(bashrc, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        # Add integration if not already present
        if "GhostLink Shell Integration" not in content:
            integration = BASH_INTEGRATION.format(ghostlink_root=str(GHOSTLINK_ROOT))
            with open(bashrc, 'a') as f:
                f.write(f"\n{integration}\n")
            print(f"✅ Bash integration enabled: {bashrc}")
        else:
            print(f"ℹ️  Bash integration already enabled: {bashrc}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to enable Bash integration: {e}")
        return False


def check_integration_status():
    """Check current shell integration status."""
    print("🔍 Checking GhostLink Shell Integration Status\n")
    print("=" * 60)
    
    # Check PowerShell
    try:
        result = subprocess.run(
            ["powershell", "-Command", "$PROFILE"],
            capture_output=True,
            text=True,
            check=True
        )
        profile_path = Path(result.stdout.strip())
        if profile_path.exists():
            with open(profile_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if "GhostLink" in content:
                print("✅ PowerShell: ENABLED")
            else:
                print("❌ PowerShell: NOT ENABLED")
        else:
            print("❌ PowerShell: NO PROFILE")
    except Exception as e:
        print(f"❌ PowerShell: ERROR - {e}")
    
    # Check Bash
    bashrc = Path.home() / ".bashrc"
    if bashrc.exists():
        with open(bashrc, 'r') as f:
            content = f.read()
        if "GhostLink" in content:
            print("✅ Bash: ENABLED")
        else:
            print("❌ Bash: NOT ENABLED")
    else:
        print("ℹ️  Bash: NO .bashrc")
    
    print("=" * 60)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="GhostLink Shell Integration Manager")
    parser.add_argument("action", choices=["enable", "status", "test"], 
                       help="Action to perform")
    parser.add_argument("--shell", choices=["powershell", "bash", "all"], 
                       default="all", help="Target shell")
    
    args = parser.parse_args()
    
    if args.action == "enable":
        print("🧠 Enabling GhostLink Shell Integration\n")
        
        if args.shell in ["powershell", "all"]:
            enable_powershell_integration()
        
        if args.shell in ["bash", "all"]:
            enable_bash_integration()
        
        print("\n✅ Shell integration setup complete!")
        print("📝 Restart your shell or run: . $PROFILE (PowerShell)")
        
    elif args.action == "status":
        check_integration_status()
    
    elif args.action == "test":
        print("🧪 Testing GhostLink commands...")
        test_commands = [
            "python -m ghostlink.link_cli status",
            "python void_activation.py --help",
        ]
        for cmd in test_commands:
            print(f"\n  Testing: {cmd}")
            try:
                subprocess.run(cmd, shell=True, check=True, timeout=5)
                print("  ✅ Success")
            except Exception as e:
                print(f"  ❌ Failed: {e}")


if __name__ == "__main__":
    main()
