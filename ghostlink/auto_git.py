"""Automatic Git operations including auto-merge and auto-pull.

Provides autonomous git operations with conflict resolution and integration
with the GhostLink troubleshooting system.
"""
from __future__ import annotations

import asyncio
import logging
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from .troubleshooter import get_troubleshooter, handle_error, ErrorCategory

logger = logging.getLogger(__name__)


class GitOperationStatus(Enum):
    """Git operation status."""
    SUCCESS = "success"
    CONFLICT = "conflict"
    FAILED = "failed"
    NO_CHANGES = "no_changes"


class MergeStrategy(Enum):
    """Git merge strategies."""
    OURS = "ours"  # Prefer our changes
    THEIRS = "theirs"  # Prefer their changes
    RECURSIVE = "recursive"  # Default recursive strategy
    OCTOPUS = "octopus"  # Multiple branches
    RESOLVE = "resolve"  # Classic merge
    AUTO = "auto"  # Let git decide


@dataclass
class GitOperationResult:
    """Result of a git operation."""
    status: GitOperationStatus
    message: str
    conflicts: list[str]
    changes: dict[str, Any]
    timestamp: datetime
    auto_resolved: bool = False


class AutoGit:
    """Automatic git operations manager."""

    def __init__(self, repo_path: Optional[Path] = None):
        """Initialize AutoGit.
        
        Args:
            repo_path: Path to git repository (default: current directory)
        """
        self.repo_path = repo_path or Path.cwd()
        self.auto_pull_enabled = True
        self.auto_merge_enabled = True
        self.auto_resolve_conflicts = True
        self.default_merge_strategy = MergeStrategy.RECURSIVE
        self.operation_history: list[GitOperationResult] = []
        
    def _run_git_command(
        self, 
        *args: str, 
        check: bool = False,
        capture_output: bool = True
    ) -> subprocess.CompletedProcess:
        """Run a git command.
        
        Args:
            *args: Git command arguments
            check: Whether to check return code
            capture_output: Whether to capture output
            
        Returns:
            CompletedProcess result
        """
        cmd = ["git", "-C", str(self.repo_path)] + list(args)
        return subprocess.run(
            cmd,
            capture_output=capture_output,
            text=True,
            check=check
        )

    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository.
        
        Returns:
            True if git repo
        """
        result = self._run_git_command("rev-parse", "--git-dir")
        return result.returncode == 0

    def get_current_branch(self) -> str:
        """Get current git branch name.
        
        Returns:
            Branch name
        """
        result = self._run_git_command("branch", "--show-current")
        return result.stdout.strip()

    def get_remote_branches(self) -> list[str]:
        """Get list of remote branches.
        
        Returns:
            List of remote branch names
        """
        result = self._run_git_command("branch", "-r")
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines()]

    def has_uncommitted_changes(self) -> bool:
        """Check for uncommitted changes.
        
        Returns:
            True if there are uncommitted changes
        """
        result = self._run_git_command("status", "--porcelain")
        return len(result.stdout.strip()) > 0

    def get_status(self) -> dict[str, Any]:
        """Get comprehensive git status.
        
        Returns:
            Dictionary with git status information
        """
        if not self.is_git_repo():
            return {"is_repo": False}
        
        return {
            "is_repo": True,
            "current_branch": self.get_current_branch(),
            "has_changes": self.has_uncommitted_changes(),
            "remote_branches": self.get_remote_branches(),
        }

    async def auto_pull(self, branch: Optional[str] = None) -> GitOperationResult:
        """Automatically pull from remote.
        
        Args:
            branch: Branch to pull (default: current branch)
            
        Returns:
            GitOperationResult with pull status
        """
        if not self.auto_pull_enabled:
            return GitOperationResult(
                status=GitOperationStatus.FAILED,
                message="Auto-pull is disabled",
                conflicts=[],
                changes={},
                timestamp=datetime.now()
            )
        
        try:
            current_branch = branch or self.get_current_branch()
            logger.info(f"Auto-pulling branch: {current_branch}")
            
            # Fetch first
            fetch_result = self._run_git_command("fetch", "--all")
            if fetch_result.returncode != 0:
                return GitOperationResult(
                    status=GitOperationStatus.FAILED,
                    message=f"Fetch failed: {fetch_result.stderr}",
                    conflicts=[],
                    changes={},
                    timestamp=datetime.now()
                )
            
            # Check if pull is needed
            result = self._run_git_command(
                "rev-list",
                f"HEAD..origin/{current_branch}",
                "--count"
            )
            
            if result.stdout.strip() == "0":
                return GitOperationResult(
                    status=GitOperationStatus.NO_CHANGES,
                    message="Already up to date",
                    conflicts=[],
                    changes={},
                    timestamp=datetime.now()
                )
            
            # Pull with rebase
            pull_result = self._run_git_command("pull", "--rebase", "origin", current_branch)
            
            if pull_result.returncode == 0:
                result = GitOperationResult(
                    status=GitOperationStatus.SUCCESS,
                    message=f"Successfully pulled {current_branch}",
                    conflicts=[],
                    changes={"branch": current_branch},
                    timestamp=datetime.now()
                )
                self.operation_history.append(result)
                return result
            
            # Check for conflicts
            if "conflict" in pull_result.stderr.lower() or "conflict" in pull_result.stdout.lower():
                conflicts = self._detect_conflicts()
                
                if self.auto_resolve_conflicts:
                    resolved = await self._auto_resolve_conflicts(conflicts)
                    if resolved:
                        result = GitOperationResult(
                            status=GitOperationStatus.SUCCESS,
                            message=f"Pulled with auto-resolved conflicts",
                            conflicts=conflicts,
                            changes={"branch": current_branch, "resolved": True},
                            timestamp=datetime.now(),
                            auto_resolved=True
                        )
                        self.operation_history.append(result)
                        return result
                
                result = GitOperationResult(
                    status=GitOperationStatus.CONFLICT,
                    message=f"Pull has conflicts: {', '.join(conflicts)}",
                    conflicts=conflicts,
                    changes={"branch": current_branch},
                    timestamp=datetime.now()
                )
                self.operation_history.append(result)
                return result
            
            return GitOperationResult(
                status=GitOperationStatus.FAILED,
                message=f"Pull failed: {pull_result.stderr}",
                conflicts=[],
                changes={},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Auto-pull failed: {e}")
            await handle_error(e, context={"operation": "auto_pull", "branch": branch})
            return GitOperationResult(
                status=GitOperationStatus.FAILED,
                message=str(e),
                conflicts=[],
                changes={},
                timestamp=datetime.now()
            )

    async def auto_merge(
        self,
        source_branch: str,
        target_branch: Optional[str] = None,
        strategy: Optional[MergeStrategy] = None
    ) -> GitOperationResult:
        """Automatically merge branches.
        
        Args:
            source_branch: Branch to merge from
            target_branch: Branch to merge into (default: current branch)
            strategy: Merge strategy to use
            
        Returns:
            GitOperationResult with merge status
        """
        if not self.auto_merge_enabled:
            return GitOperationResult(
                status=GitOperationStatus.FAILED,
                message="Auto-merge is disabled",
                conflicts=[],
                changes={},
                timestamp=datetime.now()
            )
        
        try:
            current_branch = self.get_current_branch()
            target = target_branch or current_branch
            merge_strategy = strategy or self.default_merge_strategy
            
            logger.info(f"Auto-merging {source_branch} into {target}")
            
            # Checkout target branch if needed
            if current_branch != target:
                checkout_result = self._run_git_command("checkout", target)
                if checkout_result.returncode != 0:
                    return GitOperationResult(
                        status=GitOperationStatus.FAILED,
                        message=f"Failed to checkout {target}: {checkout_result.stderr}",
                        conflicts=[],
                        changes={},
                        timestamp=datetime.now()
                    )
            
            # Build merge command
            merge_cmd = ["merge"]
            if merge_strategy != MergeStrategy.AUTO:
                merge_cmd.extend(["-s", merge_strategy.value])
            merge_cmd.append(source_branch)
            
            # Execute merge
            merge_result = self._run_git_command(*merge_cmd)
            
            if merge_result.returncode == 0:
                result = GitOperationResult(
                    status=GitOperationStatus.SUCCESS,
                    message=f"Successfully merged {source_branch} into {target}",
                    conflicts=[],
                    changes={
                        "source": source_branch,
                        "target": target,
                        "strategy": merge_strategy.value
                    },
                    timestamp=datetime.now()
                )
                self.operation_history.append(result)
                return result
            
            # Check for conflicts
            if "conflict" in merge_result.stderr.lower() or "conflict" in merge_result.stdout.lower():
                conflicts = self._detect_conflicts()
                
                if self.auto_resolve_conflicts:
                    resolved = await self._auto_resolve_conflicts(conflicts)
                    if resolved:
                        result = GitOperationResult(
                            status=GitOperationStatus.SUCCESS,
                            message=f"Merged with auto-resolved conflicts",
                            conflicts=conflicts,
                            changes={
                                "source": source_branch,
                                "target": target,
                                "resolved": True
                            },
                            timestamp=datetime.now(),
                            auto_resolved=True
                        )
                        self.operation_history.append(result)
                        return result
                
                result = GitOperationResult(
                    status=GitOperationStatus.CONFLICT,
                    message=f"Merge has conflicts: {', '.join(conflicts)}",
                    conflicts=conflicts,
                    changes={"source": source_branch, "target": target},
                    timestamp=datetime.now()
                )
                self.operation_history.append(result)
                return result
            
            return GitOperationResult(
                status=GitOperationStatus.FAILED,
                message=f"Merge failed: {merge_result.stderr}",
                conflicts=[],
                changes={},
                timestamp=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Auto-merge failed: {e}")
            await handle_error(e, context={"operation": "auto_merge", "source": source_branch})
            return GitOperationResult(
                status=GitOperationStatus.FAILED,
                message=str(e),
                conflicts=[],
                changes={},
                timestamp=datetime.now()
            )

    def _detect_conflicts(self) -> list[str]:
        """Detect files with merge conflicts.
        
        Returns:
            List of files with conflicts
        """
        result = self._run_git_command("diff", "--name-only", "--diff-filter=U")
        if result.returncode != 0:
            return []
        return [line.strip() for line in result.stdout.splitlines() if line.strip()]

    async def _auto_resolve_conflicts(self, conflict_files: list[str]) -> bool:
        """Attempt to automatically resolve conflicts.
        
        Args:
            conflict_files: List of files with conflicts
            
        Returns:
            True if all conflicts resolved
        """
        if not conflict_files:
            return True
        
        logger.info(f"Attempting to auto-resolve {len(conflict_files)} conflicts")
        
        resolved_count = 0
        for file_path in conflict_files:
            try:
                full_path = self.repo_path / file_path
                if not full_path.exists():
                    continue
                
                # Read file content
                content = full_path.read_text()
                
                # Simple conflict resolution: keep both changes with markers
                if "<<<<<<<" in content and ">>>>>>>" in content:
                    # For now, use "ours" strategy for auto-resolution
                    result = self._run_git_command(
                        "checkout", "--ours", str(file_path)
                    )
                    if result.returncode == 0:
                        self._run_git_command("add", str(file_path))
                        resolved_count += 1
                        logger.info(f"Auto-resolved conflict in {file_path} (using ours)")
                    
            except Exception as e:
                logger.warning(f"Could not auto-resolve {file_path}: {e}")
                continue
        
        if resolved_count == len(conflict_files):
            # Complete the merge
            commit_result = self._run_git_command(
                "commit", "--no-edit"
            )
            return commit_result.returncode == 0
        
        return False

    async def sync(self, branch: Optional[str] = None) -> dict[str, GitOperationResult]:
        """Perform full sync: pull and merge.
        
        Args:
            branch: Branch to sync (default: current branch)
            
        Returns:
            Dictionary with pull and merge results
        """
        results = {}
        
        # Pull first
        pull_result = await self.auto_pull(branch)
        results["pull"] = pull_result
        
        # If pull succeeded, check if merge is needed
        if pull_result.status == GitOperationStatus.SUCCESS:
            current_branch = self.get_current_branch()
            if current_branch != "main" and current_branch != "master":
                # Merge main/master into current branch
                main_branch = "main" if "origin/main" in self.get_remote_branches() else "master"
                merge_result = await self.auto_merge(f"origin/{main_branch}")
                results["merge"] = merge_result
        
        return results

    def abort_merge(self) -> bool:
        """Abort an ongoing merge.
        
        Returns:
            True if merge aborted successfully
        """
        result = self._run_git_command("merge", "--abort")
        return result.returncode == 0


# Global AutoGit instance
_auto_git: Optional[AutoGit] = None


def get_auto_git() -> AutoGit:
    """Get global AutoGit instance.
    
    Returns:
        AutoGit singleton
    """
    global _auto_git
    if _auto_git is None:
        _auto_git = AutoGit()
    return _auto_git
