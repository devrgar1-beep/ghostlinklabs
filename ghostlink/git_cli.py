"""CLI commands for automatic git operations.

Provides command-line interface for auto-pull, auto-merge, and git sync.
"""
import asyncio
import click

from .auto_git import get_auto_git, MergeStrategy


@click.group()
def git():
    """Automatic git operations."""
    pass


@git.command()
@click.option('--branch', '-b', help='Branch to pull (default: current)')
def pull(branch):
    """Automatically pull from remote with conflict resolution."""
    async def _pull():
        auto_git = get_auto_git()
        
        if not auto_git.is_git_repo():
            click.secho("✗ Not a git repository", fg="red")
            return
        
        click.echo(f"Pulling from remote...")
        result = await auto_git.auto_pull(branch)
        
        if result.status.value == "success":
            click.secho(f"✓ {result.message}", fg="green")
            if result.auto_resolved:
                click.secho(f"  Auto-resolved {len(result.conflicts)} conflicts", fg="yellow")
        elif result.status.value == "no_changes":
            click.secho(f"✓ {result.message}", fg="cyan")
        elif result.status.value == "conflict":
            click.secho(f"⚠ {result.message}", fg="yellow")
            click.echo("\nConflicts in:")
            for conflict in result.conflicts:
                click.echo(f"  - {conflict}")
        else:
            click.secho(f"✗ {result.message}", fg="red")
    
    asyncio.run(_pull())


@git.command()
@click.argument('source_branch')
@click.option('--target', '-t', help='Target branch (default: current)')
@click.option('--strategy', '-s', 
              type=click.Choice(['ours', 'theirs', 'recursive', 'auto']),
              default='auto',
              help='Merge strategy')
def merge(source_branch, target, strategy):
    """Automatically merge branches with conflict resolution."""
    async def _merge():
        auto_git = get_auto_git()
        
        if not auto_git.is_git_repo():
            click.secho("✗ Not a git repository", fg="red")
            return
        
        strategy_enum = MergeStrategy[strategy.upper()]
        
        click.echo(f"Merging {source_branch} → {target or 'current branch'}...")
        result = await auto_git.auto_merge(source_branch, target, strategy_enum)
        
        if result.status.value == "success":
            click.secho(f"✓ {result.message}", fg="green")
            if result.auto_resolved:
                click.secho(f"  Auto-resolved {len(result.conflicts)} conflicts", fg="yellow")
        elif result.status.value == "conflict":
            click.secho(f"⚠ {result.message}", fg="yellow")
            click.echo("\nConflicts in:")
            for conflict in result.conflicts:
                click.echo(f"  - {conflict}")
            click.echo("\nTip: Run 'link git abort' to cancel the merge")
        else:
            click.secho(f"✗ {result.message}", fg="red")
    
    asyncio.run(_merge())


@git.command()
@click.option('--branch', '-b', help='Branch to sync (default: current)')
def sync(branch):
    """Full sync: pull and merge with main/master."""
    async def _sync():
        auto_git = get_auto_git()
        
        if not auto_git.is_git_repo():
            click.secho("✗ Not a git repository", fg="red")
            return
        
        click.echo("Syncing repository...")
        results = await auto_git.sync(branch)
        
        # Show pull result
        pull_result = results.get("pull")
        if pull_result:
            if pull_result.status.value == "success":
                click.secho(f"✓ Pull: {pull_result.message}", fg="green")
            elif pull_result.status.value == "no_changes":
                click.secho(f"✓ Pull: {pull_result.message}", fg="cyan")
            else:
                click.secho(f"⚠ Pull: {pull_result.message}", fg="yellow")
        
        # Show merge result if applicable
        merge_result = results.get("merge")
        if merge_result:
            if merge_result.status.value == "success":
                click.secho(f"✓ Merge: {merge_result.message}", fg="green")
            elif merge_result.status.value == "conflict":
                click.secho(f"⚠ Merge: {merge_result.message}", fg="yellow")
            else:
                click.secho(f"⚠ Merge: {merge_result.message}", fg="yellow")
    
    asyncio.run(_sync())


