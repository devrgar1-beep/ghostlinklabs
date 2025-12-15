import asyncio

from ai_bots.plugins.calculator import CalculatorBot
from ai_bots.core import BotContext, AccessLevel


def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


def test_safe_eval_basic():
    bot = CalculatorBot()
    run_async(bot.initialize())

    ctx = BotContext(user_id="test", session_id="demo", access_level=AccessLevel.ROOT)

    res = run_async(bot.cmd_eval(["2", "+", "3", "*", "4"], ctx))
    assert "2 + 3 * 4 = 14" in res


def test_safe_eval_rejects_malicious():
    bot = CalculatorBot()
    run_async(bot.initialize())

    ctx = BotContext(user_id="test", session_id="demo", access_level=AccessLevel.ROOT)

    res = run_async(bot.cmd_eval(["__import__('os').system('echo hi')"], ctx))
    assert res.startswith("Error:"), "Malicious expression should be rejected"
