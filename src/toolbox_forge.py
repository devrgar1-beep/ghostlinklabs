#!/usr/bin/env python3
"""
GhostLink Toolbox Forge
A unified command center and toolkit for all GhostLink operations
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

GHOSTLINK_ROOT = Path(__file__).parent.absolute()


class ToolboxForge:
    """GhostLink Toolbox Forge - Unified Command Center"""

    def __init__(self):
        self.root = GHOSTLINK_ROOT
        self.config_file = self.root / ".ghostlink_forge_config.json"
        self.load_config()

    def load_config(self):
        """Load forge configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "initialized": False,
                "tools": {},
                "shortcuts": {},
                "history": []
            }

    def save_config(self):
        """Save forge configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, indent=2, fp=f)

    def log_action(self, action: str, status: str, details: str = ""):
        """Log an action to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": status,
            "details": details
        }
        self.config["history"].append(entry)
        self.save_config()

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None,
                   capture: bool = False) -> subprocess.CompletedProcess:
        """Run a shell command"""
        try:
            if capture:
                result = subprocess.run(
                    cmd, cwd=cwd or self.root,
                    capture_output=True, text=True, timeout=30
                )
            else:
                result = subprocess.run(cmd, cwd=cwd or self.root, timeout=30)
            return result
        except Exception as e:
            print(f"❌ Command failed: {e}")
            return subprocess.CompletedProcess(cmd, 1, "", str(e))

    # ============================================================
    # SYSTEM TOOLS
    # ============================================================

    def system_status(self):
        """Get comprehensive system status"""
        print("🔍 GhostLink System Status\n")
        print("=" * 60)

        # Check Python
        result = self.run_command([sys.executable, "--version"], capture=True)
        print(f"Python: {result.stdout.strip()}")

        # Check GhostLink modules
        modules = ["ghostlink.link_cli", "ghostlink.main", "ghostlink.health_monitor"]
        for mod in modules:
            result = self.run_command(
                [sys.executable, "-c", f"import {mod}; print('✅')"],
                capture=True
            )
            status = "✅" if result.returncode == 0 else "❌"
            print(f"{mod}: {status}")

        # Check files
        critical_files = [
            "void_activation.py",
            "ghostlink_shell_integration.ps1",
            "enable_shell_integration.py",
        ]
        print("\nCritical Files:")
        for f in critical_files:
            exists = (self.root / f).exists()
            status = "✅" if exists else "❌"
            print(f"  {f}: {status}")

        print("=" * 60)

    def health_check(self):
        """Run comprehensive health check"""
        print("🏥 Running Health Check...\n")
        result = self.run_command(
            [sys.executable, "-m", "ghostlink.link_cli", "diagnostics", "health"]
        )
        self.log_action("health_check", "completed" if result.returncode == 0 else "failed")

    def system_audit(self, target: str = "."):
        """Run system audit"""
        print(f"🔍 Running System Audit on {target}...\n")
        audit_file = self.root / "ghostlink_audit.py"
        if audit_file.exists():
            result = self.run_command([sys.executable, str(audit_file), target])
            self.log_action("system_audit", "completed" if result.returncode == 0 else "failed", target)
        else:
            print("❌ Audit tool not found")

    # ============================================================
    # SERVER TOOLS
    # ============================================================

    def start_server(self, port: int = 8001, host: str = "127.0.0.1"):
        """Start FastAPI server"""
        print(f"🚀 Starting FastAPI server on {host}:{port}...\n")
        result = self.run_command([
            sys.executable, "-m", "uvicorn", "ghostlink.main:app",
            "--host", host, "--port", str(port), "--reload"
        ])
        self.log_action("start_server", "started", f"{host}:{port}")

    def stop_server(self):
        """Stop running servers"""
        print("🛑 Stopping servers...\n")
        # Windows: Find and kill Python processes running uvicorn
        if sys.platform == "win32":
            subprocess.run([
                "powershell", "-Command",
                "Get-Process python | Where-Object {$_.CommandLine -like '*uvicorn*'} | Stop-Process -Force"
            ])
        else:
            subprocess.run(["pkill", "-f", "uvicorn"])
        print("✅ Servers stopped")
        self.log_action("stop_server", "stopped")

    # ============================================================
    # HARDWARE TOOLS
    # ============================================================

    def void_activation(self, admin_override: bool = False, bridge_bios: bool = False):
        """Run void activation"""
        print("🌌 Running Void Activation...\n")
        cmd = [sys.executable, str(self.root / "void_activation.py")]
        if admin_override:
            cmd.append("--admin-override")
        if bridge_bios:
            cmd.append("--bridge-bios")
        result = self.run_command(cmd)
        self.log_action("void_activation", "completed" if result.returncode == 0 else "failed")

    def bios_bridge(self):
        """Bridge BIOS and hardware"""
        print("🧠 Bridging BIOS and Hardware...\n")
        result = self.run_command([
            sys.executable, str(self.root / "void_activation.py"),
            "--admin-override", "--bridge-bios"
        ])
        self.log_action("bios_bridge", "completed" if result.returncode == 0 else "failed")

    # ============================================================
    # LINK ORCHESTRATOR TOOLS
    # ============================================================

    def link_start(self, hardware: bool = False):
        """Start Link orchestrator"""
        print("🔗 Starting Link Orchestrator...\n")
        cmd = [sys.executable, "-m", "ghostlink.link_cli", "start"]
        if hardware:
            cmd.extend(["--hardware", "--confirm-hardware"])
        result = self.run_command(cmd)
        self.log_action("link_start", "started" if result.returncode == 0 else "failed")

    def link_stop(self):
        """Stop Link orchestrator"""
        print("🛑 Stopping Link Orchestrator...\n")
        result = self.run_command([sys.executable, "-m", "ghostlink.link_cli", "stop"])
        self.log_action("link_stop", "stopped")

    def link_status(self):
        """Get Link status"""
        print("📊 Link Status:\n")
        self.run_command([sys.executable, "-m", "ghostlink.link_cli", "status"])

    # ============================================================
    # GIT TOOLS
    # ============================================================

    def git_sync(self):
        """Sync with git repository"""
        print("🔄 Syncing with Git...\n")
        result = self.run_command([sys.executable, "-m", "ghostlink.link_cli", "git", "sync"])
        self.log_action("git_sync", "completed" if result.returncode == 0 else "failed")

    def git_status(self):
        """Get git status"""
        print("📊 Git Status:\n")
        self.run_command(["git", "status"])

    def git_pull(self):
        """Pull from git"""
        print("⬇️ Pulling from Git...\n")
        result = self.run_command([sys.executable, "-m", "ghostlink.link_cli", "git", "pull"])
        self.log_action("git_pull", "completed" if result.returncode == 0 else "failed")

    # ============================================================
    # BUILD TOOLS
    # ============================================================

    def build_all(self):
        """Build all components"""
        print("🔨 Building All Components...\n")
        print("=" * 60)

        # Install Python package in editable mode
        print("\n1. Installing GhostLink package...")
        result = self.run_command([sys.executable, "-m", "pip", "install", "-e", "."])

        # Install dependencies
        print("\n2. Installing dependencies...")
        deps = ["psutil", "fastapi", "uvicorn[standard]", "httpx", "sqlalchemy", "pydantic"]
        for dep in deps:
            print(f"   Installing {dep}...")
            self.run_command([sys.executable, "-m", "pip", "install", dep, "--quiet"])

        print("\n✅ Build complete!")
        self.log_action("build_all", "completed")

    def clean(self):
        """Clean build artifacts"""
        print("🧹 Cleaning build artifacts...\n")
        artifacts = [
            "**/__pycache__",
            "**/*.pyc",
            "**/*.pyo",
            "**/*.egg-info",
            ".pytest_cache",
            "dist",
            "build"
        ]
        for pattern in artifacts:
            for path in self.root.glob(pattern):
                if path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    print(f"  Removed: {path}")
                else:
                    path.unlink()
                    print(f"  Removed: {path}")
        print("✅ Clean complete!")
        self.log_action("clean", "completed")

    # ============================================================
    # DEVELOPMENT TOOLS
    # ============================================================

    def test_all(self):
        """Run all tests"""
        print("🧪 Running Tests...\n")
        result = self.run_command([sys.executable, "-m", "pytest", "-v"])
        self.log_action("test_all", "passed" if result.returncode == 0 else "failed")

    def lint(self):
        """Run linting"""
        print("🔍 Running Linters...\n")
        # Try ruff first, fallback to flake8
        result = self.run_command([sys.executable, "-m", "ruff", "check", "ghostlink"])
        if result.returncode != 0:
            self.run_command([sys.executable, "-m", "flake8", "ghostlink"])
        self.log_action("lint", "completed")

    def format_code(self):
        """Format code"""
        print("✨ Formatting Code...\n")
        result = self.run_command([sys.executable, "-m", "black", "ghostlink", "*.py"])
        self.log_action("format", "completed" if result.returncode == 0 else "failed")

    # ============================================================
    # AI TOOLS - Internal Communication
    # ============================================================

    def groq_test(self):
        """Test Groq internal communication AI"""
        print("🧠 Testing Groq Internal Communication AI...\n")
        result = self.run_command([sys.executable, "groq_integration.py"])
        if result.returncode == 0:
            self.log_action("groq_test", "success", "Internal communication AI operational")
        else:
            self.log_action("groq_test", "failed", result.stderr if hasattr(result, 'stderr') else "")

    def groq_status(self):
        """Check Groq AI status"""
        print("🧠 Groq Internal Communication AI Status\n")
        try:
            from groq_integration import GroqClient
            client = GroqClient()
            print(f"✅ API Key: {client.api_key[:20]}...")
            print(f"✅ Model: {client.model}")
            print(f"✅ Purpose: Internal component coordination")
            models = client.list_models()
            print(f"✅ Available models: {len(models)}")
            self.log_action("groq_status", "success", f"{len(models)} models available")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.log_action("groq_status", "failed", str(e))

    def groq_communicate(self, sender: str, receiver: str, message: str):
        """Facilitate internal component communication"""
        print(f"🔗 Internal Communication: {sender} → {receiver}\n")
        try:
            from groq_integration import GroqClient
            client = GroqClient()
            response = client.internal_communication(sender, receiver, message)
            print(f"Response:\n{response}\n")
            self.log_action("groq_communicate", "success", f"{sender} → {receiver}")
        except Exception as e:
            print(f"❌ Error: {e}")
            self.log_action("groq_communicate", "failed", str(e))

    # ============================================================
    # LATTICE TOOLS - Unified Component Bridge
    # ============================================================

    def lattice_demo(self):
        """Run lattice demonstration"""
        print("🌐 Running GhostLink Lattice Demo...\n")
        result = self.run_command([sys.executable, "ghostlink_lattice.py", "--demo"])
        if result.returncode == 0:
            self.log_action("lattice_demo", "success", "Lattice demo completed")
        else:
            self.log_action("lattice_demo", "failed", "Demo failed")

    def lattice_state(self):
        """Show lattice state"""
        print("🌐 GhostLink Lattice State\n")
        result = self.run_command([sys.executable, "ghostlink_lattice.py", "--state"], capture=True)
        if result.returncode == 0 and result.stdout:
            print(result.stdout)
            self.log_action("lattice_state", "success", "State retrieved")
        else:
            print("❌ Failed to get lattice state")
            self.log_action("lattice_state", "failed", "State retrieval failed")

    def lattice_start(self):
        """Start lattice in interactive mode"""
        print("🌐 Starting GhostLink Lattice...\n")
        print("Note: Run 'python ghostlink_lattice.py --interactive' for full interactive mode")
        result = self.run_command([sys.executable, "ghostlink_lattice.py", "--demo"])
        self.log_action("lattice_start", "completed")

    # ============================================================
    # VSCODE INTEGRATION TOOLS
    # ============================================================

    def vscode_setup(self):
        """Setup VS Code integration"""
        print("🔧 Setting up VS Code integration...\n")
        result = self.run_command([sys.executable, "vscode_integration.py", "--install"])
        if result.returncode == 0:
            self.log_action("vscode_setup", "success", "VS Code integration complete")
        else:
            self.log_action("vscode_setup", "failed", "Setup failed")

    def vscode_extensions(self):
        """Install VS Code extensions"""
        print("📦 Installing VS Code extensions...\n")
        result = self.run_command([sys.executable, "vscode_integration.py", "--extensions"])
        self.log_action("vscode_extensions", "completed")

    def vscode_list(self):
        """List installed VS Code extensions"""
        print("📋 Installed VS Code extensions:\n")
        result = self.run_command([sys.executable, "vscode_integration.py", "--list"])
        self.log_action("vscode_list", "completed")

    def github_tools_download(self):
        """Download tools from GitHub"""
        print("📥 Downloading GitHub tools...\n")
        result = self.run_command([sys.executable, "github_tools.py", "--download"])
        self.log_action("github_tools", "completed")

    def github_tools_list(self):
        """List downloaded GitHub tools"""
        print("📦 Downloaded GitHub tools:\n")
        result = self.run_command([sys.executable, "github_tools.py", "--list"])
        self.log_action("github_tools_list", "completed")

    # ============================================================
    # UTILITY TOOLS
    # ============================================================

    def shell_integration(self):
        """Enable shell integration"""
        print("🐚 Enabling Shell Integration...\n")
        result = self.run_command([
            sys.executable,
            str(self.root / "enable_shell_integration.py"),
            "enable"
        ])
        self.log_action("shell_integration", "enabled" if result.returncode == 0 else "failed")

    def show_history(self, limit: int = 20):
        """Show action history"""
        print(f"📜 Action History (last {limit}):\n")
        print("=" * 60)
        for entry in self.config["history"][-limit:]:
            ts = entry["timestamp"]
            action = entry["action"]
            status = entry["status"]
            details = entry["details"]
            print(f"{ts} | {action:20s} | {status:10s} | {details}")
        print("=" * 60)

    def toolbox_info(self):
        """Show toolbox information"""
        print("🧰 GhostLink Toolbox Forge\n")
        print("=" * 60)
        print("Version: 1.0.0")
        print(f"Root: {self.root}")
        print(f"Initialized: {self.config['initialized']}")
        print(f"Actions Logged: {len(self.config['history'])}")
        print("\nAvailable Tool Categories:")
        print("  • System Tools: status, health, audit")
        print("  • Server Tools: start-server, stop-server")
        print("  • Hardware Tools: void, bios-bridge")
        print("  • Link Tools: link-start, link-stop, link-status")
        print("  • Git Tools: git-sync, git-status, git-pull")
        print("  • Build Tools: build, clean")
        print("  • AI Tools: groq-test, groq-status, groq-comm")
        print("  • Lattice Tools: lattice-demo, lattice-state, lattice-start")
        print("  • VSCode Tools: vscode-setup, vscode-extensions, vscode-list")
        print("  • GitHub Tools: github-tools, github-list")
        print("  • Dev Tools: test, lint, format")
        print("  • Utility Tools: shell-integration, history, info")
        print("=" * 60)

    def interactive_mode(self):
        """Run in interactive mode"""
        print("🎮 GhostLink Toolbox Forge - Interactive Mode\n")
        print("Type 'help' for available commands, 'exit' to quit\n")

        while True:
            try:
                cmd = input("forge> ").strip()
                if not cmd:
                    continue
                if cmd in ["exit", "quit", "q"]:
                    print("👋 Goodbye!")
                    break
                if cmd == "help":
                    self.toolbox_info()
                    continue

                # Parse and execute command
                parts = cmd.split()
                action = parts[0]
                args = parts[1:] if len(parts) > 1 else []

                method_map = {
                    "status": self.system_status,
                    "health": self.health_check,
                    "audit": lambda: self.system_audit(*args) if args else self.system_audit(),
                    "start-server": self.start_server,
                    "stop-server": self.stop_server,
                    "void": lambda: self.void_activation(admin_override=True),
                    "bios-bridge": self.bios_bridge,
                    "link-start": self.link_start,
                    "link-stop": self.link_stop,
                    "link-status": self.link_status,
                    "git-sync": self.git_sync,
                    "git-status": self.git_status,
                    "git-pull": self.git_pull,
                    "build": self.build_all,
                    "clean": self.clean,
                    "groq-test": self.groq_test,
                    "groq-status": self.groq_status,
                    "groq-comm": lambda: self.groq_communicate(*args) if len(args) >= 3 else print("Usage: groq-comm <sender> <receiver> <message>"),
                    "lattice-demo": self.lattice_demo,
                    "lattice-state": self.lattice_state,
                    "lattice-start": self.lattice_start,
                    "vscode-setup": self.vscode_setup,
                    "vscode-extensions": self.vscode_extensions,
                    "vscode-list": self.vscode_list,
                    "github-tools": self.github_tools_download,
                    "github-list": self.github_tools_list,
                    "test": self.test_all,
                    "lint": self.lint,
                    "format": self.format_code,
                    "shell": self.shell_integration,
                    "history": self.show_history,
                    "info": self.toolbox_info,
                }

                if action in method_map:
                    print()
                    method_map[action]()
                    print()
                else:
                    print(f"❌ Unknown command: {action}")
                    print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="GhostLink Toolbox Forge - Unified Command Center",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Commands:
  System:     status, health, audit [target]
  Server:     start-server [--port PORT], stop-server
  Hardware:   void, bios-bridge
  Link:       link-start, link-stop, link-status
  Git:        git-sync, git-status, git-pull
  Build:      build, clean
  Dev:        test, lint, format
  Utility:    shell, history, info

