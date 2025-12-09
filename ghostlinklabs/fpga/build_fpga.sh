#!/bin/bash
# FPGA Brain Stem Build Script using Docker

PROJECT=fpga_brain_stem
DOCKER_IMAGE=hdlc/icestorm

echo "Building FPGA Brain Stem..."

# Run synthesis with yosys
docker run --rm -v $(pwd):/work -w /work $DOCKER_IMAGE yosys -p "synth_ice40 -top $PROJECT -json $PROJECT.json" $PROJECT.v symbolic_gates.v neural_cores.v pwm_engine.v spi_controller.v jtag_controller.v sdr_interface.v eprom_memory.v eeprom_memory.v

# Run place and route with nextpnr
docker run --rm -v $(pwd):/work -w /work $DOCKER_IMAGE nextpnr-ice40 --hx1k --json $PROJECT.json --pcf $PROJECT.pcf --asc $PROJECT.asc --package vq100

# Generate bitstream
docker run --rm -v $(pwd):/work -w /work $DOCKER_IMAGE icepack $PROJECT.asc $PROJECT.bin

echo "Build complete. Bitstream: $PROJECT.bin"