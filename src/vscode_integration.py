#!/usr/bin/env python3
"""
GhostLink VS Code Integration Manager

Installs and manages VS Code extensions and integrations for GhostLink.
Pulls additional tools from GitHub repositories.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class VSCodeIntegration:
    """Manages VS Code integration for GhostLink"""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.root = workspace_root or Path(__file__).parent
        self.vscode_dir = self.root / ".vscode"
        self.vscode_cmd = self.find_vscode_command()

    def find_vscode_command(self) -> Optional[str]:
        """Find VS Code CLI command"""
        # Try common locations
        if sys.platform == "win32":
            paths = [
                Path(os.getenv("LOCALAPPDATA", "")) / "Programs" / "Microsoft VS Code" / "bin" / "code.cmd",
                Path(os.getenv("ProgramFiles", "")) / "Microsoft VS Code" / "bin" / "code.cmd",
                Path(os.getenv("ProgramFiles(x86)", "")) / "Microsoft VS Code" / "bin" / "code.cmd",
            ]
            for path in paths:
                if path.exists():
                    return str(path)

        # Try PATH
        import shutil
        cmd = shutil.which("code")
        if cmd:
            return cmd

        return None

    def install_extension(self, extension_id: str) -> bool:
        """Install a VS Code extension"""
        if not self.vscode_cmd:
            logger.error("VS Code CLI not found")
            return False

        try:
            logger.info(f"Installing extension: {extension_id}")
            result = subprocess.run(
                [self.vscode_cmd, "--install-extension", extension_id],
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode == 0:
                logger.info(f"✅ {extension_id} installed")
                return True
            else:
                logger.error(f"❌ Failed to install {extension_id}: {result.stderr}")
                return False

        except Exception as e:
            logger.error(f"Error installing {extension_id}: {e}")
            return False

    def list_installed_extensions(self) -> List[str]:
        """List installed VS Code extensions"""
        if not self.vscode_cmd:
            return []

        try:
            result = subprocess.run(
                [self.vscode_cmd, "--list-extensions"],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return [line.strip() for line in result.stdout.splitlines() if line.strip()]

        except Exception as e:
            logger.error(f"Error listing extensions: {e}")

        return []

    def install_ghostlink_extensions(self):
        """Install recommended GhostLink extensions"""
        logger.info("🔧 Installing GhostLink VS Code Extensions...\n")

        extensions = {
            # Python Development
            "ms-python.python": "Python language support",
            "ms-python.vscode-pylance": "Python IntelliSense",
            "ms-python.debugpy": "Python debugger",
            "ms-python.black-formatter": "Black code formatter",
            "charliermarsh.ruff": "Ruff linter (ultra-fast)",

            # GitHub & AI
            "github.copilot": "GitHub Copilot AI assistant",
            "github.copilot-chat": "GitHub Copilot Chat",
            "github.vscode-pull-request-github": "GitHub Pull Requests",

            # Shell & Terminal
            "ms-vscode.powershell": "PowerShell support",
            "foxundermoon.shell-format": "Shell script formatter",
            "timonwong.shellcheck": "ShellCheck linter",

            # Docker & Containers
            "ms-azuretools.vscode-docker": "Docker support",
            "ms-vscode-remote.remote-containers": "Dev Containers",

            # Data & Databases
            "mtxr.sqltools": "SQL Tools",
            "evidence-dev.sqltools-clickhouse-driver": "ClickHouse driver",

            # Productivity
            "eamodio.gitlens": "GitLens (supercharged Git)",
            "gruntfuggly.todo-tree": "TODO Tree",
            "wayou.vscode-todo-highlight": "TODO Highlight",

            # Code Quality
            "usernamehw.errorlens": "Error Lens (inline errors)",
            "streetsidesoftware.code-spell-checker": "Code Spell Checker",

            # Markdown & Docs
            "yzhang.markdown-all-in-one": "Markdown All in One",
            "davidanson.vscode-markdownlint": "Markdown linting",

            # JSON & YAML
            "redhat.vscode-yaml": "YAML language support",
            "tamasfe.even-better-toml": "TOML support",

            # Themes & UI
            "pkief.material-icon-theme": "Material Icon Theme",
            "github.github-vscode-theme": "GitHub Theme",
        }

        installed = self.list_installed_extensions()
        to_install = []

        for ext_id, desc in extensions.items():
            if ext_id in installed:
                logger.info(f"✓ {ext_id} - Already installed")
            else:
                logger.info(f"→ {ext_id} - {desc}")
                to_install.append(ext_id)

        if not to_install:
            logger.info("\n✅ All recommended extensions already installed!")
            return

        logger.info(f"\n📦 Installing {len(to_install)} extensions...")

        success_count = 0
        for ext_id in to_install:
            if self.install_extension(ext_id):
                success_count += 1

        logger.info(f"\n✅ Installed {success_count}/{len(to_install)} extensions")

    def update_vscode_settings(self):
        """Update VS Code settings for GhostLink"""
        settings_file = self.vscode_dir / "settings.json"

        logger.info("⚙️ Updating VS Code settings...")

        # Default settings for GhostLink
        ghostlink_settings = {
            # Python
            "python.defaultInterpreterPath": "${workspaceFolder}/.venv/Scripts/python.exe",
            "python.analysis.typeCheckingMode": "basic",
            "python.analysis.autoImportCompletions": True,
            "python.terminal.activateEnvironment": True,

            # Formatting
            "[python]": {
                "editor.defaultFormatter": "ms-python.black-formatter",
                "editor.formatOnSave": True,
                "editor.codeActionsOnSave": {
                    "source.organizeImports": "explicit"
                }
            },

            # Linting
            "ruff.enable": True,
            "ruff.organizeImports": True,

            # Editor
            "editor.rulers": [88, 120],
            "editor.tabSize": 4,
            "editor.insertSpaces": True,
            "files.trimTrailingWhitespace": True,
            "files.insertFinalNewline": True,

            # Terminal
            "terminal.integrated.defaultProfile.windows": "PowerShell",
            "terminal.integrated.env.windows": {
                "GHOSTLINK_ROOT": "${workspaceFolder}",
                "GHOSTLINK_ACTIVE": "true"
            },

            # GitHub Copilot
            "github.copilot.enable": {
                "*": True,
                "yaml": True,
                "plaintext": True,
                "markdown": True
            },

            # Git
            "git.autofetch": True,
            "git.confirmSync": False,

            # Files
            "files.exclude": {
                "**/__pycache__": True,
                "**/*.pyc": True,
                "**/.pytest_cache": True,
                "**/.mypy_cache": True,
                "**/.ruff_cache": True,
                "**/node_modules": True,
                "**/.venv": True
            },

            # Search
            "search.exclude": {
                "**/node_modules": True,
                "**/.venv": True,
                "**/dist": True,
                "**/build": True,
                "**/.git": True
            }
        }

        # Merge with existing settings
        existing_settings = {}
        if settings_file.exists():
            try:
                with open(settings_file) as f:
                    content = f.read()
                    # Remove comments and trailing commas for JSON parsing
                    import re
                    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
                    content = re.sub(r',(\s*[}\]])', r'\1', content)
                    existing_settings = json.loads(content)
            except Exception as e:
                logger.warning(f"Could not parse existing settings: {e}")

        # Update settings (preserve existing, add new)
        for key, value in ghostlink_settings.items():
            if key not in existing_settings:
                existing_settings[key] = value

        # Write back
        self.vscode_dir.mkdir(exist_ok=True)
        with open(settings_file, 'w') as f:
            json.dump(existing_settings, f, indent=4)

        logger.info("✅ VS Code settings updated")

    def update_extensions_json(self):
        """Update recommended extensions list"""
        extensions_file = self.vscode_dir / "extensions.json"

        logger.info("📋 Updating extensions recommendations...")

        recommended = [
            # Core Python
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-python.debugpy",
            "ms-python.black-formatter",
            "charliermarsh.ruff",

            # GitHub & AI
            "github.copilot",
            "github.copilot-chat",
            "github.vscode-pull-request-github",

            # Shell
            "ms-vscode.powershell",
            "foxundermoon.shell-format",
            "timonwong.shellcheck",
            "mads-hartmann.bash-ide-vscode",

            # Docker
            "ms-azuretools.vscode-docker",
            "ms-vscode-remote.remote-containers",

            # Productivity
            "eamodio.gitlens",
            "gruntfuggly.todo-tree",
            "usernamehw.errorlens",

            # Data formats
            "redhat.vscode-yaml",
            "tamasfe.even-better-toml",

            # Docs
            "yzhang.markdown-all-in-one",
            "davidanson.vscode-markdownlint",
        ]

        extensions_data = {
            "recommendations": recommended
        }

        self.vscode_dir.mkdir(exist_ok=True)
        with open(extensions_file, 'w') as f:
            json.dump(extensions_data, f, indent=4)

        logger.info("✅ Extensions recommendations updated")

    def create_workspace_file(self):
        """Create .code-workspace file"""
        workspace_file = self.root / "ghostlink.code-workspace"

        logger.info("💼 Creating VS Code workspace file...")

        workspace_config = {
            "folders": [
                {
                    "path": ".",
                    "name": "GhostLink"
                }
            ],
            "settings": {
                "files.exclude": {
                    "**/__pycache__": True,
                    "**/*.pyc": True,
                    "**/.pytest_cache": True,
                    "**/.mypy_cache": True,
                    "**/.ruff_cache": True
                }
            },
            "extensions": {
                "recommendations": [
                    "ms-python.python",
                    "github.copilot",
                    "github.copilot-chat",
                    "ms-vscode.powershell"
                ]
            },
            "tasks": {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Start GhostLink",
                        "type": "shell",
                        "command": "python -m ghostlink.main",
                        "problemMatcher": [],
                        "group": {
                            "kind": "build",
                            "isDefault": True
                        }
                    },
                    {
                        "label": "Run Tests",
                        "type": "shell",
                        "command": "pytest",
                        "problemMatcher": [],
                        "group": "test"
                    },
                    {
                        "label": "Lattice Demo",
                        "type": "shell",
                        "command": "python ghostlink_lattice.py --demo",
                        "problemMatcher": []
                    }
                ]
            }
        }

        with open(workspace_file, 'w') as f:
            json.dump(workspace_config, f, indent=4)

        logger.info(f"✅ Workspace file created: {workspace_file}")

    def install_all(self):
        """Install all VS Code integrations"""
        logger.info("🚀 Installing GhostLink VS Code Integration\n")
        logger.info("=" * 60)

        if not self.vscode_cmd:
            logger.error("❌ VS Code CLI not found!")
            logger.error("Please ensure 'code' command is in PATH")
            return False

        logger.info(f"✅ VS Code found: {self.vscode_cmd}\n")

        # Update configuration files
        self.update_vscode_settings()
        self.update_extensions_json()
        self.create_workspace_file()

        # Install extensions
        print()
        self.install_ghostlink_extensions()

        logger.info("\n" + "=" * 60)
        logger.info("✅ GhostLink VS Code Integration Complete!")
        logger.info("\n💡 Next steps:")
        logger.info("  1. Restart VS Code to load new extensions")
        logger.info("  2. Open ghostlink.code-workspace")
        logger.info("  3. Press Ctrl+Shift+P and run 'Python: Select Interpreter'")
        logger.info("  4. Select the .venv interpreter")

        return True


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="GhostLink VS Code Integration Manager")
    parser.add_argument("--install", action="store_true", help="Install all extensions and configure VS Code")
    parser.add_argument("--list", action="store_true", help="List installed extensions")
    parser.add_argument("--settings", action="store_true", help="Update VS Code settings only")
    parser.add_argument("--extensions", action="store_true", help="Install extensions only")

    args = parser.parse_args()

    vscode = VSCodeIntegration()

    if args.list:
        extensions = vscode.list_installed_extensions()
        print(f"\nInstalled Extensions ({len(extensions)}):\n")
        for ext in sorted(extensions):
            print(f"  * {ext}")
        print()

    elif args.settings:
        vscode.update_vscode_settings()
        vscode.update_extensions_json()
        vscode.create_workspace_file()
        print("\n✅ VS Code configuration updated!")

    elif args.extensions:
        vscode.install_ghostlink_extensions()

    elif args.install:
        vscode.install_all()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
