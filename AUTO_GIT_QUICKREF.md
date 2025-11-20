# Auto Git - Quick Reference

## CLI Commands

```bash
# Pull from remote
link git pull
link git pull --branch develop

# Merge branches
link git merge feature-branch
link git merge hotfix --target main --strategy ours

# Full sync (pull + merge)
link git sync
link git sync --branch feature-xyz

# Git status
link git status

# Configure
link git config --auto-pull --auto-merge
link git config --strategy ours
link git config --no-auto-resolve

# Abort merge
link git abort
```

## Merge Strategies

- `auto` - Let git decide (default)
- `recursive` - Standard 3-way merge
- `ours` - Prefer our changes
- `theirs` - Prefer their changes
- `octopus` - Multiple branches
- `resolve` - Classic merge

## Python API

```python
from ghostlink.auto_git import get_auto_git, MergeStrategy

auto_git = get_auto_git()

# Pull
result = await auto_git.auto_pull()

# Merge
result = await auto_git.auto_merge("feature-branch", strategy=MergeStrategy.OURS)

# Sync
results = await auto_git.sync()

# Check status
status = auto_git.get_status()

# Configure
auto_git.auto_pull_enabled = True
auto_git.auto_merge_enabled = True
auto_git.auto_resolve_conflicts = True
```

## Configuration

```json
{
  "ghostlink.autoGit.enabled": true,
  "ghostlink.autoGit.autoPull": true,
  "ghostlink.autoGit.autoMerge": true,
  "ghostlink.autoGit.autoResolveConflicts": true,
  "ghostlink.autoGit.defaultStrategy": "recursive",
  "ghostlink.autoGit.pullOnStartup": false,
  "ghostlink.autoGit.syncInterval": 300
}
```

## VS Code Tasks

- **Git: Auto Pull** - Pull with conflict resolution
- **Git: Auto Sync** - Full repository sync
- **Git: Status** - View git status
- **Git: Abort Merge** - Cancel merge

## Examples

```bash
# Example 1: Daily sync
link git sync

# Example 2: Merge feature with our changes
link git merge feature-auth --strategy ours

# Example 3: View status
link git status

# Example 4: Pull specific branch
link git pull --branch develop
```
