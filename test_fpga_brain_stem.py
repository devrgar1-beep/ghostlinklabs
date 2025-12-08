#!/usr/bin/env python3
"""
Test script for FPGA Brain Stem integration
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_fpga_brain_stem():
    """Test FPGA Brain Stem functionality"""
    try:
        from fpga_brain_stem import FPGABrainStem, FPGABrainStemConfig

        print("Testing FPGA Brain Stem...")

        # Create FPGA Brain Stem instance
        config = FPGABrainStemConfig()
        fpga = FPGABrainStem(config)

        # Initialize
        print("Initializing FPGA Brain Stem...")
        success = await fpga.initialize()
        if not success:
            print("Failed to initialize FPGA Brain Stem")
            return False

        print("FPGA Brain Stem initialized successfully")

        # Test symbolic operation
        print("Testing symbolic operation...")
        operation = {
            "type": "logic_gate",
            "inputs": {"input_a": True, "input_b": False},
            "logic": {"and": True}
        }

        result = await fpga.execute_symbolic_operation(operation)
        print(f"Symbolic operation result: {result}")

        # Test neural inference
        print("Testing neural inference...")
        input_data = [0.5, 0.3, 0.8]
        output = await fpga.neural_inference("neural_core_0", input_data)
        print(f"Neural inference output: {output}")

        # Test quantum simulation
        print("Testing quantum simulation...")
        state = await fpga.quantum_simulate("quantum_unit_0", "hadamard")
        print(f"Quantum state after Hadamard: {state}")

        # Get status
        status = fpga.get_status()
        print(f"FPGA Status: {status}")

        # Shutdown
        await fpga.shutdown()
        print("FPGA Brain Stem test completed successfully")
        return True

    except ImportError as e:
        print(f"Import error: {e}")
        return False
    except Exception as e:
        print(f"Test failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_fpga_brain_stem())
    sys.exit(0 if success else 1)