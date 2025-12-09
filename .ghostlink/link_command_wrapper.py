#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, "/Users/ghost-link-labs/ghostlinklabs/src")

from enable_shell_integration import LinkCommandInterceptor

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)

    interceptor = LinkCommandInterceptor()
    command = " ".join(sys.argv[1:])
    sys.exit(interceptor.execute_command(command))
