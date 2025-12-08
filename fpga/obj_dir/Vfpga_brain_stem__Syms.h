// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Symbol table internal header
//
// Internal details; most calling programs do not need this header,
// unless using verilator public meta comments.

#ifndef VERILATED_VFPGA_BRAIN_STEM__SYMS_H_
#define VERILATED_VFPGA_BRAIN_STEM__SYMS_H_  // guard

#include "verilated.h"

// INCLUDE MODEL CLASS

#include "Vfpga_brain_stem.h"

// INCLUDE MODULE CLASSES
#include "Vfpga_brain_stem___024root.h"

// SYMS CLASS (contains all model state)
class alignas(VL_CACHE_LINE_BYTES) Vfpga_brain_stem__Syms final : public VerilatedSyms {
  public:
    // INTERNAL STATE
    Vfpga_brain_stem* const __Vm_modelp;
    VlDeleter __Vm_deleter;
    bool __Vm_didInit = false;

    // MODULE INSTANCE STATE
    Vfpga_brain_stem___024root     TOP;

    // CONSTRUCTORS
    Vfpga_brain_stem__Syms(VerilatedContext* contextp, const char* namep, Vfpga_brain_stem* modelp);
    ~Vfpga_brain_stem__Syms();

    // METHODS
    const char* name() { return TOP.name(); }
};

#endif  // guard
