"""Tests for git CLI commands with uncommitted changes detection."""
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from ghostlink.git_cli import git
from ghostlink.auto_git import AutoGit, GitOperationResult, GitOperationStatus


@pytest.fixture
def temp_git_repo():
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = Path(tmpdir)
        
        # Initialize git repo
        subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True, capture_output=True)
        
        # Create initial commit
        (repo_path / "README.md").write_text("# Test Repo")
        subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True, capture_output=True)
        
        yield repo_path


def create_success_result(message: str, changes: dict) -> GitOperationResult:
    """Helper to create a successful GitOperationResult."""
    return GitOperationResult(
        status=GitOperationStatus.SUCCESS,
        message=message,
        conflicts=[],
        changes=changes,
        timestamp=datetime.now()
    )


class TestGitCliUncommittedChanges:
    """Test git CLI behavior with uncommitted changes."""
    
    def test_pull_blocked_by_uncommitted_changes(self, temp_git_repo):
        """Test that pull is blocked when uncommitted changes exist."""
        # Create an uncommitted change
        (temp_git_repo / "test.txt").write_text("uncommitted content")
        
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = True
            mock_auto_git.repo_path = temp_git_repo
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['pull'])
            
            # Should warn about uncommitted changes
            assert result.exit_code == 0
            assert "Uncommitted changes detected" in result.output
            assert "Use --force flag to proceed" in result.output
            
            # auto_pull should not be called
            mock_auto_git.auto_pull.assert_not_called()
    
    def test_pull_proceeds_with_force_flag(self, temp_git_repo):
        """Test that pull proceeds when --force flag is used."""
        # Create an uncommitted change
        (temp_git_repo / "test.txt").write_text("uncommitted content")
        
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = True
            mock_auto_git.repo_path = temp_git_repo
            
            # Mock successful pull result
            mock_result = create_success_result(
                "Successfully pulled main",
                {"branch": "main"}
            )
            
            async def mock_auto_pull(branch):
                return mock_result
            
            mock_auto_git.auto_pull = mock_auto_pull
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['pull', '--force'])
            
            # Should proceed with pull
            assert result.exit_code == 0
            assert "Pulling from remote" in result.output
            assert "Successfully pulled" in result.output
    
    def test_merge_blocked_by_uncommitted_changes(self, temp_git_repo):
        """Test that merge is blocked when uncommitted changes exist."""
        # Create an uncommitted change
        (temp_git_repo / "test.txt").write_text("uncommitted content")
        
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = True
            mock_auto_git.repo_path = temp_git_repo
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['merge', 'feature-branch'])
            
            # Should warn about uncommitted changes
            assert result.exit_code == 0
            assert "Uncommitted changes detected" in result.output
            assert "Use --force flag to proceed" in result.output
            
            # auto_merge should not be called
            mock_auto_git.auto_merge.assert_not_called()
    
    def test_merge_proceeds_with_force_flag(self, temp_git_repo):
        """Test that merge proceeds when --force flag is used."""
        # Create an uncommitted change
        (temp_git_repo / "test.txt").write_text("uncommitted content")
        
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = True
            mock_auto_git.repo_path = temp_git_repo
            
            # Mock successful merge result
            mock_result = create_success_result(
                "Successfully merged feature-branch into main",
                {"source": "feature-branch", "target": "main"}
            )
            
            async def mock_auto_merge(source, target, strategy):
                return mock_result
            
            mock_auto_git.auto_merge = mock_auto_merge
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['merge', 'feature-branch', '--force'])
            
            # Should proceed with merge
            assert result.exit_code == 0
            assert "Merging feature-branch" in result.output
            assert "Successfully merged" in result.output
    
    def test_sync_blocked_by_uncommitted_changes(self, temp_git_repo):
        """Test that sync is blocked when uncommitted changes exist."""
        # Create an uncommitted change
        (temp_git_repo / "test.txt").write_text("uncommitted content")
        
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = True
            mock_auto_git.repo_path = temp_git_repo
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['sync'])
            
            # Should warn about uncommitted changes
            assert result.exit_code == 0
            assert "Uncommitted changes detected" in result.output
            assert "Use --force flag to proceed" in result.output
            
            # sync should not be called
            mock_auto_git.sync.assert_not_called()
    
    def test_sync_proceeds_with_force_flag(self, temp_git_repo):
        """Test that sync proceeds when --force flag is used."""
        # Create an uncommitted change
        (temp_git_repo / "test.txt").write_text("uncommitted content")
        
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = True
            mock_auto_git.repo_path = temp_git_repo
            
            # Mock successful sync result
            mock_pull_result = create_success_result(
                "Successfully pulled main",
                {"branch": "main"}
            )
            
            async def mock_sync(branch):
                return {"pull": mock_pull_result}
            
            mock_auto_git.sync = mock_sync
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['sync', '--force'])
            
            # Should proceed with sync
            assert result.exit_code == 0
            assert "Syncing repository" in result.output
    
    def test_operations_proceed_without_uncommitted_changes(self, temp_git_repo):
        """Test that operations proceed normally when there are no uncommitted changes."""
        # Mock the AutoGit instance
        with patch('ghostlink.git_cli.get_auto_git') as mock_get_auto_git:
            mock_auto_git = MagicMock(spec=AutoGit)
            mock_auto_git.is_git_repo.return_value = True
            mock_auto_git.has_uncommitted_changes.return_value = False
            mock_auto_git.repo_path = temp_git_repo
            
            # Mock successful pull result
            mock_result = create_success_result(
                "Successfully pulled main",
                {"branch": "main"}
            )
            
            async def mock_auto_pull(branch):
                return mock_result
            
            mock_auto_git.auto_pull = mock_auto_pull
            mock_get_auto_git.return_value = mock_auto_git
            
            runner = CliRunner()
            result = runner.invoke(git, ['pull'])
            
            # Should proceed without warning
            assert result.exit_code == 0
            assert "Uncommitted changes detected" not in result.output
            assert "Pulling from remote" in result.output
            assert "Successfully pulled" in result.output
