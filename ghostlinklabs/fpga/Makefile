# FPGA Brain Stem Build System
# Requires: yosys, nextpnr-ice40, icepack

PROJECT = fpga_brain_stem
SOURCES = $(PROJECT).v symbolic_gates.v neural_cores.v pwm_engine.v spi_controller.v jtag_controller.v sdr_interface.v eprom_memory.v eeprom_memory.v
PCF = $(PROJECT).pcf

# Toolchain
YOSYS = yosys
NEXTPNR = nextpnr-ice40
ICEPACK = icepack
IVERILOG = iverilog
VVP = vvp

# Targets
.PHONY: all clean program simulate

all: $(PROJECT).bin

# Synthesis
$(PROJECT).json: $(SOURCES)
	$(YOSYS) -p "synth_ice40 -top $(PROJECT) -json $@" $(SOURCES)

# Place and route
$(PROJECT).asc: $(PROJECT).json $(PCF)
	$(NEXTPNR) --hx1k --json $< --pcf $(PCF) --asc $@ --package vq100

# Generate bitstream
$(PROJECT).bin: $(PROJECT).asc
	$(ICEPACK) $< $@

# Simulation
simulate: $(PROJECT)_tb
	$(VVP) $(PROJECT)_tb

$(PROJECT)_tb: $(PROJECT)_tb.v $(SOURCES)
	$(IVERILOG) -o $@ $^

# Clean
clean:
	rm -f *.json *.asc *.bin *.vcd *_tb

# Program FPGA (requires iceprog)
program: $(PROJECT).bin
	iceprog $<

# Dependencies
$(PROJECT).json: $(SOURCES)
$(PROJECT).asc: $(PROJECT).json $(PCF)
$(PROJECT).bin: $(PROJECT).asc