#!/usr/bin/env python3
"""
GhostLink AI Bot Framework
Integrated AI agents with hotkey and quick-command root access
"""
from abc import ABC, abstractmethod
import asyncio
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from ai_bots.git_auto_commit import auto_commit


class AccessLevel(Enum):
    """Bot access privilege levels"""
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"
    ROOT = "root"


@dataclass
class Command:
    """Command definition"""
    name: str
    description: str
    handler: Callable
    access_level: AccessLevel = AccessLevel.READ
    hotkey: Optional[str] = None
    aliases: List[str] = field(default_factory=list)
    requires_confirmation: bool = False  # Requires user confirmation


@dataclass
class BotContext:
    """Execution context for bot commands"""
    user_id: str
    session_id: str
    access_level: AccessLevel
    env: Dict[str, Any] = field(default_factory=dict)
    yolo_mode: bool = False  # Auto-approve dangerous commands
    auto_commit: bool = True  # Auto-commit after every action


class AIBot(ABC):
    """Base class for AI bots"""
    
    def __init__(
        self,
        name: str,
        access_level: AccessLevel = AccessLevel.READ
    ):
        self.name = name
        self.access_level = access_level
        self.commands: Dict[str, Command] = {}
        self.hotkeys: Dict[str, Command] = {}
        
    def register_command(
        self,
        name: str,
        handler: Callable,
        description: str = "",
        access_level: Optional[AccessLevel] = None,
        hotkey: Optional[str] = None,
        aliases: Optional[List[str]] = None,
        requires_confirmation: bool = False
    ):
        """Register a command with the bot"""
        cmd = Command(
            name=name,
            description=description,
            handler=handler,
            access_level=access_level or self.access_level,
            hotkey=hotkey,
            aliases=aliases or [],
            requires_confirmation=requires_confirmation
        )
        self.commands[name] = cmd
        
        # Register hotkey
        if hotkey:
            self.hotkeys[hotkey] = cmd
            
        # Register aliases
        for alias in (aliases or []):
            self.commands[alias] = cmd
            
    async def execute(
        self,
        command: str,
        args: List[str],
        context: BotContext
    ) -> Dict[str, Any]:
        """Execute a command"""
        if command not in self.commands:
            return {"error": f"Unknown command: {command}"}
            
        cmd = self.commands[command]
        
        # Check access level
        if not self._check_access(cmd.access_level, context.access_level):
            return {"error": "Insufficient permissions"}
            
        # Check confirmation
        if cmd.requires_confirmation and not context.yolo_mode:
            return {
                "confirm": f"Are you sure you want to run '{cmd.name}'? (y/N)"
            }
            
        try:
            result = await cmd.handler(args, context)
            
            # Auto-commit after successful command execution
            if context.auto_commit:
                action_desc = f"{self.name}.{command}"
                details = f"args: {args}" if args else ""
                auto_commit(action_desc, details)
            
            return {"status": "ok", "result": result}
        except Exception as e:
            return {"error": str(e)}
            
    def _check_access(
        self,
        required: AccessLevel,
        provided: AccessLevel
    ) -> bool:
        """Check if provided access level meets requirements"""
        levels = {
            AccessLevel.READ: 0,
            AccessLevel.WRITE: 1,
            AccessLevel.ADMIN: 2,
            AccessLevel.ROOT: 3
        }
        return levels.get(provided, 0) >= levels.get(required, 0)
        
    @abstractmethod
    async def initialize(self):
        """Initialize bot - override in subclasses"""
        pass


