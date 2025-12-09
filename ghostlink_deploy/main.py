import asyncio
import sys
import os

# Ensure the current directory is in the path so we can import ghostlink_core
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ghostlink_core import GhostLinkSystem

async def main():
    try:
        system = GhostLinkSystem()
        # Run a standard production session of 5 cycles
        await system.run_loop(cycles=5)
    except KeyboardInterrupt:
        print("\n⚠️  Operator Interrupt. Shutting down.")
    except Exception as e:
        print(f"\n❌ Critical Failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
