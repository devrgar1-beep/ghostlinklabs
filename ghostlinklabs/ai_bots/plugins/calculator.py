#!/usr/bin/env python3
"""
Example custom bot plugin
Demonstrates how to create custom bots
"""
import asyncio
from typing import List

from ai_bots.core import AIBot, AccessLevel, BotContext


class CalculatorBot(AIBot):
    """Simple calculator bot"""
    
    def __init__(self):
        super().__init__("calc", AccessLevel.READ)
        
    async def initialize(self):
        """Register calculator commands"""
        self.register_command(
            "add",
            self.cmd_add,
            "Add numbers: add 1 2 3",
            AccessLevel.READ,
            aliases=["sum", "+"]
        )
        
        self.register_command(
            "multiply",
            self.cmd_multiply,
            "Multiply numbers: multiply 2 3 4",
            AccessLevel.READ,
            aliases=["mul", "*"]
        )
        
        self.register_command(
            "eval",
            self.cmd_eval,
            "Evaluate expression: eval 2 + 3 * 4",
            AccessLevel.READ,
            aliases=["="]
        )
        
    async def cmd_add(self, args: List[str], ctx: BotContext) -> str:
        """Add numbers"""
        try:
            numbers = [float(x) for x in args]
            result = sum(numbers)
            return f"{' + '.join(args)} = {result}"
        except ValueError:
            return "Error: Invalid numbers"
            
    async def cmd_multiply(
        self,
        args: List[str],
        ctx: BotContext
    ) -> str:
        """Multiply numbers"""
        try:
            numbers = [float(x) for x in args]
            result = 1.0
            for num in numbers:
                result *= num
            return f"{' × '.join(args)} = {result}"
        except ValueError:
            return "Error: Invalid numbers"
            
    async def cmd_eval(self, args: List[str], ctx: BotContext) -> str:
        """Evaluate expression"""
        try:
            expr = " ".join(args)
            # Safe eval with limited scope
            result = eval(  # noqa: S307
                expr,
                {"__builtins__": {}},
                {}
            )
            return f"{expr} = {result}"
        except Exception as e:
            return f"Error: {e}"


if __name__ == "__main__":
    async def test():
        bot = CalculatorBot()
        await bot.initialize()
        
        ctx = BotContext(
            user_id="test",
            session_id="demo",
            access_level=AccessLevel.ROOT
        )
        
        print("Calculator Bot Demo")
        print("=" * 50)
        
        tests = [
            ("add", ["1", "2", "3"]),
            ("multiply", ["2", "3", "4"]),
            ("eval", ["2", "+", "3", "*", "4"]),
        ]
        
        for cmd, args in tests:
            result = await bot.execute(cmd, args, ctx)
            print(f"{cmd} {' '.join(args)}")
            print(f"  -> {result.get('result', result.get('error'))}")
            
    asyncio.run(test())
