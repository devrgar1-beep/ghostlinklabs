"""CLI commands for troubleshooting and diagnostics.

Extends Link CLI with automatic troubleshooting and health monitoring commands.
"""
import asyncio
import json
import sys
from pathlib import Path

import click

from .troubleshooter import get_troubleshooter
from .health_monitor import get_health_monitor


@click.group()
def diagnostics():
    """Troubleshooting and diagnostics commands."""
    pass


@diagnostics.command()
def health():
    """Check system health."""
    async def _check():
        monitor = get_health_monitor()
        status = await monitor.check_health()
        
        # Print status
        status_colors = {
            "healthy": "green",
            "warning": "yellow",
            "critical": "red"
        }
        color = status_colors.get(status.overall_status, "white")
        
        click.echo(f"\n{'='*60}")
        click.secho(f"System Health: {status.overall_status.upper()}", fg=color, bold=True)
        click.echo(f"{'='*60}\n")
        
        click.echo(f"CPU Usage: {status.cpu_usage}%")
        click.echo(f"Memory Usage: {status.memory_usage}%")
        click.echo(f"Disk Usage: {status.disk_usage}%")
        
        if status.issues:
            click.echo(f"\n{click.style('CRITICAL ISSUES:', fg='red', bold=True)}")
            for issue in status.issues:
                click.echo(f"  ❌ {issue}")
        
        if status.warnings:
            click.echo(f"\n{click.style('Warnings:', fg='yellow', bold=True)}")
            for warning in status.warnings:
                click.echo(f"  ⚠️  {warning}")
        
        if status.recommendations:
            click.echo(f"\n{click.style('Recommendations:', fg='cyan', bold=True)}")
            for rec in status.recommendations:
                click.echo(f"  💡 {rec}")
        
        if status.overall_status == "healthy":
            click.secho("\n✓ All systems operational", fg="green")
    
    asyncio.run(_check())


@diagnostics.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for system info')
def sysinfo(output):
    """Display system information."""
    monitor = get_health_monitor()
    info = monitor.get_system_info()
    
    if output:
        Path(output).write_text(json.dumps(info, indent=2))
        click.secho(f"✓ System info exported to {output}", fg="green")
    else:
        click.echo(json.dumps(info, indent=2))


@diagnostics.command()
@click.option('--output', '-o', type=click.Path(), help='Output file for error report')
def errors(output):
    """View error history and diagnostics."""
    troubleshooter = get_troubleshooter()
    diagnostics_data = troubleshooter.get_diagnostics()
    
    click.echo(f"\n{'='*60}")
    click.echo("Error Diagnostics")
    click.echo(f"{'='*60}\n")
    
    click.echo(f"Total Errors: {diagnostics_data['error_count']}")
    click.echo(f"Auto-fixes Applied: {diagnostics_data['fixes_applied']}")
    click.echo(f"Auto-fix Enabled: {diagnostics_data['auto_fix_enabled']}")
    
    if diagnostics_data['errors_by_category']:
        click.echo("\nErrors by Category:")
        for category, count in diagnostics_data['errors_by_category'].items():
            click.echo(f"  {category}: {count}")
    
    if diagnostics_data['errors_by_severity']:
        click.echo("\nErrors by Severity:")
        for severity, count in diagnostics_data['errors_by_severity'].items():
            click.echo(f"  {severity}: {count}")
    
    if output:
        report = troubleshooter.export_report(Path(output))
        click.secho(f"\n✓ Full error report exported to {output}", fg="green")
    elif troubleshooter.error_history:
        click.echo("\nRecent Errors:")
        for error in troubleshooter.error_history[-5:]:
            click.echo(f"\n  [{error.category.value}] {error.severity.name}")
            click.echo(f"  {error.message}")
            if error.fix_applied:
                click.secho(f"  ✓ Auto-fixed: {error.fix_result}", fg="green")
            elif error.suggested_fixes:
                click.echo(f"  Suggested: {', '.join(error.suggested_fixes[:2])}")


@diagnostics.command()
@click.option('--enable/--disable', default=True, help='Enable or disable auto-fix')
def autofix(enable):
    """Configure automatic error correction."""
    troubleshooter = get_troubleshooter()
    troubleshooter.auto_fix_enabled = enable
    
    status = "enabled" if enable else "disabled"
    color = "green" if enable else "yellow"
    click.secho(f"✓ Automatic error correction {status}", fg=color)


@diagnostics.command()
@click.argument('interval', type=int, default=60)
def monitor(interval):
    """Start continuous health monitoring."""
    async def _monitor():
        monitor = get_health_monitor()
        monitor.check_interval = interval
        
        click.echo(f"Starting health monitoring (interval: {interval}s)")
        click.echo("Press Ctrl+C to stop\n")
        
        try:
            await monitor.start_monitoring()
            # Keep running until interrupted
            while monitor.monitoring:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            click.echo("\nStopping monitor...")
            await monitor.stop_monitoring()
    
    try:
        asyncio.run(_monitor())
    except KeyboardInterrupt:
        click.echo("\nMonitoring stopped")


@diagnostics.command()
def fix_common():
    """Attempt to fix common issues automatically."""
    click.echo("Scanning for common issues...")
    
    issues_found = []
    fixes_applied = []
    
    # Check .env file
    if not Path(".env").exists() and Path(".env.example").exists():
        issues_found.append("Missing .env file")
        try:
            Path(".env").write_text(Path(".env.example").read_text())
            fixes_applied.append("✓ Created .env from .env.example")
        except Exception as e:
            fixes_applied.append(f"✗ Failed to create .env: {e}")
    
    # Check Python dependencies
    try:
        import pip
        result = pip.main(["install", "-e", ".[dev]"])
        if result == 0:
            fixes_applied.append("✓ Installed/updated Python dependencies")
    except Exception as e:
        fixes_applied.append(f"⚠️  Could not install dependencies: {e}")
    
    # Display results
    if issues_found:
        click.echo(f"\nIssues found: {len(issues_found)}")
        for issue in issues_found:
            click.echo(f"  • {issue}")
    
    if fixes_applied:
        click.echo(f"\nFixes applied: {len(fixes_applied)}")
        for fix in fixes_applied:
            if "✓" in fix:
                click.secho(f"  {fix}", fg="green")
            elif "✗" in fix:
                click.secho(f"  {fix}", fg="red")
            else:
                click.secho(f"  {fix}", fg="yellow")
    else:
        click.secho("\n✓ No common issues found", fg="green")


if __name__ == '__main__':
    diagnostics()
