#!/usr/bin/env python3
"""
GhostLink Shell Integration
Automatically routes all commands through Link for intelligent processing
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path
from typing import List, Optional, Dict, Any
import shlex

class LinkCommandInterceptor:
    """Intercepts and processes commands through Link"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_python = self.project_root / ".venv" / "bin" / "python"
        self.link_cli = [str(self.venv_python), "-m", "ghostlink.link_cli"]

    def is_link_command(self, command: str) -> bool:
        """Check if command should be handled by Link"""
        link_commands = [
            "link", "@link", "forge", "ghostlink",
            "git", "python", "pip", "pytest", "black", "ruff"
        ]
        return any(cmd in command.lower() for cmd in link_commands)

    def analyze_command(self, command: str) -> Dict[str, Any]:
        """Analyze command to determine Link processing strategy"""
        analysis = {
            "should_intercept": False,
            "processing_type": "direct",
            "link_task": None,
            "reason": ""
        }

        cmd_lower = command.lower()

        # Git operations - route through Link
        if cmd_lower.startswith("git "):
            analysis["should_intercept"] = True
            analysis["processing_type"] = "link_git"
            analysis["link_task"] = "git_operation"
            analysis["reason"] = "Git operations should be tracked by Link"

        # Python/package operations - route through Link
        elif any(cmd in cmd_lower for cmd in ["pip ", "python -m ", "pytest", "black", "ruff"]):
            analysis["should_intercept"] = True
            analysis["processing_type"] = "link_task"
            analysis["link_task"] = "code_quality_operation"
            analysis["reason"] = "Code quality operations should be managed by Link"

        # Direct Link commands - process normally
        elif self.is_link_command(command):
            analysis["should_intercept"] = False
            analysis["processing_type"] = "direct"
            analysis["reason"] = "Direct Link command"

        # Other commands - create Link task for tracking
        else:
            analysis["should_intercept"] = True
            analysis["processing_type"] = "link_track"
            analysis["link_task"] = "system_operation"
            analysis["reason"] = "Track system operations through Link"

        return analysis

    def execute_via_link(self, command: str, analysis: Dict[str, Any]) -> int:
        """Execute command through Link processing"""
        try:
            if analysis["processing_type"] == "link_git":
                # Route git commands through Link
                git_args = shlex.split(command)[1:]  # Remove 'git'
                link_cmd = self.link_cli + ["git"] + git_args
                result = subprocess.run(link_cmd, cwd=self.project_root)
                return result.returncode

            elif analysis["processing_type"] == "link_task":
                # Create Link task and execute
                task_desc = f"Execute: {command}"
                priority = "normal"

                # Determine priority based on command
                if any(urgent in command.lower() for urgent in ["deploy", "release", "production"]):
                    priority = "critical"
                elif any(important in command.lower() for important in ["test", "build", "lint"]):
                    priority = "high"

                # Add task to Link
                add_task_cmd = self.link_cli + ["task", "add", task_desc, "--priority", priority]
                subprocess.run(add_task_cmd, capture_output=True)

                # Execute command
                result = subprocess.run(shlex.split(command), cwd=self.project_root)
                return result.returncode

            elif analysis["processing_type"] == "link_track":
                # Just track the command execution
                task_desc = f"System command: {command[:50]}..."
                add_task_cmd = self.link_cli + ["task", "add", task_desc, "--priority", "low"]
                subprocess.run(add_task_cmd, capture_output=True)

                # Execute command
                result = subprocess.run(shlex.split(command), cwd=self.project_root)
                return result.returncode

        except Exception as e:
            print(f"❌ Link processing failed: {e}")
            # Fallback to direct execution
            result = subprocess.run(shlex.split(command), cwd=self.project_root)
            return result.returncode

    def execute_command(self, command: str) -> int:
        """Main command execution with Link integration"""
        analysis = self.analyze_command(command)

        if analysis["should_intercept"]:
            print(f"🔗 Link intercepting: {analysis['reason']}")
            return self.execute_via_link(command, analysis)
        else:
            # Direct execution
            result = subprocess.run(shlex.split(command), cwd=self.project_root)
            return result.returncode


