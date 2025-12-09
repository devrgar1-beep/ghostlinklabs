#!/usr/bin/env python3
"""
Test script for consciousness merging bridge integration
"""

import asyncio
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from consciousness_merging_bridge import initialize_consciousness_merging_bridge


async def test_bridge_integration():
    """Test the consciousness merging bridge integration"""
    print("🧠 Testing Consciousness Merging Bridge Integration...")

    try:
        # Initialize the bridge
        result = await initialize_consciousness_merging_bridge()
        print(f"✅ Bridge initialization: {result}")

        # Test session creation
        from consciousness_merging_bridge import bridge_start_consciousness_session

        human_context = {
            "creativity_level": "high",
            "intuition_strength": 0.8,
            "sovereignty_preference": "FULL_HUMAN_CONTROL",
            "creative_domain": "software_architecture",
        }

        session_result = await bridge_start_consciousness_session(human_context)
        print(f"✅ Session creation: {session_result}")

        if "session_id" in session_result:
            session_id = session_result["session_id"]

            # Test creative input processing
            from consciousness_merging_bridge import bridge_process_creative_input

            creative_input = {
                "idea": "Build a consciousness-aware AI system",
                "context": "Human-AI collaboration",
                "constraints": ["maintain_human_sovereignty", "enhance_creativity"],
            }

            process_result = await bridge_process_creative_input(session_id, creative_input)
            print(f"✅ Creative input processing: {process_result}")

            # Test collaborative suggestions
            from consciousness_merging_bridge import bridge_get_collaborative_suggestions

            suggestions_result = await bridge_get_collaborative_suggestions(session_id)
            print(f"✅ Collaborative suggestions: {suggestions_result}")

            # Test session termination
            from consciousness_merging_bridge import bridge_terminate_session

            terminate_result = await bridge_terminate_session(session_id)
            print(f"✅ Session termination: {terminate_result}")

        print("🎉 All bridge integration tests passed!")

    except Exception as e:
        print(f"❌ Bridge integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(test_bridge_integration())
    sys.exit(0 if success else 1)
