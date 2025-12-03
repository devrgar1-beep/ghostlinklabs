#!/usr/bin/env python3
"""
Quick Execution Test for Autonomous Evolution System
Runs a short evolution cycle to verify functionality
"""

from autonomous_evolution import AutonomousEvolution


def test_evolution_cycle():
    """Run a short evolution cycle for testing"""
    print("🧬 Testing Autonomous Evolution System")
    print("=" * 40)

    # Create evolution system
    evolution = AutonomousEvolution()
    print("✅ Evolution system initialized")

    # Run genesis
    evolution._genesis()
    print(f"✅ Created {len(evolution.genome)} foundational genes")

    # Test basic evolution components
    print("\n🧪 Testing Evolution Components:")

    # Test selection
    survivors = evolution._select_fittest()
    print(f"  ✓ Selection: {len(survivors)} survivors from {len(evolution.genome)} genes")

    # Test environment sensing
    env = evolution._sense_environment()
    print(f"  ✓ Environment sensing: {len(env)} parameters detected")

    # Test synergy detection
    if len(evolution.genome) >= 2:
        synergy = evolution._check_synergy(evolution.genome[0], evolution.genome[1])
        print(
            f"  ✓ Synergy detection: {'Found' if synergy else 'Not found'} between first two genes"
        )

    # Test fitness evaluation
    print("  ✓ Fitness evaluation: Running...")
    evolution._fitness_evaluator()
    avg_fitness = sum(g.fitness for g in evolution.genome) / len(evolution.genome)
    print(f"  ✓ Fitness evaluation: Average fitness = {avg_fitness:.2f}")

    # Test checkpoint saving
    evolution.current_generation = 1
    evolution._save_checkpoint()
    print("  ✓ Checkpoint saving: State saved")

    print("\n✅ All evolution components tested successfully!")
    print(f"System ready for autonomous operation with {len(evolution.genome)} genes")


if __name__ == "__main__":
    test_evolution_cycle()
