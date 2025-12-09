// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table implementation internals

#include "Vfpga_brain_stem__pch.h"
#include "Vfpga_brain_stem.h"
#include "Vfpga_brain_stem___024root.h"

// FUNCTIONS
Vfpga_brain_stem__Syms::~Vfpga_brain_stem__Syms()
{
}

Vfpga_brain_stem__Syms::Vfpga_brain_stem__Syms(VerilatedContext* contextp, const char* namep, Vfpga_brain_stem* modelp)
    : VerilatedSyms{contextp}
    // Setup internal state of the Syms class
    , __Vm_modelp{modelp}
    // Setup module instances
    , TOP{this, namep}
{
    // Check resources
    Verilated::stackCheck(222);
    // Configure time unit / time precision
    _vm_contextp__->timeunit(-9);
    _vm_contextp__->timeprecision(-12);
    // Setup each module's pointers to their submodules
    // Setup each module's pointer back to symbol table (for public functions)
    TOP.__Vconfigure(true);
}