class ShellIntegration:
    """Shell integration manager"""

    def __init__(self):
        self.interceptor = LinkCommandInterceptor()
        self.shell_rc_files = {
            "zsh": Path.home() / ".zshrc",
            "bash": Path.home() / ".bashrc",
            "fish": Path.home() / ".config" / "fish" / "config.fish"
        }

    def detect_shell(self) -> str:
        """Detect current shell"""
        shell = os.environ.get("SHELL", "").lower()
        if "zsh" in shell:
            return "zsh"
        elif "bash" in shell:
            return "bash"
        elif "fish" in shell:
            return "fish"
        else:
            return "bash"  # default

    def create_wrapper_script(self) -> Path:
        """Create command wrapper script"""
        wrapper_dir = Path.home() / ".ghostlink"
        wrapper_dir.mkdir(exist_ok=True)

        wrapper_script = wrapper_dir / "link_command_wrapper.py"
        wrapper_content = f'''#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, "{self.interceptor.project_root / "src"}")

from enable_shell_integration import LinkCommandInterceptor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    interceptor = LinkCommandInterceptor()
    command = " ".join(sys.argv[1:])
    sys.exit(interceptor.execute_command(command))
'''

        with open(wrapper_script, "w") as f:
            f.write(wrapper_content)

        wrapper_script.chmod(0o755)
        return wrapper_script

    def setup_shell_integration(self):
        """Set up automatic command interception"""
        shell = self.detect_shell()
        rc_file = self.shell_rc_files.get(shell)

        if not rc_file:
            print(f"❌ Unsupported shell: {shell}")
            return False

        wrapper_script = self.create_wrapper_script()

        # Add to shell RC
        integration_line = f'\nalias ghostlink_cmd="{wrapper_script}"\n'
        integration_line += 'function preexec() {\n'
        integration_line += f'    if [[ "$1" != ghostlink* ]] && [[ "$1" != link* ]]; then\n'
        integration_line += f'        export GHOSTLINK_LAST_CMD="$1"\n'
        integration_line += f'        eval "ghostlink_cmd \\"$1\\""\n'
        integration_line += '        return $?\n'
        integration_line += '    fi\n'
        integration_line += '}\n'

        # Backup original RC
        if rc_file.exists():
            backup_file = rc_file.with_suffix(rc_file.suffix + ".ghostlink_backup")
            if not backup_file.exists():
                import shutil
                shutil.copy2(rc_file, backup_file)

        # Add integration
        with open(rc_file, "a") as f:
            f.write("\n# GhostLink Shell Integration\n")
            f.write(integration_line)

        print(f"✅ Shell integration enabled for {shell}")
        print(f"📁 Wrapper script: {wrapper_script}")
        print(f"🔄 Restart your shell or run: source {rc_file}")
        return True

    def remove_shell_integration(self):
        """Remove shell integration"""
        shell = self.detect_shell()
        rc_file = self.shell_rc_files.get(shell)

        if rc_file and rc_file.exists():
            content = rc_file.read_text()

            # Remove GhostLink integration
            lines = content.split('\n')
            filtered_lines = []
            skip_block = False

            for line in lines:
                if line.strip() == "# GhostLink Shell Integration":
                    skip_block = True
                    continue
                elif skip_block and line.strip() == "":
                    skip_block = False
                    continue
                elif skip_block:
                    continue
                else:
                    filtered_lines.append(line)

            rc_file.write_text('\n'.join(filtered_lines))
            print(f"✅ Shell integration removed from {shell}")
            return True

        return False


def main():
    parser = argparse.ArgumentParser(description="GhostLink Shell Integration")
    parser.add_argument("action", choices=["enable", "disable", "status", "test"])
    parser.add_argument("--shell", help="Force specific shell")

    args = parser.parse_args()

    integration = ShellIntegration()

    if args.shell:
        integration.shell_rc_files = {args.shell: integration.shell_rc_files.get(args.shell)}

    if args.action == "enable":
        success = integration.setup_shell_integration()
        if success:
            print("\n🎉 All commands will now automatically interact with Link!")
            print("💡 Commands are analyzed and routed through Link for intelligent processing")

    elif args.action == "disable":
        success = integration.remove_shell_integration()
        if success:
            print("✅ Shell integration disabled")

    elif args.action == "status":
        shell = integration.detect_shell()
        print(f"🐚 Current shell: {shell}")

        rc_file = integration.shell_rc_files.get(shell)
        if rc_file and rc_file.exists():
            content = rc_file.read_text()
            if "GhostLink Shell Integration" in content:
                print("✅ Link integration: ACTIVE")
            else:
                print("❌ Link integration: INACTIVE")
        else:
            print("❌ Shell RC file not found")

    elif args.action == "test":
        interceptor = LinkCommandInterceptor()

        test_commands = [
            "git status",
            "pip install requests",
            "python -m pytest",
            "ls -la",
            "link status"
        ]

        print("🧪 Testing Link command interception:")
        for cmd in test_commands:
            analysis = interceptor.analyze_command(cmd)
            status = "🔗 INTERCEPT" if analysis["should_intercept"] else "➡️ DIRECT"
            print(f"  {status} {cmd} - {analysis['reason']}")


if __name__ == "__main__":
    main()
