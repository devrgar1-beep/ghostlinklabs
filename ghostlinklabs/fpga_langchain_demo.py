#!/usr/bin/env python3
"""
FPGA Brain Stem LangChain Integration Demo
Demonstrates system-wide AI toolchaining with FPGA hardware acceleration.
"""

import asyncio
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fpga_brain_stem import FPGABrainStemIntegration


class FPGALangChainDemo:
    """Demonstration of FPGA Brain Stem with LangChain integration"""

    def __init__(self):
        self.fpga_integration = FPGABrainStemIntegration(None)  # Pass None for root_control
        self.agent = None

    async def initialize_system(self) -> bool:
        """Initialize FPGA Brain Stem with LangChain"""
        print("🔌 Initializing FPGA Brain Stem with LangChain integration...")

        # Initialize FPGA hardware
        success = await self.fpga_integration.initialize_brain_stem()
        if not success:
            print("❌ FPGA Brain Stem initialization failed")
            return False

        print("✅ FPGA Brain Stem initialized")

        # Configure LangChain (local models)
        self.fpga_integration.enable_langchain_mode(True)

        # Create LangChain agent with local model
        self.agent = self.fpga_integration.create_langchain_agent()
        if self.agent:
            print("✅ LangChain agent created with FPGA tools (using local model)")
        else:
            print("⚠️  LangChain agent creation failed - install required packages: pip install langchain langchain-community transformers torch")

        return True

    async def demonstrate_fpga_tools(self):
        """Demonstrate FPGA hardware tools"""
        print("\n🔧 FPGA Hardware Tool Demonstration")
        print("=" * 50)

        # Test symbolic logic
        print("🧠 Testing Symbolic Logic Operations:")
        result = await self.fpga_integration.execute_symbolic_operation("AND", [True, False])
        print(f"  AND(True, False) = {result}")

        result = await self.fpga_integration.execute_symbolic_operation("OR", [True, False])
        print(f"  OR(True, False) = {result}")

        result = await self.fpga_integration.execute_symbolic_operation("XOR", [True, True])
        print(f"  XOR(True, True) = {result}")

        # Test neural inference
        print("\n🧠 Testing Neural Inference:")
        neural_input = [0.1, 0.3, 0.5, 0.7, 0.2, 0.8, 0.4, 0.6]
        result = await self.fpga_integration.neural_inference(neural_input)
        print(f"  Neural inference result: {result}")

        # Test PWM control
        print("\n🎛️  Testing PWM Control:")
        pwm_result = await self.fpga_integration.pwm_configure_channel(
            "pwm_channel_0", frequency=1000, duty_cycle=0.5
        )
        print(f"  PWM Channel 0 configured: {pwm_result}")

        # Test memory access
        print("\n💾 Testing Memory Access:")
        eprom_data = await self.fpga_integration.read_eprom(0, 4)
        print(f"  EPROM[0:4]: {eprom_data}")

        eeprom_data = await self.fpga_integration.read_eeprom(0, 4)
        print(f"  EEPROM[0:4]: {eeprom_data}")

    async def demonstrate_langchain_integration(self):
        """Demonstrate LangChain integration with FPGA tools"""
        if not self.agent:
            print("\n🤖 LangChain Integration (Skipped - Local model not available)")
            print("-" * 50)
            print("To enable LangChain features:")
            print("1. Install required packages: pip install langchain langchain-community transformers torch")
            print("2. Optionally set LOCAL_MODEL_PATH for custom local models")
            print("3. Re-run this demo")
            return

        print("\n🤖 LangChain Integration with FPGA Tools")
        print("=" * 50)

        # Show available tools
        tools = self.fpga_integration.get_langchain_tools()
        print(f"Available FPGA Tools: {', '.join(tools)}")

        # Demonstrate tool usage through LangChain
        test_queries = [
            "Perform an AND operation on inputs 1 and 0",
            "Configure PWM channel 5 for audio at 440Hz with 50% duty cycle",
            "Read 8 bytes from EEPROM starting at address 0",
            "Execute neural inference with inputs [0.2, 0.4, 0.6, 0.8]",
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\nQuery {i}: {query}")
            try:
                result = await self.fpga_integration.execute_langchain_query(query)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")

    async def show_system_status(self):
        """Display system status and performance metrics"""
        print("\n📊 System Status Report")
        print("=" * 50)

        status = self.fpga_integration.get_brain_stem_status()

        print(f"FPGA Running: {'✅' if status['running'] else '❌'}")
        print(f"Mode: {status['mode']}")
        print(f"Device: {status['config']['device_type']}")
        print(f"Clock: {status['config']['clock_frequency']/1e6:.1f} MHz")

        print("\nHardware Components:")
        print(f"  • Neural Cores: {status['neural_networks']}")
        print(f"  • PWM Channels: {status['pwm_channels']} ({status['pwm_channels_active']} active)")
        print(f"  • EPROM: {status['eprom_size']} bytes")
        print(f"  • EEPROM: {status['eeprom_size']} bytes")
        print(f"  • SDR Channels: {status['sdr_channels']}")
        print(f"  • MCU Cores: {status['mcu_cores']}")
        print(f"  • ESP32 Cores: {status['esp32_cores']}")
        print(f"  • JTAG Interfaces: {status['jtag_interfaces']}")

        print("\nPerformance Metrics:")
        perf = status['performance']
        print(f"  • Symbolic Operations: {perf['symbolic_operations']}")
        print(f"  • Neural Inferences: {perf['neural_inferences']}")
        print(f"  • PWM Operations: {perf['pwm_operations']}")
        print(f"  • Memory Operations: {perf['eprom_operations'] + perf['eeprom_operations']}")

        if 'langchain_queries' in perf:
            print(f"  • LangChain Queries: {perf['langchain_queries']}")
            print(f"  • Tool Executions: {perf['tool_executions']}")

    async def run_demo(self):
        """Run the complete FPGA LangChain demonstration"""
        print("🎮 FPGA BRAIN STEM - LANGCHAIN INTEGRATION DEMO")
        print("=" * 60)
        print("Demonstrating system-wide AI toolchaining with FPGA hardware acceleration")
        print()

        # Initialize system
        if not await self.initialize_system():
            return

        # Demonstrate FPGA tools
        await self.demonstrate_fpga_tools()

        # Demonstrate LangChain integration
        await self.demonstrate_langchain_integration()

        # Show final status
        await self.show_system_status()

        print("\n🏆 DEMO COMPLETE!")
        print("FPGA Brain Stem with LangChain integration successfully demonstrated")
        print("System-wide AI toolchaining enables powerful hardware-accelerated AI workflows")


async def main():
    """Main demo function"""
    demo = FPGALangChainDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())