@git.command()
def status():
    """Show git status and auto-git configuration."""
    auto_git = get_auto_git()
    
    if not auto_git.is_git_repo():
        click.secho("✗ Not a git repository", fg="red")
        return
    
    status = auto_git.get_status()
    
    click.echo(f"\n{'='*60}")
    click.echo("Git Status")
    click.echo(f"{'='*60}\n")
    
    click.echo(f"Current Branch: {click.style(status['current_branch'], fg='cyan')}")
    click.echo(f"Uncommitted Changes: {click.style('Yes' if status['has_changes'] else 'No', fg='yellow' if status['has_changes'] else 'green')}")
    
    click.echo(f"\nAuto-Git Configuration:")
    click.echo(f"  Auto-pull: {click.style('Enabled' if auto_git.auto_pull_enabled else 'Disabled', fg='green' if auto_git.auto_pull_enabled else 'red')}")
    click.echo(f"  Auto-merge: {click.style('Enabled' if auto_git.auto_merge_enabled else 'Disabled', fg='green' if auto_git.auto_merge_enabled else 'red')}")
    click.echo(f"  Auto-resolve conflicts: {click.style('Enabled' if auto_git.auto_resolve_conflicts else 'Disabled', fg='green' if auto_git.auto_resolve_conflicts else 'red')}")
    click.echo(f"  Merge strategy: {auto_git.default_merge_strategy.value}")
    
    if auto_git.operation_history:
        click.echo(f"\nRecent Operations:")
        for op in auto_git.operation_history[-5:]:
            status_color = {
                "success": "green",
                "conflict": "yellow",
                "failed": "red",
                "no_changes": "cyan"
            }.get(op.status.value, "white")
            click.echo(f"  {op.timestamp.strftime('%H:%M:%S')} - {click.style(op.status.value, fg=status_color)}: {op.message}")


@git.command()
@click.option('--auto-pull/--no-auto-pull', default=None, help='Enable/disable auto-pull')
@click.option('--auto-merge/--no-auto-merge', default=None, help='Enable/disable auto-merge')
@click.option('--auto-resolve/--no-auto-resolve', default=None, help='Enable/disable auto-resolve conflicts')
@click.option('--strategy', type=click.Choice(['ours', 'theirs', 'recursive', 'auto']), help='Default merge strategy')
def config(auto_pull, auto_merge, auto_resolve, strategy):
    """Configure auto-git settings."""
    auto_git = get_auto_git()
    
    if auto_pull is not None:
        auto_git.auto_pull_enabled = auto_pull
        status = "enabled" if auto_pull else "disabled"
        click.secho(f"✓ Auto-pull {status}", fg="green")
    
    if auto_merge is not None:
        auto_git.auto_merge_enabled = auto_merge
        status = "enabled" if auto_merge else "disabled"
        click.secho(f"✓ Auto-merge {status}", fg="green")
    
    if auto_resolve is not None:
        auto_git.auto_resolve_conflicts = auto_resolve
        status = "enabled" if auto_resolve else "disabled"
        click.secho(f"✓ Auto-resolve conflicts {status}", fg="green")
    
    if strategy:
        auto_git.default_merge_strategy = MergeStrategy[strategy.upper()]
        click.secho(f"✓ Default merge strategy set to: {strategy}", fg="green")
    
    if not any([auto_pull is not None, auto_merge is not None, auto_resolve is not None, strategy]):
        click.echo("No configuration changes. Use --help to see options.")


@git.command()
def abort():
    """Abort an ongoing merge."""
    auto_git = get_auto_git()
    
    if not auto_git.is_git_repo():
        click.secho("✗ Not a git repository", fg="red")
        return
    
    if auto_git.abort_merge():
        click.secho("✓ Merge aborted", fg="green")
    else:
        click.secho("✗ No merge to abort or abort failed", fg="red")


if __name__ == '__main__':
    git()
