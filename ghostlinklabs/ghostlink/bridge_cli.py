"""Link Bridge CLI - Universal System Bridge integration commands."""

import json
import sys
from pathlib import Path

import click

# Import bridge integration
try:
    import sys
    from pathlib import Path
    # Add the src directory to path (bridge_cli.py is in ghostlink/, src is at parent level)
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))
    from link_bridge_integration import LinkBridgeIntegration
except ImportError as e:
    print(f"Warning: Bridge integration not available: {e}")
    LinkBridgeIntegration = None


@click.group()
def bridge():
    """Universal System Bridge integration commands."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        sys.exit(1)


@bridge.command()
def start():
    """Start the Universal System Bridge."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    success = integration.start_bridge()

    if success:
        click.echo("✅ Universal System Bridge started successfully")
    else:
        click.echo("❌ Failed to start Universal System Bridge")
        sys.exit(1)


@bridge.command()
def stop():
    """Stop the Universal System Bridge."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    success = integration.stop_bridge()

    if success:
        click.echo("✅ Universal System Bridge stopped successfully")
    else:
        click.echo("❌ Failed to stop Universal System Bridge")
        sys.exit(1)


@bridge.command()
def status():
    """Get Universal System Bridge status."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    status = integration.get_bridge_status()

    click.echo("🔗 Universal System Bridge Status:")
    click.echo(json.dumps(status, indent=2))


@bridge.command()
def overview():
    """Get comprehensive system overview."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    overview = integration.get_system_overview()

    click.echo("🌐 System Overview:")
    click.echo(json.dumps(overview, indent=2))


@bridge.command()
def health():
    """Perform comprehensive system health check."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    health = integration.perform_system_health_check()

    click.echo("🏥 System Health Check:")
    click.echo(json.dumps(health, indent=2))


@bridge.command()
@click.argument("component_id")
def component(component_id):
    """Get detailed information about a specific component."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    info = integration.get_component_details(component_id)

    click.echo(f"📋 Component Information for {component_id}:")
    click.echo(json.dumps(info, indent=2))


@bridge.command()
@click.argument("action")
@click.option("--payload", default="{}", help="JSON payload for the action")
def execute(action, payload):
    """Execute a bridge action."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()

    try:
        payload_dict = json.loads(payload)
    except json.JSONDecodeError:
        click.echo("❌ Invalid JSON payload")
        sys.exit(1)

    result = integration.send_bridge_command(action, payload_dict)

    click.echo("⚡ Command Execution Result:")
    click.echo(json.dumps(result, indent=2))


@bridge.command()
@click.argument("action")
@click.argument("component")
@click.option("--description", default="", help="Task description")
def task(action, component, description):
    """Create a Link task for a bridge action."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    success = integration.create_link_task_for_bridge_action(action, component, description)

    if success:
        click.echo("✅ Link task created successfully")
    else:
        click.echo("❌ Failed to create Link task")
        sys.exit(1)


@bridge.command()
@click.argument("command")
@click.option("--component-type", default="system", help="Component type for command routing")
def cmd(command, component_type):
    """Execute a system command through the bridge."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    result = integration.execute_system_command_via_bridge(command, component_type)

    click.echo("⚡ Command Execution Result:")
    click.echo(json.dumps(result, indent=2))


@bridge.command()
def components():
    """List all registered bridge components."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    overview = integration.get_system_overview()

    click.echo("🔧 Registered Components:")
    for comp_type, components in overview.get("system_components", {}).items():
        click.echo(f"\n{comp_type.upper()}:")
        for comp in components:
            status_emoji = "🟢" if comp.get("status") == "online" else "🔴"
            click.echo(f"  {status_emoji} {comp['id']}")


@bridge.command()
def integrations():
    """Show active system integrations."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()
    overview = integration.get_system_overview()

    click.echo("🔗 Active System Integrations:")
    for integration_name in overview.get("active_integrations", []):
        click.echo(f"  ✅ {integration_name}")


@bridge.command()
def monitor():
    """Start real-time bridge monitoring."""
    if LinkBridgeIntegration is None:
        click.echo("❌ Bridge integration not available")
        return
    integration = LinkBridgeIntegration()

    click.echo("📊 Starting Bridge Monitor (Ctrl+C to stop)...")
    click.echo("Press Ctrl+C to stop monitoring")

    try:
        while True:
            status = integration.get_bridge_status()
            health = integration.perform_system_health_check()

            # Clear screen and show status
            click.clear()
            click.echo("🔗 Universal System Bridge Monitor")
            click.echo("=" * 50)
            click.echo(f"Bridge Status: {status.get('bridge_status', 'unknown')}")
            click.echo(f"Components: {status.get('total_components', 0)}")
            click.echo(".1f")
            click.echo(f"Health Score: {health.get('health_summary', {}).get('overall_score', 0):.1f}")
            click.echo("")

            # Show component status
            click.echo("Component Status:")
            for comp_type, count in status.get("component_types", {}).items():
                click.echo(f"  {comp_type}: {count}")

            click.echo("")
            click.echo("Recent Recommendations:")
            recommendations = health.get("health_summary", {}).get("recommendations", [])[:3]
            for rec in recommendations:
                click.echo(f"  • {rec}")

            click.echo("")
            click.echo("Press Ctrl+C to stop...")

            import time
            time.sleep(5)

    except KeyboardInterrupt:
        click.echo("\n✅ Monitoring stopped")
