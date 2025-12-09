// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design internal header
// See Vfpga_brain_stem.h for the primary calling header

#ifndef VERILATED_VFPGA_BRAIN_STEM___024ROOT_H_
#define VERILATED_VFPGA_BRAIN_STEM___024ROOT_H_  // guard

#include "verilated.h"


class Vfpga_brain_stem__Syms;

class alignas(VL_CACHE_LINE_BYTES) Vfpga_brain_stem___024root final : public VerilatedModule {
  public:

    // DESIGN SPECIFIC STATE
    VL_IN8(clk,0,0);
    VL_IN8(reset_n,0,0);
    VL_IN8(jtag_tck,0,0);
    VL_IN8(jtag_tms,0,0);
    VL_IN8(command,7,0);
    VL_OUT8(ready,0,0);
    VL_OUT8(spi_sck,0,0);
    VL_OUT8(spi_ss_n,7,0);
    VL_OUT8(spi_mosi,0,0);
    VL_IN8(spi_miso,0,0);
    VL_IN8(jtag_tdi,0,0);
    VL_OUT8(jtag_tdo,0,0);
    VL_OUT8(sdr_tx,0,0);
    VL_IN8(sdr_rx,0,0);
    CData/*2:0*/ fpga_brain_stem__DOT__spi__DOT__state;
    CData/*7:0*/ fpga_brain_stem__DOT__spi__DOT__tx_data;
    CData/*2:0*/ fpga_brain_stem__DOT__spi__DOT__bit_count;
    CData/*7:0*/ fpga_brain_stem__DOT__spi__DOT__slave_select;
    CData/*1:0*/ fpga_brain_stem__DOT__spi__DOT__clk_div;
    CData/*3:0*/ fpga_brain_stem__DOT__jtag__DOT__state;
    CData/*4:0*/ fpga_brain_stem__DOT__jtag__DOT__ir;
    CData/*3:0*/ fpga_brain_stem__DOT__sdr__DOT__tx_bit_count;
    CData/*7:0*/ fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg;
    CData/*0:0*/ fpga_brain_stem__DOT__sdr__DOT__tx_active;
    CData/*0:0*/ __VstlFirstIteration;
    CData/*0:0*/ __Vtrigprevexpr___TOP__clk__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__reset_n__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__jtag_tck__0;
    CData/*0:0*/ __Vtrigprevexpr___TOP__jtag_tms__0;
    VL_OUT16(pwm_out,15,0);
    SData/*11:0*/ fpga_brain_stem__DOT__pwm__DOT__counter;
    VL_IN(data_in,31,0);
    VL_OUT(data_out,31,0);
    IData/*31:0*/ fpga_brain_stem__DOT__pwm_counter;
    IData/*31:0*/ fpga_brain_stem__DOT__neural_output;
    IData/*31:0*/ fpga_brain_stem__DOT__neural__DOT__bias;
    IData/*31:0*/ fpga_brain_stem__DOT__neural__DOT__sum;
    IData/*31:0*/ fpga_brain_stem__DOT__jtag__DOT__dr;
    IData/*31:0*/ __VactIterCount;
    VlUnpacked<IData/*31:0*/, 8> fpga_brain_stem__DOT__neural__DOT__weights;
    VlUnpacked<SData/*11:0*/, 16> fpga_brain_stem__DOT__pwm__DOT__duty_cycle;
    VlUnpacked<IData/*31:0*/, 8192> fpga_brain_stem__DOT__eprom__DOT__memory;
    VlUnpacked<IData/*31:0*/, 2048> fpga_brain_stem__DOT__eeprom__DOT__memory;
    VlUnpacked<QData/*63:0*/, 1> __VstlTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VactTriggered;
    VlUnpacked<QData/*63:0*/, 1> __VnbaTriggered;

    // INTERNAL VARIABLES
    Vfpga_brain_stem__Syms* const vlSymsp;

    // CONSTRUCTORS
    Vfpga_brain_stem___024root(Vfpga_brain_stem__Syms* symsp, const char* v__name);
    ~Vfpga_brain_stem___024root();
    VL_UNCOPYABLE(Vfpga_brain_stem___024root);

    // INTERNAL METHODS
    void __Vconfigure(bool first);
};


#endif  // guard
