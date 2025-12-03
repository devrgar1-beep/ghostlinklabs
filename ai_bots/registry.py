#!/usr/bin/env python3
"""
Bot registry and plugin system
Dynamic bot loading and management
"""
import asyncio
import importlib.util
import inspect
from pathlib import Path
from typing import Dict, List, Optional

from ai_bots.core import AIBot


class BotRegistry:
    """Registry for managing bot plugins"""
    
    def __init__(self):
        self.bots: Dict[str, AIBot] = {}
        self.plugin_paths: List[Path] = []
        
    def add_plugin_path(self, path: Path):
        """Add path to search for bot plugins"""
        if path.exists() and path.is_dir():
            self.plugin_paths.append(path)
            
    async def discover_bots(self):
        """Discover and load bots from plugin paths"""
        for plugin_path in self.plugin_paths:
            await self._scan_directory(plugin_path)
            
    async def _scan_directory(self, path: Path):
        """Scan directory for bot modules"""
        for file_path in path.glob("*.py"):
            if file_path.stem.startswith("_"):
                continue
            await self._load_module(file_path)
            
    async def _load_module(self, file_path: Path):
        """Load bot from Python module"""
        try:
            # Load module
            spec = importlib.util.spec_from_file_location(
                file_path.stem,
                file_path
            )
            if not spec or not spec.loader:
                return
                
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Find AIBot subclasses
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, AIBot)
                    and obj is not AIBot
                    and not inspect.isabstract(obj)
                ):
                    # Instantiate and register
                    bot = obj()
                    await bot.initialize()
                    self.bots[bot.name] = bot
                    
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    def register_bot(self, bot: AIBot):
        """Manually register a bot"""
        self.bots[bot.name] = bot
        
    def unregister_bot(self, name: str) -> Optional[AIBot]:
        """Unregister and return bot"""
        return self.bots.pop(name, None)
        
    def get_bot(self, name: str) -> Optional[AIBot]:
        """Get bot by name"""
        return self.bots.get(name)
        
    def list_bots(self) -> List[str]:
        """List all registered bot names"""
        return list(self.bots.keys())
        
    def get_all_commands(self) -> Dict[str, str]:
        """Get all commands from all bots"""
        commands = {}
        for bot in self.bots.values():
            for cmd_name, cmd in bot.commands.items():
                commands[cmd_name] = f"{bot.name}.{cmd_name}"
        return commands
        
    def get_all_hotkeys(self) -> Dict[str, str]:
        """Get all hotkeys from all bots"""
        hotkeys = {}
        for bot in self.bots.values():
            for hotkey, cmd in bot.hotkeys.items():
                hotkeys[hotkey] = f"{bot.name}.{cmd.name}"
        return hotkeys


async def demo():
    """Demo bot registry"""
    registry = BotRegistry()
    
    # Add plugin path
    plugin_dir = Path(__file__).parent / "plugins"
    registry.add_plugin_path(plugin_dir)
    
    # Discover bots
    await registry.discover_bots()
    
    print("Bot Registry Demo")
    print("=" * 50)
    print(f"\nRegistered bots: {registry.list_bots()}")
    print("\nCommands:")
    for cmd, location in registry.get_all_commands().items():
        print(f"  {cmd:20} -> {location}")
    print("\nHotkeys:")
    for hotkey, location in registry.get_all_hotkeys().items():
        print(f"  {hotkey:20} -> {location}")


if __name__ == "__main__":
    asyncio.run(demo())
