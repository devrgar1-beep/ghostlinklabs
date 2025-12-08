#include "Vfpga_brain_stem.h"
#include "verilated.h"

int main(int argc, char** argv) {
    Verilated::commandArgs(argc, argv);

    // Create simulation context
    VerilatedContext* contextp = new VerilatedContext;
    contextp->commandArgs(argc, argv);

    // Instantiate the DUT
    Vfpga_brain_stem* dut = new Vfpga_brain_stem{contextp};

    // Simple test
    dut->reset_n = 0;
    dut->eval();

    dut->reset_n = 1;
    dut->command = 0x01; // Test symbolic gates
    dut->data_in = 0x03; // a=1, b=1
    dut->eval();

    printf("Symbolic gates result: %x\n", dut->data_out);

    // Test neural inference
    dut->command = 0x02; // Neural inference
    dut->data_in = 0x12345678;
    dut->eval();

    printf("Neural inference result: %x\n", dut->data_out);

    // Cleanup
    dut->final();
    delete dut;
    delete contextp;

    return 0;
}