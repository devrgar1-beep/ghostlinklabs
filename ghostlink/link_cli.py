"""Link CLI - Command-line interface for your AI brain.

Example usage:
    python -m ghostlink.link_cli start
    python -m ghostlink.link_cli task add "Fix bug in core module"
    python -m ghostlink.link_cli status
    python -m ghostlink.link_cli stop
"""
import asyncio
import sys
from pathlib import Path
from typing import Optional

import click

from .link import Link, TaskPriority, get_link
from .diagnostics_cli import diagnostics
from .git_cli import git


@click.group()
def cli():
    """Link - Your AI orchestration brain."""
    pass


# Add subcommand groups
cli.add_command(diagnostics)
cli.add_command(git)


@cli.command()
@click.option("--name", default="Link", help="Link's display name")
def start(name: str):
    """Start Link's autonomous operation."""
    link = get_link()
    link.name = name
    
    async def run():
        await link.start()
        click.echo(f"🧠 {name} started. Press Ctrl+C to stop.")
        try:
            while link.active:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await link.stop()
    
    asyncio.run(run())


@cli.command()
def stop():
    """Stop Link's operation."""
    link = get_link()
    
    async def run():
        await link.stop()
    
    asyncio.run(run())


@cli.command()
def status():
    """Show Link's current status."""
    link = get_link()
    status = link.get_status()
    
    click.echo(f"\n🧠 {link.name} Status:")
    click.echo(f"  Active: {status['active']}")
    click.echo(f"  Pending tasks: {status['pending_tasks']}")
    click.echo(f"  Completed tasks: {status['completed_tasks']}")
    click.echo(f"  Failed tasks: {status['failed_tasks']}")
    click.echo(f"  Context variables: {status['context_vars']}")
    click.echo(f"  Learned preferences: {status['preferences']}")
    click.echo(f"  History size: {status['history_size']}")


@cli.group()
def task():
    """Task management commands."""
    pass


@task.command("add")
@click.argument("description")
@click.option("--name", help="Task name", default=None)
@click.option(
    "--priority",
    type=click.Choice(["low", "normal", "high", "critical"], case_sensitive=False),
    default="normal",
)
def task_add(description: str, name: Optional[str], priority: str):
    """Add a new task for Link."""
    link = get_link()
    
    priority_map = {
        "low": TaskPriority.LOW,
        "normal": TaskPriority.NORMAL,
        "high": TaskPriority.HIGH,
        "critical": TaskPriority.CRITICAL,
    }
    
    task_name = name or description[:50]
    task = link.add_task(
        task_name,
        description,
        priority=priority_map[priority.lower()],
    )
    
    click.echo(f"✅ Task created: {task.id}")


@task.command("list")
@click.option("--status", help="Filter by status")
def task_list(status: Optional[str]):
    """List all tasks."""
    link = get_link()
    tasks = link.memory.tasks
    
    if status:
        tasks = [t for t in tasks if t.status.value == status.lower()]
    
    if not tasks:
        click.echo("No tasks found.")
        return
    
    click.echo(f"\n📋 Tasks ({len(tasks)}):")
    for task in tasks:
        click.echo(f"  [{task.status.value.upper()}] {task.name}")
        click.echo(f"    Priority: {task.priority.name}")
        click.echo(f"    Created: {task.created_at}")
        if task.error:
            click.echo(f"    Error: {task.error}")


@cli.group()
def context():
    """Context management commands."""
    pass


@context.command("set")
@click.argument("key")
@click.argument("value")
def context_set(key: str, value: str):
    """Set a context variable."""
    link = get_link()
    link.set_context(key, value)
    click.echo(f"✅ Context set: {key} = {value}")


@context.command("get")
@click.argument("key")
def context_get(key: str):
    """Get a context variable."""
    link = get_link()
    value = link.get_context(key)
    
    if value is None:
        click.echo(f"❌ Context variable '{key}' not found")
    else:
        click.echo(f"{key} = {value}")


@context.command("list")
def context_list():
    """List all context variables."""
    link = get_link()
    
    if not link.memory.context:
        click.echo("No context variables set.")
        return
    
    click.echo("\n🔍 Context Variables:")
    for key, value in link.memory.context.items():
        click.echo(f"  {key} = {value}")


@cli.group()
def learn():
    """Learning and preferences commands."""
    pass


@learn.command("set")
@click.argument("key")
@click.argument("value")
def learn_set(key: str, value: str):
    """Teach Link a preference."""
    link = get_link()
    link.learn_preference(key, value)


@learn.command("list")
def learn_list():
    """List learned preferences."""
    link = get_link()
    
    if not link.memory.preferences:
        click.echo("No preferences learned yet.")
        return
    
    click.echo("\n📚 Learned Preferences:")
    for key, value in link.memory.preferences.items():
        click.echo(f"  {key} = {value}")


@cli.command()
def history():
    """Show Link's execution history."""
    link = get_link()
    
    if not link.memory.history:
        click.echo("No history yet.")
        return
    
    click.echo(f"\n📜 History ({len(link.memory.history)} entries):")
    for entry in link.memory.history[-10:]:  # Last 10
        task = entry["task"]
        click.echo(f"  [{entry['timestamp']}] {task['name']}")
        click.echo(f"    Status: {task['status']}")


@cli.command()
@click.option("--confirm", is_flag=True, help="Confirm memory wipe")
def reset(confirm: bool):
    """Reset Link's memory."""
    if not confirm:
        click.echo("⚠️  This will erase all of Link's memory!")
        click.echo("Use --confirm flag to proceed.")
        return
    
    link = get_link()
    link.memory = type(link.memory)()  # Fresh memory
    link.memory.save(link.memory_path)
    click.echo("✅ Memory reset complete.")


if __name__ == "__main__":
    cli()
