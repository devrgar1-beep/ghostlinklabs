"""Link CLI - Command-line interface for your AI brain.

Example usage:
    python -m ghostlink.link_cli start
    python -m ghostlink.link_cli task add "Fix bug in core module"
    python -m ghostlink.link_cli status
    python -m ghostlink.link_cli stop
"""

import asyncio
from typing import Optional

import click

try:
    # Attempt to import bios bridge from package layout
    from .bios_bridge import (
        BIOSOperation,
        get_bios_status,
        initialize_bios_bridge,
        supergrok_bios,
    )
except Exception:
    try:
        # Fallback: import from the bridge subpackage if available
        from .bridge.bios_bridge import (
            BIOSOperation,
            get_bios_status,
            initialize_bios_bridge,
            supergrok_bios,
        )
    except Exception:
        # Stubs if BIOS bridge is not available - keep CLI usable
        BIOSOperation = None

        def get_bios_status(*args, **kwargs):
            return None

        def initialize_bios_bridge(*args, **kwargs):
            return False

        supergrok_bios = None
from .diagnostics_cli import diagnostics
from .git_cli import git
from .hardware_utils import bind_to_disk, bind_to_nic, is_admin, is_virtual_machine
from .link import TaskPriority, get_link


@click.group()
def cli():
    """Link - Your AI orchestration brain."""


# Add subcommand groups
cli.add_command(diagnostics)
cli.add_command(git)


@cli.command()
@click.option("--name", default="Link", help="Link's display name")
@click.option(
    "--hardware/--no-hardware",
    default=False,
    help="Bind Link to physical hardware and enable hardware mode",
)
@click.option("--bind-nic", default=None, help="MAC address of NIC to bind to (physical)")
@click.option("--bind-disk", default=None, help="Disk DeviceID to bind to (physical)")
@click.option(
    "--confirm-hardware",
    is_flag=True,
    default=False,
    help="Requires explicit confirmation for hardware binding",
)
def start(name: str, hardware: bool, bind_nic: str, bind_disk: str, confirm_hardware: bool):
    """Start Link's autonomous operation."""
    link = get_link()
    link.name = name
    # Apply hardware binding if requested
    if hardware:
        if is_virtual_machine():
            click.echo(
                "⚠️ VM detected. Hardware binding is not supported in virtualized environments. Aborting."
            )
            return
        if not is_admin():
            click.echo(
                "⚠️ Administrator privileges required to bind to hardware. Please run as elevated user."
            )
            return
        if not confirm_hardware:
            click.echo(
                "⚠️ Hardware binding requires explicit confirmation via --confirm-hardware. Aborting."
            )
            return
        bound_ok = True
        if bind_nic:
            if not bind_to_nic(bind_nic):
                bound_ok = False
        if bind_disk:
            if not bind_to_disk(bind_disk):
                bound_ok = False
        if not bound_ok:
            click.echo("⚠️ Failed to bind to requested hardware devices. Aborting.")
            return

    async def run():
        await link.start(hardware_mode=hardware, bound_devices={"nic": bind_nic, "disk": bind_disk})
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
def bios():
    """BIOS bridge operations"""


@bios.command("info")
def bios_info():
    """Show BIOS bridge status and key settings"""
    if not initialize_bios_bridge():
        click.echo("⚠️ BIOS bridge not available or failed to initialize")
        return
    status = get_bios_status()
    click.echo(f"{status}")


@bios.command("read")
@click.argument("setting_name")
def bios_read(setting_name: str):
    """Read a BIOS setting"""
    if not initialize_bios_bridge():
        click.echo("⚠️ BIOS bridge not available")
        return
    bridge = supergrok_bios.bridge
    result = bridge.perform_bios_operation(BIOSOperation.READ_SETTING, setting_name=setting_name)
    click.echo(f"{result}")


@bios.command("write")
@click.argument("setting_name")
@click.option("--value", required=True, help="Value to set")
@click.option("--simulate/--no-simulate", default=True, help="Run in simulation (dry-run) mode")
@click.option("--confirm", is_flag=True, default=False, help="Confirm to apply changes")
@click.option(
    "--hardware",
    is_flag=True,
    default=False,
    help="Indicates you want to perform the operation on physical hardware",
)
def bios_write(setting_name: str, value: str, simulate: bool, confirm: bool, hardware: bool):
    """Write a BIOS setting (requires explicit confirm to apply)"""
    if not initialize_bios_bridge():
        click.echo("⚠️ BIOS bridge not available")
        return
    if hardware:
        if is_virtual_machine():
            click.echo(
                "⚠️ VM detected. Hardware binding is not supported in virtualized environments. Aborting."
            )
            return
        if not is_admin():
            click.echo(
                "⚠️ Administrator privileges required to bind to hardware. Please run as elevated user."
            )
            return
    bridge = supergrok_bios.bridge
    result = bridge.perform_bios_operation(
        BIOSOperation.WRITE_SETTING,
        setting_name=setting_name,
        value=value,
        simulate=simulate,
        confirm=confirm,
        hardware_bind=hardware,
    )
    click.echo(f"{result}")


@bios.command("firmware")
@click.option("--simulate/--no-simulate", default=True)
@click.option("--confirm", is_flag=True, default=False)
@click.option(
    "--hardware",
    is_flag=True,
    default=False,
    help="Indicates you want to run firmware tasks on a physical device",
)
def bios_firmware(simulate: bool, confirm: bool, hardware: bool):
    """Discover vendor firmware tools and prepare (simulation by default)"""
    if not initialize_bios_bridge():
        click.echo("⚠️ BIOS bridge not available")
        return
    if hardware:
        if is_virtual_machine():
            click.echo(
                "⚠️ VM detected. Hardware binding is not supported in virtualized environments. Aborting."
            )
            return
        if not is_admin():
            click.echo(
                "⚠️ Administrator privileges required to bind to hardware. Please run as elevated user."
            )
            return
    bridge = supergrok_bios.bridge
    result = bridge.perform_bios_operation(
        BIOSOperation.UPDATE_FIRMWARE, simulate=simulate, confirm=confirm, hardware_bind=hardware
    )
    click.echo(f"{result}")


@cli.group()
def task():
    """Task management commands."""


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


@cli.group()
def hardware():
    """Hardware and device operations (read-only listing)."""


@hardware.command("nics")
def hardware_nics():
    """List physical network adapters."""
    from .hardware_utils import list_physical_nics

    nics = list_physical_nics()
    if not nics:
        click.echo("No physical NICs found or insufficient permission")
        return
    click.echo("\n🔗 Physical NICs:")
    for nic in nics:
        click.echo(f" - {nic.get('name')} ({nic.get('mac')}) - {nic.get('status')}")


@hardware.command("disks")
def hardware_disks():
    """List physical disks."""
    from .hardware_utils import list_physical_disks

    disks = list_physical_disks()
    if not disks:
        click.echo("No physical disks found or insufficient permission")
        return
    click.echo("\n💾 Physical Disks:")
    for d in disks:
        click.echo(f" - {d.get('device')} {d.get('model')} size={d.get('size')}")


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
def reset():
    """Reset Link's memory."""
    click.echo("⚠️  Resetting Link's memory...")
    link = get_link()
    link.memory = type(link.memory)()  # Fresh memory
    link.memory.save(link.memory_path)
    click.echo("✅ Memory reset complete.")


if __name__ == "__main__":
    cli()
