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

            # Safely evaluate arithmetic expressions using AST
            import ast

            allowed_nodes = (
                ast.Expression,
                ast.BinOp,
                ast.UnaryOp,
                ast.Num,
                ast.Constant,
                ast.Add,
                ast.Sub,
                ast.Mult,
                ast.Div,
                ast.Mod,
                ast.Pow,
                ast.USub,
                ast.UAdd,
                ast.FloorDiv,
                ast.LShift,
                ast.RShift,
                ast.BitOr,
                ast.BitAnd,
                ast.BitXor,
                ast.UnaryOp,
                ast.Call,
                ast.Name,
                ast.Load,
            )

            def _safe_eval(node):
                # Allow numeric constants
                if isinstance(node, ast.Expression):
                    return _safe_eval(node.body)

                if isinstance(node, ast.Constant):
                    if isinstance(node.value, (int, float)):
                        return node.value
                    raise ValueError("Only numeric constants are allowed")

                if isinstance(node, ast.BinOp):
                    left = _safe_eval(node.left)
                    right = _safe_eval(node.right)
                    op = node.op
                    if isinstance(op, ast.Add):
                        return left + right
                    if isinstance(op, ast.Sub):
                        return left - right
                    if isinstance(op, ast.Mult):
                        return left * right
                    if isinstance(op, ast.Div):
                        return left / right
                    if isinstance(op, ast.Mod):
                        return left % right
                    if isinstance(op, ast.Pow):
                        return left ** right
                    if isinstance(op, ast.FloorDiv):
                        return left // right
                    raise ValueError("Unsupported binary operator")

                if isinstance(node, ast.UnaryOp):
                    operand = _safe_eval(node.operand)
                    if isinstance(node.op, ast.UAdd):
                        return +operand
                    if isinstance(node.op, ast.USub):
                        return -operand
                    raise ValueError("Unsupported unary operator")

                # Disallow anything else (names, calls, attributes...)
                raise ValueError("Unsupported expression")

            parsed = ast.parse(expr, mode="eval")
            # Walk AST to ensure nodes are only allowed types
            for n in ast.walk(parsed):
                if not isinstance(n, allowed_nodes):
                    raise ValueError("Disallowed expression component")

            result = _safe_eval(parsed)
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
