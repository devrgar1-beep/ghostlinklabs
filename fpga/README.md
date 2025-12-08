# FPGA Brain Stem - Physical Hardware Implementation

This directory contains the Verilog HDL implementation of the FPGA Brain Stem, translated from the Python simulation for deployment on physical FPGA hardware.

## Files Overview

- `fpga_brain_stem.v` - Main FPGA module integrating all components
- `symbolic_gates.v` - Basic logic gates (AND, OR, NOT, XOR)
- `neural_cores.v` - Simplified neural processing cores
- `pwm_engine.v` - 16-channel PWM controller
- `spi_controller.v` - SPI master controller with 8 slave selects
- `jtag_controller.v` - JTAG debugging interface
- `sdr_interface.v` - Simplified SDR communication interface
- `eprom_memory.v` - 32KB EPROM simulation
- `eeprom_memory.v` - 8KB EEPROM simulation
- `fpga_brain_stem.pcf` - Pin constraints for iCE40-HX1K FPGA
- `Makefile` - Build system for FPGA synthesis
- `build_fpga.sh` - Docker-based build script
- `sim_main.cpp` - C++ simulation main function
- `fpga_brain_stem_tb.v` - Verilog testbench (incomplete)

## Target Hardware

- **FPGA**: Lattice iCE40-HX1K (TQFP-144 package)
- **Clock**: 100MHz
- **Resources Used**:
  - ~1280 LUTs (gates)
  - 8 neural cores
  - 16 PWM channels
  - SPI with 8 slave selects
  - JTAG interface
  - Memory: 32KB EPROM + 8KB EEPROM

## Building for Physical Hardware

### Prerequisites

1. **FPGA Toolchain**:
   - Yosys (synthesis)
   - nextpnr (place & route)
   - icepack (bitstream generation)
   - iceprog (programming)

2. **Installation on macOS**:

   ```bash
   # Install Homebrew (if not already installed)
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

   # Install FPGA tools (may require building from source)
   brew install verilator  # For simulation

   # For actual FPGA tools, you may need to build from source:
   git clone https://github.com/YosysHQ/icestorm.git
   cd icestorm
   make -j$(nproc)
   sudo make install
   ```

### Build Process

1. **Using Docker (Recommended)**:

   ```bash
   # Ensure Docker Desktop is running
   open -a Docker

   # Build the FPGA bitstream
   ./build_fpga.sh
   ```

2. **Using Native Tools**:

   ```bash
   # Synthesis
   yosys -p "synth_ice40 -top fpga_brain_stem -json fpga_brain_stem.json" *.v

   # Place and route
   nextpnr-ice40 --hx1k --json fpga_brain_stem.json --pcf fpga_brain_stem.pcf --asc fpga_brain_stem.asc --package vq100

   # Generate bitstream
   icepack fpga_brain_stem.asc fpga_brain_stem.bin
   ```

### Programming the FPGA

1. **Connect iCE40 Board**:
   - Ensure the board is properly connected via USB
   - Verify device recognition: `ls /dev/tty*` or check device manager

2. **Program the Device**:

   ```bash
   iceprog fpga_brain_stem.bin
   ```

## Interface Specification

### Input Signals

- `clk`: 100MHz system clock
- `reset_n`: Active-low reset
- `command[7:0]`: Command register
- `data_in[31:0]`: Input data bus

### Output Signals

- `data_out[31:0]`: Output data bus
- `ready`: Operation complete flag
- `pwm_out[15:0]`: PWM output channels
- `spi_sck`: SPI clock
- `spi_ss_n[7:0]`: SPI slave selects
- `spi_mosi`: SPI master out slave in
- `jtag_tck/tms/tdi`: JTAG signals
- `jtag_tdo`: JTAG output
- `sdr_tx`: SDR transmit
- `sdr_rx`: SDR receive (input)

### Command Codes

- `0x01`: Execute symbolic logic operation
- `0x02`: Neural inference
- `0x03`: Read EPROM
- `0x04`: Read EEPROM
- `0x10`: SPI transmit

## Testing and Verification

### Simulation

```bash
# Build and run simulation
verilator -Wno-fatal --cc fpga_brain_stem.v *.v --exe sim_main.cpp --top-module fpga_brain_stem
make -C obj_dir -f Vfpga_brain_stem.mk
./obj_dir/Vfpga_brain_stem
```

### Hardware Testing

1. Program the FPGA
2. Connect test equipment to verify:
   - PWM outputs with oscilloscope
   - SPI signals with logic analyzer
   - JTAG functionality
   - Memory read operations

## Integration with GhostLink

The FPGA Brain Stem serves as the hardware acceleration platform for GhostLink's AI systems. It provides:

- Real-time symbolic processing
- Neural network inference acceleration
- PWM control for robotics
- Communication interfaces (SPI, SDR)
- Debugging capabilities (JTAG)

## Performance Characteristics

- **Clock Frequency**: 100MHz
- **PWM Resolution**: 12-bit (4096 levels)
- **PWM Frequency**: Configurable, default 1kHz
- **Memory Access**: Single cycle for EPROM/EEPROM
- **Neural Processing**: 8 parallel cores
- **SPI Speed**: Up to 50MHz (board dependent)

## Future Enhancements

- Add more sophisticated neural network implementations
- Implement quantum simulation cores
- Add Ethernet/MAC interfaces
- Integrate with ARM processors for SoC functionality
- Add DDR memory controllers
- Implement advanced DSP functions

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Ensure all Verilog files are in the same directory
   - Check for syntax errors in HDL code
   - Verify toolchain installation

2. **Programming Issues**:
   - Check USB connection to FPGA board
   - Verify board power supply
   - Ensure correct pin constraints for target board

3. **Functional Issues**:
   - Verify clock signal integrity
   - Check reset timing
   - Validate input data formats

### Debug Tips

- Use `iverilog` for basic syntax checking
- Add debug signals to monitor internal states
- Use JTAG for in-circuit debugging
- Implement status registers for health monitoring

## LangChain Integration

The FPGA Brain Stem includes comprehensive LangChain integration for system-wide AI toolchaining. This enables natural language control of hardware-accelerated AI operations.

### Features

- **Hardware-Accelerated Tools**: FPGA operations exposed as LangChain tools
- **Agent Orchestration**: AI agents that can control hardware through natural language
- **Real-time Performance**: Hardware acceleration for AI inference and control
- **Memory Integration**: Persistent memory access through conversational interfaces

### Available Tools

1. **Symbolic Logic Tool**: Execute AND, OR, NOT, XOR operations
2. **Neural Inference Tool**: Perform hardware-accelerated neural network inference
3. **PWM Control Tool**: Configure PWM outputs for motor/audio control
4. **Memory Access Tool**: Read/write EPROM and EEPROM

### Usage Example

```python
from fpga_brain_stem import FPGABrainStemIntegration

# Initialize FPGA with LangChain
fpga = FPGABrainStemIntegration(root_control)
await fpga.initialize_brain_stem()

# Configure LangChain
fpga.set_openai_api_key("your-api-key")
agent = fpga.create_langchain_agent()

# Execute natural language commands
result = await fpga.execute_langchain_query(
    "Configure PWM channel 0 for motor control at 20kHz with 75% duty cycle"
)
```

### Requirements

```bash
pip install langchain langchain-openai langchain-core
export OPENAI_API_KEY="your-api-key"
```

### Demo

Run the LangChain integration demo:

```bash
python fpga_langchain_demo.py
```