class SystemBot(AIBot):
    """Bot with root system access"""
    
    def __init__(self):
        super().__init__("system", AccessLevel.ROOT)
        
    async def initialize(self):
        """Register system commands"""
        self.register_command(
            "status",
            self.cmd_status,
            "Show system status",
            AccessLevel.READ,
            hotkey="ctrl+shift+s"
        )
        
        self.register_command(
            "restart",
            self.cmd_restart,
            "Restart service",
            AccessLevel.ROOT,
            hotkey="ctrl+shift+r",
            aliases=["reboot"],
            requires_confirmation=True
        )
        
        self.register_command(
            "logs",
            self.cmd_logs,
            "View system logs",
            AccessLevel.ADMIN,
            hotkey="ctrl+shift+l"
        )
        
        # Toggle YOLO mode
        self.register_command(
            "yolo",
            self.cmd_yolo,
            "Toggle YOLO mode (auto-approve dangerous commands)",
            AccessLevel.ADMIN,
            hotkey="ctrl+shift+y",
            aliases=["toggle-yolo"]
        )
        
        # Toggle auto-commit
        self.register_command(
            "autocommit",
            self.cmd_autocommit,
            "Toggle auto-commit mode (commit after every action)",
            AccessLevel.ADMIN,
            aliases=["auto-commit", "ac"]
        )

        # Execute shell command (dangerous; requires confirmation unless YOLO)
        self.register_command(
            "exec",
            self.cmd_exec,
            "Execute shell command",
            AccessLevel.ROOT,
            aliases=["run", "!"],
            requires_confirmation=True
        )
        
    async def cmd_status(self, args: List[str], ctx: BotContext) -> str:
        """Get system status"""
        import psutil
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        return (
            f"CPU: {cpu}% | "
            f"Memory: {mem.percent}% ({mem.used // 1024**2}MB / "
            f"{mem.total // 1024**2}MB)"
        )
        
    async def cmd_restart(self, args: List[str], ctx: BotContext) -> str:
        """Restart service"""
        service = args[0] if args else "ghostlink"
        
        import subprocess
        try:
            # Try Docker Compose first
            result = subprocess.run(
                ["docker-compose", "restart", service],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return f"✓ Restarted {service} (Docker Compose)"
            
            # Try systemctl if Docker fails
            result = subprocess.run(
                ["systemctl", "restart", service],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return f"✓ Restarted {service} (systemd)"
            else:
                return f"Failed to restart {service}: {result.stderr}"
                
        except FileNotFoundError:
            return (
                f"Cannot restart {service}: "
                "Neither docker-compose nor systemctl available"
            )
        except Exception as e:
            return f"Error restarting {service}: {e}"
        
    async def cmd_logs(self, args: List[str], ctx: BotContext) -> str:
        """View logs"""
        lines = int(args[0]) if args else 50
        service = args[1] if len(args) > 1 else "ghostlink"
        
        from pathlib import Path
        import subprocess
        
        try:
            # Try Docker Compose logs first
            result = subprocess.run(
                ["docker-compose", "logs", "--tail", str(lines), service],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and result.stdout:
                return result.stdout
            
            # Try journalctl for systemd services
            result = subprocess.run(
                ["journalctl", "-u", service, "-n", str(lines), "--no-pager"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                return result.stdout or "No logs found"
            
            # Try reading log files directly
            log_paths = [
                Path("/var/log") / f"{service}.log",
                Path("/var/log") / service / "access.log",
                Path.home() / ".local" / "share" / service / "logs" / "app.log"
            ]
            
            for log_path in log_paths:
                if log_path.exists():
                    with open(log_path) as f:
                        all_lines = f.readlines()
                        return ''.join(all_lines[-lines:])
            
            return (
                f"No logs found for {service}. "
                "Tried Docker, systemd, and common log paths."
            )
            
        except Exception as e:
            return f"Error reading logs: {e}"
        
    async def cmd_exec(self, args: List[str], ctx: BotContext) -> str:
        """Execute shell command"""
        if not args:
            return "Usage: exec <command>"
        import subprocess
        cmd = " ".join(args)
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout or result.stderr or "Command executed"
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error: {e}"
            
    async def cmd_yolo(self, args: List[str], ctx: BotContext) -> str:
        """Toggle YOLO mode"""
        ctx.yolo_mode = not ctx.yolo_mode
        status = "ENABLED" if ctx.yolo_mode else "DISABLED"
        action = (
            "be auto-approved"
            if ctx.yolo_mode
            else "require confirmation"
        )
        return f"YOLO mode {status}: Dangerous commands will {action}"
        
    async def cmd_autocommit(self, args: List[str], ctx: BotContext) -> str:
        """Toggle auto-commit mode"""
        ctx.auto_commit = not ctx.auto_commit
        status = "ENABLED" if ctx.auto_commit else "DISABLED"
        action = (
            "commit after every action"
            if ctx.auto_commit
            else "not auto-commit"
        )
        return f"Auto-commit {status}: Will {action}"


class MetricsBot(AIBot):
    """Bot for metrics and monitoring"""
    
    def __init__(self):
        super().__init__("metrics", AccessLevel.READ)
        
    async def initialize(self):
        """Register metrics commands"""
        self.register_command(
            "get",
            self.cmd_get,
            "Get metrics",
            AccessLevel.READ,
            hotkey="ctrl+m"
        )
        
        self.register_command(
            "alert",
            self.cmd_alert,
            "Create alert rule",
            AccessLevel.ADMIN,
            aliases=["watch"]
        )
        
    async def cmd_get(self, args: List[str], ctx: BotContext) -> str:
        """Get metrics from controller"""
        import httpx
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "http://127.0.0.1:9108/metrics",
                    timeout=2.0
                )
                return resp.text[:500] + "..."
        except Exception as e:
            return f"Error fetching metrics: {e}"
            
    async def cmd_alert(self, args: List[str], ctx: BotContext) -> str:
        """Create alert rule"""
        if len(args) < 2:
            return "Usage: alert <metric> <threshold>"
        metric, threshold = args[0], args[1]
        return f"Alert created: {metric} > {threshold}"


class CommandRouter:
    """Routes commands to appropriate bots"""
    
    def __init__(self):
        self.bots: Dict[str, AIBot] = {}
        self.hotkey_map: Dict[str, tuple[AIBot, Command]] = {}
        
    async def register_bot(self, bot: AIBot):
        """Register a bot"""
        await bot.initialize()
        self.bots[bot.name] = bot
        
        # Map hotkeys
        for hotkey, cmd in bot.hotkeys.items():
            self.hotkey_map[hotkey] = (bot, cmd)
            
    async def route(
        self,
        input_str: str,
        context: BotContext
    ) -> Dict[str, Any]:
        """Route command to appropriate bot"""
        parts = input_str.strip().split()
        if not parts:
            return {"error": "Empty command"}
            
        # Explicit bot routing: /botname command args
        if parts[0].startswith("/"):
            bot_name = parts[0][1:]
            if bot_name not in self.bots:
                return {"error": f"Unknown bot: {bot_name}"}
            command = parts[1] if len(parts) > 1 else ""
            args = parts[2:]
            return await self.bots[bot_name].execute(command, args, context)

        # Mention style: @botname command args
        if parts[0].startswith("@"):
            bot_name = parts[0][1:]
            if bot_name not in self.bots:
                return {"error": f"Unknown bot: {bot_name}"}
            command = parts[1] if len(parts) > 1 else ""
            args = parts[2:]
            return await self.bots[bot_name].execute(command, args, context)

        # Bang quick command: !command args (strip leading '!')
        if parts[0].startswith("!"):
            command = parts[0][1:]
            args = parts[1:]
            for bot in self.bots.values():
                if command in bot.commands:
                    return await bot.execute(command, args, context)
            return {"error": f"Unknown command: {command}"}
            
        # Direct command (try all bots)
        command = parts[0]
        args = parts[1:]
        
        for bot in self.bots.values():
            if command in bot.commands:
                return await bot.execute(command, args, context)
                
        return {"error": f"Unknown command: {command}"}
        
    async def handle_hotkey(
        self,
        hotkey: str,
        context: BotContext
    ) -> Dict[str, Any]:
        """Handle hotkey press"""
        if hotkey not in self.hotkey_map:
            return {"error": f"Unknown hotkey: {hotkey}"}
            
        bot, cmd = self.hotkey_map[hotkey]
        return await bot.execute(cmd.name, [], context)


async def main():
    """CLI interface"""
    router = CommandRouter()
    
    # Register bots
    await router.register_bot(SystemBot())
    await router.register_bot(MetricsBot())
    
    # Create root context
    context = BotContext(
        user_id="admin",
        session_id="local",
        access_level=AccessLevel.ROOT
    )
    
    print("🤖 GhostLink AI Bot Framework")
    print("=" * 50)
    print("Commands:")
    print("  /system status       - System status")
    print("  /system restart      - Restart service")
    print("  /system exec <cmd>   - Execute command")
    print("  /metrics get         - Get metrics")
    print("  status               - Quick status (any bot)")
    print("")
    print("Hotkeys:")
    print("  ctrl+shift+s  - System status")
    print("  ctrl+shift+r  - Restart")
    print("  ctrl+shift+l  - View logs")
    print("  ctrl+m        - Get metrics")
    print("=" * 50)
    print("")
    
    while True:
        try:
            cmd_input = input("bot> ").strip()
            if not cmd_input:
                continue
            if cmd_input in ["exit", "quit"]:
                break
                
            result = await router.route(cmd_input, context)
            
            if "error" in result:
                print(f"❌ {result['error']}")
            else:
                print(f"✓ {result.get('result', 'OK')}")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
