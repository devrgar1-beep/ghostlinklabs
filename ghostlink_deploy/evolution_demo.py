#!/usr/bin/env python3
"""
GhostLink Evolution Demonstration
Shows the evolved behaviors and world building capabilities
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from ghostlink_core import GhostLinkSystem

async def evolution_demo():
    """Demonstrate the evolved capabilities"""
    print("🧬 GHOSTLINK EVOLUTION DEMONSTRATION")
    print("=" * 50)

    # Initialize system
    system = GhostLinkSystem()

    # Run extended evolution cycles
    print("🚀 Starting Evolution Demonstration...")

    await system.run_loop(cycles=12)  # More cycles to see evolution

    # Save evolution state
    evolution_file = "evolution_state_demo.json"
    await system.evolution.save_evolution_state(evolution_file)

    # Deploy best evolved behavior
    print("\n🎯 Deploying Best Evolved Behavior...")
    success = await system.evolution.deploy_best_behavior()

    if success:
        print("✅ Evolution demonstration completed successfully!")
        print(f"💾 Evolution state saved to: {evolution_file}")

        # Show evolution statistics
        if system.evolution.best_genome:
            best = system.evolution.best_genome
            print("🏆 Best Genome Stats:")
            print(f"   ID: {best.id}")
            print(f"   Generation: {best.generation}")
            print(f"   Fitness: {best.fitness:.2f}")
            print(f"   Genes: {best.genes}")
            if best.mutation_history:
                print(f"   Mutation History: {best.mutation_history}")

    else:
        print("⚠️  Evolution deployment encountered issues")

if __name__ == "__main__":
    asyncio.run(evolution_demo())