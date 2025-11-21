"""Command Line Interface for GhostLink"""

import asyncio
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.ai_providers import AIProviderManager
from ..core.api_integration import FreeAPIIntegration
from ..core.autonomous_agents import AgentOrchestrator
from ..utils.config import config
from ..utils.logging import setup_logging

console = Console()
ai_manager = AIProviderManager()
api_integration = FreeAPIIntegration()
agent_orchestrator = AgentOrchestrator()


@click.group()
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def cli(verbose):
    """GhostLink AI Ecosystem CLI"""
    if verbose:
        setup_logging("DEBUG")
    else:
        setup_logging()


@cli.command()
@click.argument("question")
@click.option("--provider", default=None, help="AI provider to use")
@click.option("--temperature", type=float, default=None, help="AI temperature")
def ask(question: str, provider: Optional[str], temperature: Optional[float]):
    """Ask a question to AI"""
    try:
        if provider:
            config.set("ai.default_provider", provider)
        if temperature is not None:
            config.set("ai.temperature", temperature)

        response = asyncio.run(ai_manager.ask(question))
        console.print(Panel(response, title="AI Response", border_style="green"))
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
@click.argument("query")
@click.option("--question", "-q", help="Question to ask about the API data")
def api(query: str, question: Optional[str]):
    """Query free APIs"""
    try:
        data = asyncio.run(api_integration.query_api(query))

        if question:
            analysis = asyncio.run(api_integration.query_ai_with_api_data(question, data))
            console.print(Panel(analysis, title="AI Analysis", border_style="blue"))
        else:
            console.print(Panel(str(data), title="API Data", border_style="yellow"))
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
@click.argument("task")
@click.option("--agent-role", default="analyst", help="Agent role")
def agent(task: str, agent_role: str):
    """Run autonomous agent"""
    try:
        result = asyncio.run(agent_orchestrator.run_agent_task(task, agent_role))
        console.print(Panel(result, title="Agent Result", border_style="magenta"))
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@cli.command()
def providers():
    """List available AI providers"""
    table = Table(title="AI Providers")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Model", style="yellow")

    for provider_name, provider in ai_manager.providers.items():
        status = "✅ Available" if provider else "❌ Unavailable"
        model = getattr(provider, "model", "N/A") if provider else "N/A"
        table.add_row(provider_name, status, model)

    console.print(table)


@cli.command()
def apis():
    """List available free APIs"""
    apis = api_integration.get_available_apis()

    table = Table(title="Free APIs")
    table.add_column("API", style="cyan")
    table.add_column("Description", style="white")

    for api_name, description in apis.items():
        table.add_row(api_name, description)

    console.print(table)


@cli.command()
def status():
    """Show system status"""
    console.print(
        Panel.fit(
            "[green]GhostLink AI Ecosystem[/green]\n"
            f"Version: {config.get('system.version')}\n"
            f"Debug: {config.get('system.debug')}\n"
            f"Default Provider: {config.get('ai.default_provider')}\n"
            f"Log Level: {config.get('logging.level')}",
            title="System Status",
            border_style="blue",
        )
    )


@cli.command()
def interfaces():
    """List available user interfaces"""
    console.print("[yellow]Available UIs:[/yellow]")
    console.print("  --terminal-90s    Launch retro 90s terminal")
    console.print("  --web            Launch web interface (not implemented)")


if __name__ == "__main__":
    cli()
