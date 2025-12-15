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
import json

import click

from .link import Link, TaskPriority, get_link
from .diagnostics_cli import diagnostics
from .git_cli import git
from .system_audit import SystemAuditor
from .orchestrator import PipelineOrchestrator
from .health import HealthMonitor, HealthCheckService


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


@cli.group()
def audit():
    """System audit commands."""
    pass


@audit.command("run")
@click.option("--save-report", is_flag=True, default=True, help="Save audit report")
@click.option("--show-findings", is_flag=True, help="Show detailed findings")
def audit_run(save_report: bool, show_findings: bool):
    """Run system audit."""
    click.echo("🔍 Running system audit...")

    auditor = SystemAuditor()
    report = auditor.audit()

    # Display summary
    audit_data = report["audit"]
    click.echo(f"\n✓ Audit complete in {audit_data['duration_seconds']:.2f}s")
    click.echo(f"Status: {audit_data['status']}")

    summary = audit_data["findings_summary"]
    click.echo(f"Findings: {summary['total']} total")
    if summary["critical"] > 0:
        click.echo(f"  🔴 Critical: {summary['critical']}")
    if summary["errors"] > 0:
        click.echo(f"  ⚠️  Error: {summary['errors']}")
    if summary["warnings"] > 0:
        click.echo(f"  ⚡ Warning: {summary['warnings']}")
    if summary["total"] == 0:
        click.echo("  ✅ No issues found")

    # Show findings if requested
    if show_findings and report["findings"]:
        click.echo("\n📋 Findings:")
        for finding in report["findings"]:
            level = finding["level"]
            if level == "CRITICAL":
                symbol = "🔴"
            elif level == "ERROR":
                symbol = "⚠️ "
            elif level == "WARNING":
                symbol = "⚡"
            else:
                symbol = "ℹ️ "

            click.echo(f"\n  {symbol} [{finding['category']}] {finding['title']}")
            click.echo(f"     {finding['message']}")
            if finding.get("recommendations"):
                click.echo(f"     Recommendation: {finding['recommendations'][0]}")

    # Show system info
    system = report["system"]
    click.echo(f"\n🖥️  System Info:")
    click.echo(f"  Platform: {system['platform']}")
    click.echo(f"  Python: {system['python_version']}")
    click.echo(f"  CPUs: {system['cpu_count']}")


@audit.command("view")
def audit_view():
    """View latest audit report."""
    report_path = Path.home() / ".local" / "share" / "ghostlink" / "audit_report.json"

    if not report_path.exists():
        click.echo("❌ No audit report found. Run 'ghostlink audit run' first.")
        return

    with open(report_path) as f:
        report = json.load(f)

    # Display in formatted way
    audit_data = report["audit"]
    click.echo(f"📊 Latest Audit Report")
    click.echo(f"Timestamp: {audit_data['timestamp']}")
    click.echo(f"Status: {audit_data['status']}")
    summary = audit_data["findings_summary"]
    click.echo(f"Findings: {summary['total']} ({summary['critical']} critical, {summary['errors']} errors, {summary['warnings']} warnings)")


@cli.group()
def health():
    """Health monitoring commands."""
    pass


@health.command("check")
@click.option("--export", is_flag=True, help="Export to JSON")
def health_check(export: bool):
    """Check system health."""
    click.echo("🏥 Checking system health...")

    service = HealthCheckService(check_interval=5)
    result = service.perform_check()

    click.echo(f"\n✓ Health check complete")
    click.echo(f"Status: {result['overall_status'].upper()}")

    checks = result["checks"]
    click.echo(f"\n📊 Metrics:")
    click.echo(f"  CPU: {checks['cpu']['value']:.1f}% ({checks['cpu']['status']})")
    click.echo(f"  Memory: {checks['memory']['value']:.1f}% ({checks['memory']['status']})")
    click.echo(f"  Disk: {checks['disk']['value']:.1f}% ({checks['disk']['status']})")

    if export:
        export_file = Path.home() / ".local" / "share" / "ghostlink" / "health_check.json"
        export_file.parent.mkdir(parents=True, exist_ok=True)
        with open(export_file, "w") as f:
            json.dump(result, f, indent=2, default=str)
        click.echo(f"\n✓ Exported to {export_file}")
@health.command("monitor")
@click.option("--duration", default=60, help="Monitoring duration in seconds")
@click.option("--interval", default=5, help="Update interval in seconds")
def health_monitor(duration: int, interval: int):
    """Monitor system health in real-time."""
    click.echo(f"🔴 Monitoring system health for {duration}s (interval: {interval}s)...")
    click.echo("Press Ctrl+C to stop\n")

    async def run():
        monitor = HealthMonitor(update_interval=interval)
        task = monitor.start()

        try:
            elapsed = 0
            while elapsed < duration:
                await asyncio.sleep(interval)
                latest = monitor.get_latest()

                if latest:
                    status_symbol = "✅" if latest.overall_status == "HEALTHY" else "⚠️ " if latest.overall_status == "WARNING" else "🔴"
                    click.echo(f"{status_symbol} CPU: {latest.cpu_percent:.1f}% | Memory: {latest.memory_percent:.1f}% | Disk: {latest.disk_percent:.1f}% | Status: {latest.overall_status}")

                elapsed += interval
        except KeyboardInterrupt:
            click.echo("\n⏹️  Monitoring stopped")
        finally:
            monitor.stop()
            await task

            # Show summary
            report = monitor.get_report()
            click.echo(f"\n📊 Summary:")
            click.echo(f"  Avg CPU: {report['averages']['avg_cpu']:.1f}%")
            click.echo(f"  Avg Memory: {report['averages']['avg_memory']:.1f}%")
            click.echo(f"  Avg Disk: {report['averages']['avg_disk']:.1f}%")
            click.echo(f"  Samples: {report['history_size']}")

    asyncio.run(run())


@health.command("export")
@click.option("--output", help="Output file path", default=None)
def health_export(output: Optional[str]):
    """Export health history to JSON."""
    service = HealthCheckService()

    if output:
        output_path = Path(output)
    else:
        output_path = Path.home() / ".local" / "share" / "ghostlink" / "health_history.json"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Get current check and save
    result = service.perform_check()
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    click.echo(f"✓ Exported to {output_path}")


@cli.group()
def pipeline():
    """Pipeline orchestration commands."""
    pass


@pipeline.command("create")
@click.argument("name")
@click.option("--description", help="Pipeline description")
def pipeline_create(name: str, description: Optional[str]):
    """Create a new pipeline."""
    pipeline = PipelineOrchestrator(name, description or "")
    click.echo(f"✅ Pipeline created: {name}")
    click.echo(f"   ID: {pipeline.pipeline_id}")


@pipeline.command("execute")
@click.argument("name")
@click.option("--save-report", is_flag=True, default=True, help="Save execution report")
@click.option("--parallel", is_flag=True, help="Enable parallel execution")
def pipeline_execute(name: str, save_report: bool, parallel: bool):
    """Execute a pipeline by name."""
    click.echo(f"▶️  Executing pipeline '{name}'...")

    # This is a placeholder - in real implementation, would load pipeline from storage
    pipeline = PipelineOrchestrator(name, "Executing pipeline")

    click.echo("Note: Create actual pipeline tasks via API to execute them.")
    click.echo("See documentation for pipeline execution examples.")


@pipeline.command("list")
def pipeline_list():
    """List available pipelines."""
    click.echo("📋 Pipelines:")
    click.echo("  Note: Use API to create and list pipelines")
    click.echo("  See: ghostlink pipeline create --help")


if __name__ == "__main__":
    cli()
