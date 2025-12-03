#!/usr/bin/env python3
"""
Quick command parser for GhostLink AI bots
Parses text commands with various formats
"""
from dataclasses import dataclass
import re
from typing import List, Optional


@dataclass
class ParsedCommand:
    """Parsed command structure"""
    bot: Optional[str]
    command: str
    args: List[str]
    raw: str


class CommandParser:
    """Parse quick commands in various formats"""
    
    # Command formats:
    # /bot command args     - Explicit bot routing
    # !command args         - Quick command (any bot)
    # @bot command args     - Mention-style
    # command args          - Direct (any bot)
    
    def __init__(self):
        self.patterns = [
            # /bot command args
            (
                r"^/([a-z]+)\s+([a-z]+)(?:\s+(.*))?$",
                lambda m: ParsedCommand(
                    bot=m.group(1),
                    command=m.group(2),
                    args=self._split_args(m.group(3) or ""),
                    raw=m.group(0)
                )
            ),
            # !command args
            (
                r"^!([a-z]+)(?:\s+(.*))?$",
                lambda m: ParsedCommand(
                    bot=None,
                    command=m.group(1),
                    args=self._split_args(m.group(2) or ""),
                    raw=m.group(0)
                )
            ),
            # @bot command args
            (
                r"^@([a-z]+)\s+([a-z]+)(?:\s+(.*))?$",
                lambda m: ParsedCommand(
                    bot=m.group(1),
                    command=m.group(2),
                    args=self._split_args(m.group(3) or ""),
                    raw=m.group(0)
                )
            ),
            # command args (direct)
            (
                r"^([a-z]+)(?:\s+(.*))?$",
                lambda m: ParsedCommand(
                    bot=None,
                    command=m.group(1),
                    args=self._split_args(m.group(2) or ""),
                    raw=m.group(0)
                )
            ),
        ]
        
    def parse(self, text: str) -> Optional[ParsedCommand]:
        """Parse command text"""
        text = text.strip()
        if not text:
            return None
            
        # Try each pattern
        for pattern, builder in self.patterns:
            match = re.match(pattern, text, re.IGNORECASE)
            if match:
                return builder(match)
                
        return None
        
    def _split_args(self, arg_str: str) -> List[str]:
        """
        Split arguments respecting quotes
        Example: 'arg1 "arg 2" arg3' -> ['arg1', 'arg 2', 'arg3']
        """
        if not arg_str:
            return []
            
        args = []
        current = []
        in_quotes = False
        escaped = False
        
        for char in arg_str:
            if escaped:
                current.append(char)
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quotes = not in_quotes
            elif char.isspace() and not in_quotes:
                if current:
                    args.append("".join(current))
                    current = []
            else:
                current.append(char)
                
        if current:
            args.append("".join(current))
            
        return args


def demo():
    """Demo command parser"""
    parser = CommandParser()
    
    test_cases = [
        "/system status",
        "/system restart ghostlink",
        "!status",
        "!exec ps aux",
        "@metrics get cpu",
        "status",
        'exec echo "hello world"',
        "/system exec ls -la /tmp",
    ]
    
    print("Command Parser Demo")
    print("=" * 50)
    
    for test in test_cases:
        result = parser.parse(test)
        if result:
            print(f"\nInput:   {test}")
            print(f"Bot:     {result.bot or '(any)'}")
            print(f"Command: {result.command}")
            print(f"Args:    {result.args}")
        else:
            print(f"\nInput:   {test}")
            print("Result:  PARSE ERROR")


if __name__ == "__main__":
    demo()
