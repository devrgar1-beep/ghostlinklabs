#!/usr/bin/env python3
"""
CLI interface for GhostLink AI bots
Interactive terminal with rich formatting
"""
import asyncio
from pathlib import Path

from ai_bots.ai_bus import ai_bus
from ai_bots.core import (
    AccessLevel,
    BotContext,
    CommandRouter,
    MetricsBot,
    SystemBot,
)
from ai_bots.hotkeys import HotkeyHandler
from ai_bots.parser import CommandParser
from ai_bots.registry import BotRegistry


class BotCLI:
    """Interactive CLI for bot management"""
    
    def __init__(self):
        self.router = CommandRouter()
        self.registry = BotRegistry()
        self.parser = CommandParser()
        self.hotkey_handler = HotkeyHandler()
        self.context = BotContext(
            user_id="admin",
            session_id="local",
            access_level=AccessLevel.ROOT,
            yolo_mode=True  # Auto-approve dangerous commands
        )
        self.running = False
        
    async def initialize(self):
        """Initialize CLI"""
        # Register built-in bots
        system_bot = SystemBot()
        metrics_bot = MetricsBot()
        
        await self.router.register_bot(system_bot)
        await self.router.register_bot(metrics_bot)
        
        self.registry.register_bot(system_bot)
        self.registry.register_bot(metrics_bot)
        
        # Load plugins
        plugin_dir = Path(__file__).parent / "plugins"
        if plugin_dir.exists():
            self.registry.add_plugin_path(plugin_dir)
            await self.registry.discover_bots()
            
        # Register discovered bots with router and AI bus
        for bot in self.registry.bots.values():
            if bot.name not in ["system", "metrics"]:
                await self.router.register_bot(bot)
                ai_bus.register_agent(bot)
        
        # Register built-in bots with AI bus
        ai_bus.register_agent(system_bot)
        ai_bus.register_agent(metrics_bot)        # Setup hotkeys
        for hotkey, (bot, cmd) in self.router.hotkey_map.items():
            async def callback(b=bot, c=cmd):
                result = await b.execute(c.name, [], self.context)
                print(f"\n[Hotkey] {result.get('result', result)}")
                print("bot> ", end="", flush=True)
            self.hotkey_handler.register(hotkey, callback)
            
    def print_banner(self):
        """Print welcome banner"""
        yolo_status = "ENABLED" if self.context.yolo_mode else "DISABLED"
        ac_status = "ENABLED" if self.context.auto_commit else "DISABLED"
        print()
        print("=" * 60)
        print("🤖 GhostLink AI Bot Framework")
        print(f"YOLO Mode: {yolo_status}")
        print(f"Auto-Commit: {ac_status}")
        print("=" * 60)
        print()
        
    def print_help(self):
        """Print help text"""
        print("Available Bots:")
        for name in self.registry.list_bots():
            bot = self.registry.get_bot(name)
            if bot:
                print(f"  {name:15} - {len(bot.commands)} commands")
                
        print()
        print("Command Formats:")
        print("  /bot command args    - Route to specific bot")
        print("  !command args        - Quick command (any bot)")
        print("  @bot command args    - Mention style")
        print("  command args         - Direct (any bot)")
        print()
        print("AI Orchestration:")
        print("  ai ask <prompt>      - Ask AI (Groq)")
        print("  ai oracle <question> - Ask Copilot oracle")
        print("  ai providers         - List AI providers")
        print()
        print("Special Commands:")
        print("  help                 - Show this help")
        print("  list                 - List all commands")
        print("  hotkeys              - List all hotkeys")
        print("  exit, quit           - Exit CLI")
        print()
        
    def print_commands(self):
        """Print all commands"""
        print("All Commands:")
        for bot in self.registry.bots.values():
            print(f"\n  {bot.name}:")
            for cmd_name, cmd in bot.commands.items():
                if cmd_name in cmd.aliases:
                    continue
                aliases = (
                    f" [{', '.join(cmd.aliases)}]"
                    if cmd.aliases else ""
                )
                print(f"    {cmd_name:15}{aliases:20} - {cmd.description}")
                
    def print_hotkeys(self):
        """Print all hotkeys"""
        print("Hotkeys:")
        hotkeys = self.registry.get_all_hotkeys()
        if not hotkeys:
            print("  No hotkeys registered")
            return
        for hotkey, location in hotkeys.items():
            print(f"  {hotkey:20} -> {location}")
            
    async def run(self):
        """Run CLI loop"""
        await self.initialize()
        self.print_banner()
        self.print_help()
        
        # Start hotkey handler
        try:
            self.hotkey_handler.start()
            print("✓ Hotkey handler started")
        except RuntimeError as e:
            print(f"⚠ Hotkey handler disabled: {e}")
            
        print()
        self.running = True
        
        while self.running:
            try:
                user_input = input("bot> ").strip()
                if not user_input:
                    continue
                    
                # Special commands
                if user_input in ["exit", "quit"]:
                    break
                elif user_input == "help":
                    self.print_help()
                    continue
                elif user_input == "list":
                    self.print_commands()
                    continue
                elif user_input == "hotkeys":
                    self.print_hotkeys()
                    continue
                    
                # Parse and route command
                result = await self.router.route(user_input, self.context)
                
                if "confirm" in result:
                    # Handle confirmation
                    confirm_msg = result["confirm"]
                    print(f"⚠️  {confirm_msg}")
                    try:
                        response = input("Confirm (y/N): ").strip().lower()
                        if response in ["y", "yes"]:
                            # Re-run the command with yolo temporarily enabled
                            original_yolo = self.context.yolo_mode
                            self.context.yolo_mode = True
                            result = await self.router.route(
                                user_input, self.context
                            )
                            self.context.yolo_mode = original_yolo
                        else:
                            result = {"result": "Command cancelled"}
                    except (KeyboardInterrupt, EOFError):
                        result = {"result": "Command cancelled"}
                
                if "error" in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"✓ {result.get('result', 'OK')}")
                    
            except KeyboardInterrupt:
                print("\nUse 'exit' or 'quit' to exit")
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")
                
        # Cleanup
        self.hotkey_handler.stop()
        print("\nGoodbye!")


async def main():
    """Main entry point"""
    cli = BotCLI()
    await cli.run()


if __name__ == "__main__":
    asyncio.run(main())
