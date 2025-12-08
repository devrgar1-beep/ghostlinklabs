#!/usr/bin/env python3
"""
GhostLink Complete Automation Setup
Sets up all automatic interactions and integrations
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any

class CompleteAutomationSetup:
    """Sets up complete automatic command interaction system"""

    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_python = self.project_root / ".venv" / "bin" / "python3"
        self.link_cli = [str(self.venv_python), "-m", "ghostlink.link_cli"]

    def run_link_command(self, args: List[str]) -> subprocess.CompletedProcess:
        """Run a Link CLI command"""
        cmd = self.link_cli + args
        return subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)

    def setup_shell_integration(self) -> bool:
        """Set up shell command interception"""
        print("🐚 Setting up shell integration...")

        result = subprocess.run([
            str(self.venv_python), "src/enable_shell_integration.py", "enable"
        ], cwd=self.project_root)

        if result.returncode == 0:
            print("✅ Shell integration enabled")
            return True
        else:
            print("❌ Shell integration failed")
            return False

    def setup_vscode_integration(self) -> bool:
        """Set up VS Code integration (if available)"""
        print("💻 Setting up VS Code integration...")

        # Check if VS Code CLI is available
        vscode_check = subprocess.run(["which", "code"], capture_output=True)
        if vscode_check.returncode != 0:
            print("⚠️  VS Code CLI not found - skipping VS Code integration")
            return True

        result = subprocess.run([
            str(self.venv_python), "src/vscode_integration.py", "--settings"
        ], cwd=self.project_root)

        if result.returncode == 0:
            print("✅ VS Code integration configured")
            return True
        else:
            print("❌ VS Code integration failed")
            return False

    def setup_link_automation_rules(self) -> bool:
        """Set up Link automation rules for command processing"""
        print("🔗 Setting up Link automation rules...")

        # Add high-priority automation tasks
        automation_tasks = [
            ("Monitor system health continuously", "critical"),
            ("Auto-commit safe changes", "high"),
            ("Run tests on code changes", "high"),
            ("Backup configuration files", "normal"),
            ("Update dependencies weekly", "low"),
        ]

        for task_desc, priority in automation_tasks:
            result = self.run_link_command(["task", "add", task_desc, "--priority", priority])
            if result.returncode != 0:
                print(f"⚠️  Failed to add task: {task_desc}")
            else:
                print(f"✅ Added automation task: {task_desc}")

        # Set up learning preferences for automation
        preferences = [
            ("automation_level", "full_auto"),
            ("command_interception", "enabled"),
            ("task_auto_creation", "enabled"),
            ("error_auto_recovery", "enabled"),
        ]

        for pref, value in preferences:
            result = self.run_link_command(["learn", "set", pref, value])
            if result.returncode != 0:
                print(f"⚠️  Failed to set preference: {pref}")
            else:
                print(f"✅ Set preference: {pref} = {value}")

        return True

    def setup_environment_variables(self) -> bool:
        """Set up environment variables for automation"""
        print("🌍 Setting up environment variables...")

        env_vars = {
            "GHOSTLINK_AUTO_INTERACT": "true",
            "GHOSTLINK_ROOT": str(self.project_root),
            "GHOSTLINK_ACTIVE": "true",
            "GHOSTLINK_AUTOMATION_LEVEL": "full",
        }

        # Add to shell profile
        shell_rc = Path.home() / ".zshrc"
        if not shell_rc.exists():
            shell_rc = Path.home() / ".bashrc"

        if shell_rc.exists():
            content = shell_rc.read_text()
            if "# GhostLink Environment" not in content:
                with open(shell_rc, "a") as f:
                    f.write("\n# GhostLink Environment\n")
                    for key, value in env_vars.items():
                        f.write(f'export {key}="{value}"\n')

                print("✅ Environment variables added to shell profile")
                print("🔄 Run: source ~/.zshrc (or ~/.bashrc)")
            else:
                print("✅ Environment variables already configured")
        else:
            print("⚠️  Could not find shell profile")

        return True

    def setup_git_hooks(self) -> bool:
        """Set up Git hooks for automatic Link integration"""
        print("🔄 Setting up Git hooks...")

        git_hooks_dir = self.project_root / ".git" / "hooks"
        if not git_hooks_dir.exists():
            print("⚠️  Git repository not initialized - skipping hooks")
            return True

        # Pre-commit hook
        pre_commit_hook = git_hooks_dir / "pre-commit"
        hook_content = f'''#!/bin/bash
# GhostLink pre-commit hook
{self.venv_python} -m ghostlink.link_cli task add "Git commit: $GIT_COMMIT_MESSAGE" --priority normal
{self.venv_python} -m ghostlink.link_cli git status
'''

        try:
            with open(pre_commit_hook, "w") as f:
                f.write(hook_content)
            pre_commit_hook.chmod(0o755)
            print("✅ Pre-commit hook installed")
        except Exception as e:
            print(f"⚠️  Failed to install pre-commit hook: {e}")

        return True

    def create_automation_dashboard(self) -> bool:
        """Create automation status dashboard"""
        print("📊 Creating automation dashboard...")

        dashboard_script = self.project_root / "automation_status.py"
        dashboard_content = f'''#!/usr/bin/env python3
"""
GhostLink Automation Status Dashboard
"""

import subprocess
import json
from pathlib import Path

def run_link_cmd(args):
    """Run Link CLI command"""
    cmd = ["{self.venv_python}", "-m", "ghostlink.link_cli"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="{self.project_root}")
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
            print(f"🔗 Link Active: {{'✅' if status.get('active', False) else '❌'}}")
            print(f"📋 Pending Tasks: {{status.get('pending_tasks', 0)}}")
            print(f"✅ Completed Tasks: {{status.get('completed_tasks', 0)}}")
            print(f"❌ Failed Tasks: {{status.get('failed_tasks', 0)}}")
        except:
            print("🔗 Link Status: Unknown")
    else:
        print("🔗 Link Status: ❌ Not responding")

    # Shell integration
    result = subprocess.run(["{self.venv_python}", "src/enable_shell_integration.py", "status"],
                          capture_output=True, text=True, cwd="{self.project_root}")
    if "ACTIVE" in result.stdout:
        print("🐚 Shell Integration: ✅ ACTIVE")
    else:
        print("🐚 Shell Integration: ❌ INACTIVE")

    # Environment variables
    auto_interact = os.getenv("GHOSTLINK_AUTO_INTERACT", "false")
    print(f"⚙️  Auto Interact: {{'✅' if auto_interact == 'true' else '❌'}}")

    print("\\n🎯 Automation Rules:")
    result = run_link_cmd(["learn", "list"])
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print("❌ Could not retrieve learning data")

if __name__ == "__main__":
    show_status()
'''

        try:
            with open(dashboard_script, "w") as f:
                f.write(dashboard_content)
            dashboard_script.chmod(0o755)
            print("✅ Automation dashboard created")
            print(f"📁 Run: python automation_status.py")
            return True
        except Exception as e:
            print(f"❌ Failed to create dashboard: {e}")
            return False

    def run_all_setup(self) -> bool:
        """Run complete automation setup"""
        print("🚀 Setting up complete GhostLink automation...")
        print("=" * 60)

        success = True

        # Core integrations
        success &= self.setup_shell_integration()
        success &= self.setup_vscode_integration()

        # Link automation
        success &= self.setup_link_automation_rules()
        success &= self.setup_environment_variables()

        # Additional features
        success &= self.setup_git_hooks()
        success &= self.create_automation_dashboard()

        print("\\n" + "=" * 60)
        if success:
            print("🎉 Complete automation setup successful!")
            print("\\n💡 All commands now automatically interact with Link!")
            print("🔄 Restart your shell to activate all features")
            print("📊 Check status: python automation_status.py")
        else:
            print("⚠️  Setup completed with some warnings")

        return success


def main():
    parser = argparse.ArgumentParser(description="GhostLink Complete Automation Setup")
    parser.add_argument("action", choices=["setup", "status", "test"],
                       help="Action to perform")

    args = parser.parse_args()

    setup = CompleteAutomationSetup()

    if args.action == "setup":
        setup.run_all_setup()

    elif args.action == "status":
        # Run the dashboard if it exists
        dashboard = setup.project_root / "automation_status.py"
        if dashboard.exists():
            subprocess.run([str(setup.venv_python), "automation_status.py"],
                         cwd=setup.project_root)
        else:
            print("❌ Automation dashboard not found. Run setup first.")

    elif args.action == "test":
        print("🧪 Testing automation components...")

        # Test Link connectivity
        result = setup.run_link_command(["status"])
        if result.returncode == 0:
            print("✅ Link CLI: Connected")
        else:
            print("❌ Link CLI: Failed")

        # Test shell integration
        result = subprocess.run([
            str(setup.venv_python), "src/enable_shell_integration.py", "test"
        ], capture_output=True, text=True, cwd=setup.project_root)

        if result.returncode == 0:
            print("✅ Shell Integration: Working")
        else:
            print("❌ Shell Integration: Failed")

        print("\\n🎯 Test complete!")


if __name__ == "__main__":
    main()
