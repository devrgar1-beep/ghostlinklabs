#!/usr/bin/env python3
"""
GhostLink Model Training Script
Collects data and trains the custom GhostLink AI model
"""

import asyncio
from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ghostlink.core.autonomous_agents import agent_orchestrator
from ghostlink.core.ghostlink_model import ghostlink_model


async def collect_agent_data():
    """Collect data from agent interactions"""
    print("Collecting data from agent interactions...")

    # Run some sample agent tasks to generate training data
    sample_tasks = [
        "Analyze the current project structure",
        "Suggest improvements for the codebase",
        "Explain how the AI providers work",
        "Tell me a joke about programming",
        "What are the main components of GhostLink?",
    ]

    for task in sample_tasks:
        try:
            print(f"Running agent task: {task}")
            result = await agent_orchestrator.run_agent_task(task)

            # The agent should have learned from this interaction
            # (assuming the autonomous_agents.py has been updated to call learn_from_interaction)

        except Exception as e:
            print(f"Error running task '{task}': {e}")


async def train_model():
    """Train the GhostLink model"""
    print("Starting GhostLink model training...")

    try:
        # Initialize the model
        await ghostlink_model.initialize()

        # Collect training data
        await ghostlink_model.collect_training_data()

        # Show training stats
        stats = ghostlink_model.get_training_stats()
        print("Training Data Stats:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

        if stats["total_samples"] == 0:
            print("No training data found. Collecting sample data...")
            await collect_agent_data()
            await ghostlink_model.collect_training_data()

        # Train the model
        await ghostlink_model.train(epochs=2, batch_size=2, learning_rate=5e-5)

        print("Model training completed!")

    except Exception as e:
        print(f"Training failed: {e}")
        import traceback

        traceback.print_exc()


async def test_model():
    """Test the trained model"""
    print("\nTesting the trained model...")

    test_questions = [
        "What is GhostLink?",
        "How do autonomous agents work?",
        "Tell me about AI providers",
        "What can you help me with?",
    ]

    for question in test_questions:
        try:
            response = await ghostlink_model.generate_response(question)
            print(f"\nQ: {question}")
            print(f"A: {response}")
        except Exception as e:
            print(f"Error testing question '{question}': {e}")


async def main():
    """Main training workflow"""
    print("GhostLink Custom Model Training")
    print("=" * 40)

    # Train the model
    await train_model()

    # Test the model
    await test_model()

    print("\nTraining and testing completed!")
    print("The custom GhostLink model is now available as an AI provider.")


if __name__ == "__main__":
    asyncio.run(main())
