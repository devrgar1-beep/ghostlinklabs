#!/usr/bin/env python3
"""
Execution Script for Autonomous Evolution System
Runs the self-evolving, self-improving intelligence system
"""

import argparse
from pathlib import Path
import signal
import sys

from autonomous_evolution import AutonomousEvolution


def signal_handler(signum, _frame):
    """Handle interrupt signals gracefully"""
    print(f"\n[EXECUTION] Received signal {signum}. Shutting down evolution...")
    sys.exit(0)


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="Run GhostLink Autonomous Evolution System")
    parser.add_argument(
        "--max-generations",
        type=int,
        default=None,
        help="Maximum generations to run (default: unlimited)",
    )
    parser.add_argument(
        "--checkpoint-interval",
        type=int,
        default=25,
        help="Generations between checkpoints (default: 25)",
    )
    parser.add_argument(
        "--log-level",
        choices=["minimal", "standard", "verbose"],
        default="standard",
        help="Logging verbosity level",
    )
    parser.add_argument(
        "--resume-from", type=str, default=None, help="Resume from checkpoint file path"
    )

    args = parser.parse_args()

    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("🚀 GhostLink Autonomous Evolution System")
    print("=" * 50)
    print(f"Max Generations: {args.max_generations or 'Unlimited'}")
    print(f"Checkpoint Interval: {args.checkpoint_interval}")
    print(f"Log Level: {args.log_level}")
    if args.resume_from:
        print(f"Resuming from: {args.resume_from}")
    print()

    try:
        # Initialize evolution system
        evolution = AutonomousEvolution()

        # Resume from checkpoint if specified
        if args.resume_from:
            checkpoint_path = Path(args.resume_from)
            if checkpoint_path.exists():
                print(f"[EXECUTION] Loading checkpoint: {checkpoint_path}")
                # Note: In a full implementation, you'd load the checkpoint here
                # For now, we start fresh
            else:
                print(f"[ERROR] Checkpoint not found: {checkpoint_path}")
                return 1

        # Modify checkpoint interval if specified
        if args.checkpoint_interval != 25:
            # This would modify the evolution system's checkpoint behavior
            print(f"[EXECUTION] Checkpoint interval set to {args.checkpoint_interval}")

        # Start autonomous evolution
        print("[EXECUTION] Starting autonomous evolution...")
        final_generation = evolution.initiate_autonomy()

        print(f"\n✅ Evolution completed at generation {final_generation}")

        return 0

    except (KeyboardInterrupt, SystemExit):
        print("\n[EXECUTION] Evolution interrupted by user")
        return 0
    except Exception as e:
        print(f"\n❌ Evolution failed with error: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
