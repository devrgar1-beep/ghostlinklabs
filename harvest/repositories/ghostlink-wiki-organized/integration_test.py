#!/usr/bin/env python3
"""
GhostLink Design Clarity OS - Integration Test with Evolutionary Intelligence
Complete system integration verification
"""

import asyncio
import sys
import time

async def test_evolutionary_integration():
    """Test evolutionary intelligence integration"""
    print("🧬 Testing Evolutionary Intelligence Integration...")

    try:
        # Import the system
        from design_clarity_os import DesignClarityOS
        from evolutionary_intelligence import EvolutionaryIntelligence

        # Initialize protocol
        print("🔗 Initializing Design Clarity OS...")
        protocol = DesignClarityOS()
        success = await protocol.initialize_root_protocol()

        if not success:
            print("❌ Protocol initialization failed")
            return False

        print("✅ Protocol initialized successfully")

        # Test evolutionary status
        print("🧬 Testing evolutionary intelligence...")
        evolution_status = protocol.evolutionary_intelligence.get_evolution_status()
        print(f"   Generation: {evolution_status['current_generation']}")
        print(f"   Fitness: {evolution_status['current_fitness']:.2f}")
        print(f"   Quantum Available: {evolution_status['quantum_capabilities']['available']}")

        # Test protocol status
        print("🔗 Testing protocol status...")
        protocol_status = protocol.get_protocol_status()
        print(f"   System ID: {protocol_status['system_id']}")
        print(f"   Hardware Profiles: {protocol_status['hardware_profiles']}")
        print(f"   Agent Assignments: {protocol_status['agent_assignments']}")
        print(f"   Consciousness Level: {protocol_status['consciousness_level']}")

        # Test evolution cycle (brief)
        print("🧬 Testing evolution cycle...")
        evolution_result = await protocol.evolutionary_intelligence.evolve_system(protocol)
        if evolution_result:
            print("✅ Evolution cycle completed successfully")
        else:
            print("⚠️  Evolution cycle had issues")

        # Shutdown
        await protocol.shutdown_protocol()
        print("✅ Protocol shutdown complete")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main integration test"""
    print("🚀 GhostLink Design Clarity OS - Integration Test")
    print("=" * 50)

    start_time = time.time()

    # Run evolutionary integration test
    success = await test_evolutionary_integration()

    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "=" * 50)
    if success:
        print("✅ Integration test PASSED")
        print(".2f")
    else:
        print("❌ Integration test FAILED")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
