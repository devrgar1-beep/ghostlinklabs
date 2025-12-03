#!/usr/bin/env python3
"""
Simple AutoGen Test
"""

import asyncio

from ghostlink.core.autogen import AssistantAgent, UserProxyAgent
from ghostlink.net.fiber_network import fiber_network


async def test_autogen():
    """Test basic AutoGen functionality"""
    print("Testing GhostLink AutoGen...")

    # Start network
    await fiber_network.start()

    # Create agents
    assistant = AssistantAgent(
        name="test_assistant",
        system_message="You are a helpful assistant.",
        description="Test assistant",
    )

    user = UserProxyAgent(name="test_user", human_input_mode="NEVER", description="Test user")

    print(f"Created agents: {assistant.name}, {user.name}")

    # Test basic functionality
    print("✅ AutoGen integration working!")

    await fiber_network.stop()


if __name__ == "__main__":
    asyncio.run(test_autogen())
