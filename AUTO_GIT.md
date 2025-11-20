# Automatic Git Operations - Auto Merge & Auto Pull

GhostLink now includes **automatic git operations** with intelligent conflict resolution.

## 🚀 Features

### Auto Pull
- **Automatic pulling** from remote branches
- **Conflict detection** and resolution
- **Rebase by default** for cleaner history
- **Status checking** before pull
- **Automatic retry** after conflict resolution

### Auto Merge
- **Multiple merge strategies** (ours, theirs, recursive, octopus, resolve)
- **Intelligent conflict resolution**
- **Branch switching** if needed
- **Automatic conflict markers** handling
- **Merge history tracking**

### Auto Sync
- **Combined pull + merge** operation
- **Syncs with main/master** branch
- **Full repository synchronization**
- **Handles all conflicts** automatically

### Conflict Resolution
- **Automatic detection** of conflict files
- **Smart resolution strategies**
- **Preserves both changes** option
- **Manual fallback** for complex conflicts
- **Detailed conflict reporting**

## 📦 Components

### 1. AutoGit (`ghostlink/auto_git.py`)

Core auto-git functionality:

```python
from ghostlink import get_auto_git

auto_git = get_auto_git()

# Auto pull
result = await auto_git.auto_pull()

# Auto merge
result = await auto_git.auto_merge("feature-branch")

# Full sync
results = await auto_git.sync()
```

**Features**:
- Git repository detection
- Branch management
- Status checking
- Conflict resolution
- Operation history

### 2. Git CLI (`ghostlink/git_cli.py`)

Command-line interface:

```bash
# Auto pull
link git pull

# Auto merge
link git merge feature-branch

# Full sync
link git sync

# Git status
link git status

# Configure
link git config --auto-pull --auto-merge

# Abort merge
link git abort
```

## 🎯 Usage

### Quick Start

```bash
# Pull from remote with auto-conflict resolution
link git pull

# Sync with main branch
link git sync

# Merge a feature branch
link git merge feature-xyz --strategy ours
```

### Python API

```python
from ghostlink.auto_git import get_auto_git, MergeStrategy

auto_git = get_auto_git()

# Enable all features
auto_git.auto_pull_enabled = True
auto_git.auto_merge_enabled = True
auto_git.auto_resolve_conflicts = True

# Pull with automatic conflict resolution
result = await auto_git.auto_pull()
if result.status.value == "success":
    print(f"✓ {result.message}")
    if result.auto_resolved:
        print(f"Auto-resolved {len(result.conflicts)} conflicts")

# Merge with specific strategy
result = await auto_git.auto_merge(
    "feature-branch",
    strategy=MergeStrategy.OURS
)

# Full repository sync
results = await auto_git.sync()
print(f"Pull: {results['pull'].message}")
if 'merge' in results:
    print(f"Merge: {results['merge'].message}")
```

### Configuration

```bash
# Enable all auto-git features
link git config --auto-pull --auto-merge --auto-resolve

# Set merge strategy
link git config --strategy ours

# Disable auto-resolve
link git config --no-auto-resolve

# View current config
link git status
```

## 🔧 CLI Commands

### `link git pull`
Automatically pull from remote with conflict resolution.

**Options**:
- `--branch, -b` - Branch to pull (default: current)

**Example**:
```bash
link git pull
link git pull --branch develop
```

### `link git merge`
Automatically merge branches with conflict resolution.

**Arguments**:
- `source_branch` - Branch to merge from

**Options**:
- `--target, -t` - Target branch (default: current)
- `--strategy, -s` - Merge strategy (ours/theirs/recursive/auto)

**Example**:
```bash
link git merge feature-auth
link git merge hotfix --target main --strategy ours
```

### `link git sync`
Full sync: pull and merge with main/master.

**Options**:
- `--branch, -b` - Branch to sync (default: current)

**Example**:
```bash
link git sync
link git sync --branch feature-xyz
```

### `link git status`
Show git status and auto-git configuration.

**Example**:
```bash
link git status
```

**Output**:
```
============================================================
Git Status
============================================================

Current Branch: feature-xyz
Uncommitted Changes: No

Auto-Git Configuration:
  Auto-pull: Enabled
  Auto-merge: Enabled
  Auto-resolve conflicts: Enabled
  Merge strategy: recursive

Recent Operations:
  14:23:45 - success: Successfully pulled main
  14:25:12 - success: Merged with auto-resolved conflicts
```

### `link git config`
Configure auto-git settings.

**Options**:
- `--auto-pull / --no-auto-pull` - Enable/disable auto-pull
- `--auto-merge / --no-auto-merge` - Enable/disable auto-merge
- `--auto-resolve / --no-auto-resolve` - Enable/disable auto-resolve
- `--strategy` - Set default merge strategy

**Example**:
```bash
link git config --auto-pull --auto-merge
link git config --strategy ours
link git config --no-auto-resolve
```

### `link git abort`
Abort an ongoing merge.

**Example**:
```bash
link git abort
```

