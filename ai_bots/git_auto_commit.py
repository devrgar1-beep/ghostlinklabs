#!/usr/bin/env python3
"""
Auto-commit wrapper for git operations
Automatically commits changes after every action
"""
from datetime import datetime
import os
from pathlib import Path
import subprocess
from typing import Optional


class GitAutoCommit:
    """Automatically commit changes to git after actions"""
    
    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize auto-commit
        
        Args:
            repo_path: Path to git repository (defaults to current directory)
        """
        self.repo_path = Path(repo_path or os.getcwd())
        self.enabled = True
        
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception:
            return False
            
    def get_status(self) -> str:
        """Get git status output"""
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error getting status: {e}"
            
    def has_changes(self) -> bool:
        """Check if there are uncommitted changes"""
        status = self.get_status()
        return bool(status)
        
    def commit(
        self,
        message: Optional[str] = None,
        action: Optional[str] = None
    ) -> bool:
        """
        Commit all changes with auto-generated message
        
        Args:
            message: Custom commit message (optional)
            action: Action description for auto-generated message
            
        Returns:
            True if commit succeeded, False otherwise
        """
        if not self.enabled:
            return False
            
        if not self.is_git_repo():
            return False
            
        if not self.has_changes():
            return False
            
        try:
            # Stage all changes
            subprocess.run(
                ["git", "add", "."],
                cwd=self.repo_path,
                capture_output=True,
                timeout=10,
                check=True
            )
            
            # Generate commit message
            if not message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if action:
                    message = f"[AUTO] {action} - {timestamp}"
                else:
                    message = f"[AUTO] Automated commit - {timestamp}"
            
            # Commit changes
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.repo_path,
                capture_output=True,
                timeout=10,
                check=True
            )
            
            return True
            
        except subprocess.CalledProcessError:
            # Commit may fail if there are no staged changes
            return False
        except Exception as e:
            print(f"Auto-commit error: {e}")
            return False
            
    def commit_with_action(self, action: str, details: str = "") -> bool:
        """
        Commit with action-specific message
        
        Args:
            action: Action type (e.g., "Command executed", "Bot action")
            details: Additional details about the action
            
        Returns:
            True if commit succeeded
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[AUTO] {action}"
        if details:
            message += f": {details}"
        message += f" - {timestamp}"
        
        return self.commit(message=message)
        
    def enable(self):
        """Enable auto-commit"""
        self.enabled = True
        
    def disable(self):
        """Disable auto-commit"""
        self.enabled = False
        
    def toggle(self) -> bool:
        """Toggle auto-commit on/off"""
        self.enabled = not self.enabled
        return self.enabled


# Global instance
_auto_commit_instance = None


def get_auto_commit(repo_path: Optional[str] = None) -> GitAutoCommit:
    """Get or create global auto-commit instance"""
    global _auto_commit_instance
    if _auto_commit_instance is None:
        _auto_commit_instance = GitAutoCommit(repo_path)
    return _auto_commit_instance


def auto_commit(action: str, details: str = "") -> bool:
    """
    Convenience function for auto-committing
    
    Args:
        action: Action description
        details: Additional details
        
    Returns:
        True if commit succeeded
    """
    committer = get_auto_commit()
    return committer.commit_with_action(action, details)
