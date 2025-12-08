// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Model implementation (design independent parts)

#include "Vfpga_brain_stem__pch.h"

//============================================================
// Constructors

Vfpga_brain_stem::Vfpga_brain_stem(VerilatedContext* _vcontextp__, const char* _vcname__)
    : VerilatedModel{*_vcontextp__}
    , vlSymsp{new Vfpga_brain_stem__Syms(contextp(), _vcname__, this)}
    , clk{vlSymsp->TOP.clk}
    , reset_n{vlSymsp->TOP.reset_n}
    , jtag_tck{vlSymsp->TOP.jtag_tck}
    , jtag_tms{vlSymsp->TOP.jtag_tms}
    , command{vlSymsp->TOP.command}
    , ready{vlSymsp->TOP.ready}
    , spi_sck{vlSymsp->TOP.spi_sck}
    , spi_ss_n{vlSymsp->TOP.spi_ss_n}
    , spi_mosi{vlSymsp->TOP.spi_mosi}
    , spi_miso{vlSymsp->TOP.spi_miso}
    , jtag_tdi{vlSymsp->TOP.jtag_tdi}
    , jtag_tdo{vlSymsp->TOP.jtag_tdo}
    , sdr_tx{vlSymsp->TOP.sdr_tx}
    , sdr_rx{vlSymsp->TOP.sdr_rx}
    , pwm_out{vlSymsp->TOP.pwm_out}
    , data_in{vlSymsp->TOP.data_in}
    , data_out{vlSymsp->TOP.data_out}
    , rootp{&(vlSymsp->TOP)}
{
    // Register model with the context
    contextp()->addModel(this);
}

Vfpga_brain_stem::Vfpga_brain_stem(const char* _vcname__)
    : Vfpga_brain_stem(Verilated::threadContextp(), _vcname__)
{
}

//============================================================
// Destructor

Vfpga_brain_stem::~Vfpga_brain_stem() {
    delete vlSymsp;
}

//============================================================
// Evaluation function

#ifdef VL_DEBUG
void Vfpga_brain_stem___024root___eval_debug_assertions(Vfpga_brain_stem___024root* vlSelf);
#endif  // VL_DEBUG
void Vfpga_brain_stem___024root___eval_static(Vfpga_brain_stem___024root* vlSelf);
void Vfpga_brain_stem___024root___eval_initial(Vfpga_brain_stem___024root* vlSelf);
void Vfpga_brain_stem___024root___eval_settle(Vfpga_brain_stem___024root* vlSelf);
void Vfpga_brain_stem___024root___eval(Vfpga_brain_stem___024root* vlSelf);

void Vfpga_brain_stem::eval_step() {
    VL_DEBUG_IF(VL_DBG_MSGF("+++++TOP Evaluate Vfpga_brain_stem::eval_step\n"); );
#ifdef VL_DEBUG
    // Debug assertions
    Vfpga_brain_stem___024root___eval_debug_assertions(&(vlSymsp->TOP));
#endif  // VL_DEBUG
    vlSymsp->__Vm_deleter.deleteAll();
    if (VL_UNLIKELY(!vlSymsp->__Vm_didInit)) {
        vlSymsp->__Vm_didInit = true;
        VL_DEBUG_IF(VL_DBG_MSGF("+ Initial\n"););
        Vfpga_brain_stem___024root___eval_static(&(vlSymsp->TOP));
        Vfpga_brain_stem___024root___eval_initial(&(vlSymsp->TOP));
        Vfpga_brain_stem___024root___eval_settle(&(vlSymsp->TOP));
    }
    VL_DEBUG_IF(VL_DBG_MSGF("+ Eval\n"););
    Vfpga_brain_stem___024root___eval(&(vlSymsp->TOP));
    // Evaluate cleanup
    Verilated::endOfEval(vlSymsp->__Vm_evalMsgQp);
}

//============================================================
// Events and timing
bool Vfpga_brain_stem::eventsPending() { return false; }

uint64_t Vfpga_brain_stem::nextTimeSlot() {
    VL_FATAL_MT(__FILE__, __LINE__, "", "No delays in the design");
    return 0;
}

//============================================================
// Utilities

const char* Vfpga_brain_stem::name() const {
    return vlSymsp->name();
}

//============================================================
// Invoke final blocks

void Vfpga_brain_stem___024root___eval_final(Vfpga_brain_stem___024root* vlSelf);

VL_ATTR_COLD void Vfpga_brain_stem::final() {
    Vfpga_brain_stem___024root___eval_final(&(vlSymsp->TOP));
}

//============================================================
// Implementations of abstract methods from VerilatedModel

const char* Vfpga_brain_stem::hierName() const { return vlSymsp->name(); }
const char* Vfpga_brain_stem::modelName() const { return "Vfpga_brain_stem"; }
unsigned Vfpga_brain_stem::threads() const { return 1; }
void Vfpga_brain_stem::prepareClone() const { contextp()->prepareClone(); }
void Vfpga_brain_stem::atClone() const {
    contextp()->threadPoolpOnClone();
}