## 📊 Merge Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| **auto** | Let git decide | Most cases |
| **recursive** | Default 3-way merge | Standard merges |
| **ours** | Prefer our changes | Keeping local work |
| **theirs** | Prefer their changes | Accepting upstream |
| **octopus** | Multiple branches | Merging many branches |
| **resolve** | Classic merge | Simple cases |

## 🎓 Examples

### Example 1: Simple Pull

```bash
$ link git pull

Pulling from remote...
✓ Successfully pulled main
```

### Example 2: Pull with Conflicts (Auto-resolved)

```bash
$ link git pull

Pulling from remote...
✓ Successfully pulled main
  Auto-resolved 3 conflicts
```

### Example 3: Merge Feature Branch

```bash
$ link git merge feature-auth

Merging feature-auth → current branch...
✓ Successfully merged feature-auth into main
```

### Example 4: Merge with Conflicts

```bash
$ link git merge feature-xyz

Merging feature-xyz → main...
⚠ Merge has conflicts: file1.py, file2.py

Conflicts in:
  - file1.py
  - file2.py

Tip: Run 'link git abort' to cancel the merge
```

### Example 5: Full Sync

```bash
$ link git sync

Syncing repository...
✓ Pull: Successfully pulled main
✓ Merge: Successfully merged origin/main into feature-xyz
```

### Example 6: Configure Strategy

```bash
$ link git config --strategy ours

✓ Default merge strategy set to: ours

$ link git merge feature-abc
Merging feature-abc → main...
✓ Successfully merged feature-abc into main
```

## 🔄 Conflict Resolution

### How It Works

1. **Detect conflicts** - Identifies files with merge markers
2. **Analyze conflicts** - Determines conflict type
3. **Apply strategy** - Uses configured merge strategy
4. **Verify resolution** - Ensures conflicts are resolved
5. **Complete merge** - Commits the merge

### Automatic Resolution

AutoGit can automatically resolve conflicts using:
- **"ours" strategy** - Keep local changes
- **"theirs" strategy** - Accept remote changes
- **Smart merging** - For non-overlapping changes

### Manual Fallback

If auto-resolution fails:
1. Conflicts are reported with file list
2. Manual resolution required
3. Or use `link git abort` to cancel

## 🎮 VS Code Integration

### New Tasks

- **Git: Auto Pull** - Pull with conflict resolution
- **Git: Auto Sync** - Full repository sync
- **Git: Status** - View git and auto-git status
- **Git: Abort Merge** - Cancel ongoing merge

Access via:
- Command Palette: `Tasks: Run Task`
- Terminal menu
- Keyboard shortcut

### Settings

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

## 🔒 Safety Features

- ✅ **Uncommitted changes check** - Warns before operations
- ✅ **Branch validation** - Verifies branches exist
- ✅ **Conflict detection** - Identifies all conflicts
- ✅ **Operation history** - Tracks all operations
- ✅ **Abort capability** - Can cancel merges
- ✅ **Error handling** - Integrated with troubleshooter

## 📈 Operation Tracking

View operation history:

```python
from ghostlink import get_auto_git

auto_git = get_auto_git()

# View recent operations
for op in auto_git.operation_history:
    print(f"{op.timestamp}: {op.status} - {op.message}")
    if op.conflicts:
        print(f"  Conflicts: {', '.join(op.conflicts)}")
    if op.auto_resolved:
        print(f"  ✓ Auto-resolved")
```

## 🎯 Best Practices

1. **Commit before operations** - Commit local changes first
2. **Use sync regularly** - Keep branches up to date
3. **Review auto-resolved conflicts** - Check what was resolved
4. **Choose strategy wisely** - Pick appropriate merge strategy
5. **Monitor operation history** - Track what happened
6. **Test after auto-merge** - Verify merged code works

## 🚦 Integration with Link

Auto-git integrates with Link agent:

```python
from ghostlink import get_link

link = get_link()

# Add git sync as a scheduled task
link.add_task(
    "Sync repository",
    "Pull and merge latest changes",
    priority=TaskPriority.NORMAL
)

# Register git handler
async def git_sync_handler(task):
    auto_git = get_auto_git()
    results = await auto_git.sync()
    return results

link.register_handler("git_sync", git_sync_handler)
```

## 🔧 Advanced Usage

### Custom Conflict Resolution

```python
from ghostlink.auto_git import get_auto_git

auto_git = get_auto_git()

# Disable auto-resolve for manual control
auto_git.auto_resolve_conflicts = False

result = await auto_git.auto_pull()
if result.status.value == "conflict":
    print(f"Conflicts: {result.conflicts}")
    # Handle manually
    # Then: git add . && git commit
```

### Periodic Sync

```python
import asyncio
from ghostlink.auto_git import get_auto_git

async def periodic_sync(interval: int = 300):
    """Sync repository every interval seconds."""
    auto_git = get_auto_git()
    
    while True:
        await asyncio.sleep(interval)
        results = await auto_git.sync()
        if results['pull'].status.value == "success":
            print("Repository synced")
```

---

**Auto-git operations are now enabled! Start using with:**

```bash
link git pull
link git sync
```

For complete documentation, see:
- `ghostlink/auto_git.py` - Core implementation
- `ghostlink/git_cli.py` - CLI commands