Interactive: Run without arguments for interactive mode
        """
    )

    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--port", type=int, default=8001, help="Server port")
    parser.add_argument("--host", default="127.0.0.1", help="Server host")

    args = parser.parse_args()

    forge = ToolboxForge()

    if not args.command:
        # Interactive mode
        forge.interactive_mode()
        return

    # Command mode
    command_map = {
        "status": forge.system_status,
        "health": forge.health_check,
        "audit": lambda: forge.system_audit(args.args[0] if args.args else "."),
        "start-server": lambda: forge.start_server(args.port, args.host),
        "stop-server": forge.stop_server,
        "void": lambda: forge.void_activation(admin_override=True),
        "bios-bridge": forge.bios_bridge,
        "link-start": forge.link_start,
        "link-stop": forge.link_stop,
        "link-status": forge.link_status,
        "git-sync": forge.git_sync,
        "git-status": forge.git_status,
        "git-pull": forge.git_pull,
        "build": forge.build_all,
        "clean": forge.clean,
        "groq-test": forge.groq_test,
        "groq-status": forge.groq_status,
        "groq-comm": lambda: forge.groq_communicate(args.args[0], args.args[1], " ".join(args.args[2:])) if len(args.args) >= 3 else print("Usage: groq-comm <sender> <receiver> <message>"),
        "lattice-demo": forge.lattice_demo,
        "lattice-state": forge.lattice_state,
        "lattice-start": forge.lattice_start,
        "vscode-setup": forge.vscode_setup,
        "vscode-extensions": forge.vscode_extensions,
        "vscode-list": forge.vscode_list,
        "github-tools": forge.github_tools_download,
        "github-list": forge.github_tools_list,
        "test": forge.test_all,
        "lint": forge.lint,
        "format": forge.format_code,
        "shell": forge.shell_integration,
        "history": forge.show_history,
        "info": forge.toolbox_info,
    }

    if args.command in command_map:
        command_map[args.command]()
    else:
        print(f"❌ Unknown command: {args.command}")
        print("Run with --help for usage information")
        sys.exit(1)


if __name__ == "__main__":
    main()
