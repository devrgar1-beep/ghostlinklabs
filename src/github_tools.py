#!/usr/bin/env python3
"""
GitHub Tools Downloader for GhostLink

Pulls useful tools and utilities from GitHub repositories.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class GitHubToolsManager:
    """Manages GitHub tool downloads and integration"""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.root = workspace_root or Path(__file__).parent
        self.tools_dir = self.root / "external_tools"
        self.tools_dir.mkdir(exist_ok=True)

    def clone_repo(self, repo_url: str, target_name: Optional[str] = None) -> bool:
        """Clone a GitHub repository"""
        if target_name:
            target_path = self.tools_dir / target_name
        else:
            target_name = repo_url.split("/")[-1].replace(".git", "")
            target_path = self.tools_dir / target_name

        if target_path.exists():
            logger.info(f"✓ {target_name} already exists, pulling latest...")
            try:
                subprocess.run(
                    ["git", "-C", str(target_path), "pull"],
                    check=True,
                    capture_output=True
                )
                logger.info(f"✅ {target_name} updated")
                return True
            except Exception as e:
                logger.error(f"Failed to update {target_name}: {e}")
                return False

        try:
            logger.info(f"📥 Cloning {repo_url}...")
            subprocess.run(
                ["git", "clone", repo_url, str(target_path)],
                check=True,
                capture_output=True
            )
            logger.info(f"✅ {target_name} cloned successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to clone {repo_url}: {e}")
            return False

    def download_useful_tools(self):
        """Download useful GitHub tools for GhostLink"""
        logger.info("🔧 Downloading Useful GitHub Tools...\n")
        logger.info("=" * 60)

        tools = [
            {
                "url": "https://github.com/microsoft/terminal",
                "name": "windows-terminal",
                "description": "Windows Terminal - Modern terminal application",
                "category": "Terminal"
            },
            {
                "url": "https://github.com/PowerShell/PowerShell",
                "name": "powershell-core",
                "description": "PowerShell 7+ cross-platform shell",
                "category": "Shell"
            },
            {
                "url": "https://github.com/ohmyzsh/ohmyzsh",
                "name": "oh-my-zsh",
                "description": "Oh My Zsh - Shell framework",
                "category": "Shell"
            },
            {
                "url": "https://github.com/junegunn/fzf",
                "name": "fzf",
                "description": "Fuzzy finder for command-line",
                "category": "CLI Tools"
            },
            {
                "url": "https://github.com/sharkdp/bat",
                "name": "bat",
                "description": "Cat clone with syntax highlighting",
                "category": "CLI Tools"
            },
            {
                "url": "https://github.com/sharkdp/fd",
                "name": "fd",
                "description": "Fast and user-friendly alternative to find",
                "category": "CLI Tools"
            },
            {
                "url": "https://github.com/BurntSushi/ripgrep",
                "name": "ripgrep",
                "description": "Extremely fast grep alternative",
                "category": "CLI Tools"
            },
            {
                "url": "https://github.com/stedolan/jq",
                "name": "jq",
                "description": "JSON processor for command-line",
                "category": "Data Tools"
            },
            {
                "url": "https://github.com/mikefarah/yq",
                "name": "yq",
                "description": "YAML/JSON/XML processor",
                "category": "Data Tools"
            },
            {
                "url": "https://github.com/dbcli/pgcli",
                "name": "pgcli",
                "description": "Postgres CLI with autocomplete",
                "category": "Database"
            },
            {
                "url": "https://github.com/tiangolo/fastapi",
                "name": "fastapi-examples",
                "description": "FastAPI framework examples",
                "category": "Python"
            },
            {
                "url": "https://github.com/astral-sh/ruff",
                "name": "ruff",
                "description": "Ultra-fast Python linter",
                "category": "Python"
            },
            {
                "url": "https://github.com/psf/black",
                "name": "black",
                "description": "Python code formatter",
                "category": "Python"
            },
            {
                "url": "https://github.com/pre-commit/pre-commit",
                "name": "pre-commit",
                "description": "Git pre-commit hooks framework",
                "category": "Git"
            },
            {
                "url": "https://github.com/charmbracelet/glow",
                "name": "glow",
                "description": "Markdown renderer for terminal",
                "category": "Docs"
            },
            {
                "url": "https://github.com/antonmedv/fx",
                "name": "fx",
                "description": "Terminal JSON viewer",
                "category": "Data Tools"
            },
            {
                "url": "https://github.com/wagoodman/dive",
                "name": "dive",
                "description": "Docker image layer explorer",
                "category": "Docker"
            },
            {
                "url": "https://github.com/httpie/httpie",
                "name": "httpie",
                "description": "Modern HTTP client for testing APIs",
                "category": "API Tools"
            },
            {
                "url": "https://github.com/chubin/cheat.sh",
                "name": "cheatsh",
                "description": "Cheat sheets for command-line",
                "category": "Documentation"
            },
            {
                "url": "https://github.com/cli/cli",
                "name": "gh-cli",
                "description": "GitHub CLI tool",
                "category": "Git"
            }
        ]

        # Group by category
        by_category = {}
        for tool in tools:
            cat = tool["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(tool)

        # Show tools by category
        for category, category_tools in sorted(by_category.items()):
            print(f"\n📦 {category}:")
            for tool in category_tools:
                print(f"  • {tool['name']}: {tool['description']}")

        print(f"\n{'='*60}")
        print(f"Total: {len(tools)} tools available")
        print(f"{'='*60}\n")

        response = input("Download all tools? (y/n/select): ").strip().lower()

        if response == 'y':
            selected_tools = tools
        elif response == 'select':
            print("\nEnter tool names to download (comma-separated):")
            names = input("> ").strip().split(',')
            names = [n.strip() for n in names]
            selected_tools = [t for t in tools if t['name'] in names]
        else:
            logger.info("Download cancelled")
            return

        logger.info(f"\n📥 Downloading {len(selected_tools)} tools...\n")

        success_count = 0
        for tool in selected_tools:
            if self.clone_repo(tool['url'], tool['name']):
                success_count += 1
            print()

        logger.info(f"\n✅ Downloaded {success_count}/{len(selected_tools)} tools")
        logger.info(f"📁 Tools location: {self.tools_dir}")

    def create_tools_index(self):
        """Create an index of downloaded tools"""
        index = {
            "tools_directory": str(self.tools_dir),
            "tools": []
        }

        if not self.tools_dir.exists():
            return

        for item in self.tools_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                tool_info = {
                    "name": item.name,
                    "path": str(item),
                    "git_url": self.get_git_remote(item)
                }

                # Check for README
                for readme_name in ["README.md", "README.rst", "README.txt", "README"]:
                    readme = item / readme_name
                    if readme.exists():
                        tool_info["readme"] = str(readme)
                        break

                index["tools"].append(tool_info)

        # Save index
        index_file = self.tools_dir / "tools_index.json"
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)

        logger.info(f"📋 Tools index created: {index_file}")
        return index

    def get_git_remote(self, repo_path: Path) -> Optional[str]:
        """Get git remote URL for a repository"""
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except:
            return None

    def list_downloaded_tools(self):
        """List all downloaded tools"""
        if not self.tools_dir.exists():
            logger.info("No tools downloaded yet")
            return

        tools = []
        for item in self.tools_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                tools.append(item.name)

        if not tools:
            logger.info("No tools downloaded yet")
            return

        logger.info(f"\n📦 Downloaded Tools ({len(tools)}):\n")
        for tool in sorted(tools):
            remote = self.get_git_remote(self.tools_dir / tool)
            print(f"  • {tool}")
            if remote:
                print(f"    └─ {remote}")
        print()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="GitHub Tools Downloader for GhostLink")
    parser.add_argument("--download", action="store_true", help="Download tools from GitHub")
    parser.add_argument("--list", action="store_true", help="List downloaded tools")
    parser.add_argument("--index", action="store_true", help="Create tools index")
    parser.add_argument("--clone", type=str, help="Clone specific GitHub repo")

    args = parser.parse_args()

    manager = GitHubToolsManager()

    if args.list:
        manager.list_downloaded_tools()

    elif args.index:
        index = manager.create_tools_index()
        if index:
            print(json.dumps(index, indent=2))

    elif args.clone:
        manager.clone_repo(args.clone)

    elif args.download:
        manager.download_useful_tools()
        manager.create_tools_index()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
