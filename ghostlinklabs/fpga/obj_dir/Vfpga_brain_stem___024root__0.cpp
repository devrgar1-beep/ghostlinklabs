// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vfpga_brain_stem.h for the primary calling header

#include "Vfpga_brain_stem__pch.h"

#ifdef VL_DEBUG
VL_ATTR_COLD void Vfpga_brain_stem___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG

void Vfpga_brain_stem___024root___eval_triggers__act(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_triggers__act\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VactTriggered[0U] = (QData)((IData)(
                                                    (((((~ (IData)(vlSelfRef.jtag_tms)) 
                                                        & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__jtag_tms__0)) 
                                                       << 3U) 
                                                      | (((IData)(vlSelfRef.jtag_tck) 
                                                          & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__jtag_tck__0))) 
                                                         << 2U)) 
                                                     | ((((~ (IData)(vlSelfRef.reset_n)) 
                                                          & (IData)(vlSelfRef.__Vtrigprevexpr___TOP__reset_n__0)) 
                                                         << 1U) 
                                                        | ((IData)(vlSelfRef.clk) 
                                                           & (~ (IData)(vlSelfRef.__Vtrigprevexpr___TOP__clk__0)))))));
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__reset_n__0 = vlSelfRef.reset_n;
    vlSelfRef.__Vtrigprevexpr___TOP__jtag_tck__0 = vlSelfRef.jtag_tck;
    vlSelfRef.__Vtrigprevexpr___TOP__jtag_tms__0 = vlSelfRef.jtag_tms;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vfpga_brain_stem___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
    }
#endif
}

bool Vfpga_brain_stem___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___trigger_anySet__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        if (in[n]) {
            return (1U);
        }
        n = ((IData)(1U) + n);
    } while ((1U > n));
    return (0U);
}

void Vfpga_brain_stem___024root___nba_sequent__TOP__0(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___nba_sequent__TOP__0\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __Vdly__fpga_brain_stem__DOT__pwm_counter;
    __Vdly__fpga_brain_stem__DOT__pwm_counter = 0;
    CData/*1:0*/ __Vdly__fpga_brain_stem__DOT__spi__DOT__clk_div;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__clk_div = 0;
    CData/*7:0*/ __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data = 0;
    CData/*2:0*/ __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count = 0;
    CData/*2:0*/ __Vdly__fpga_brain_stem__DOT__spi__DOT__state;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__state = 0;
    CData/*7:0*/ __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg;
    __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg = 0;
    CData/*0:0*/ __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active;
    __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active = 0;
    CData/*3:0*/ __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count;
    __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count = 0;
    CData/*0:0*/ __VdlySet__fpga_brain_stem__DOT__neural__DOT__weights__v0;
    __VdlySet__fpga_brain_stem__DOT__neural__DOT__weights__v0 = 0;
    // Body
    __VdlySet__fpga_brain_stem__DOT__neural__DOT__weights__v0 = 0U;
    __Vdly__fpga_brain_stem__DOT__pwm_counter = vlSelfRef.fpga_brain_stem__DOT__pwm_counter;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__clk_div 
        = vlSelfRef.fpga_brain_stem__DOT__spi__DOT__clk_div;
    __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg 
        = vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg;
    __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active 
        = vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_active;
    __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count 
        = vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_bit_count;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data 
        = vlSelfRef.fpga_brain_stem__DOT__spi__DOT__tx_data;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count 
        = vlSelfRef.fpga_brain_stem__DOT__spi__DOT__bit_count;
    __Vdly__fpga_brain_stem__DOT__spi__DOT__state = vlSelfRef.fpga_brain_stem__DOT__spi__DOT__state;
    if (vlSelfRef.reset_n) {
        __Vdly__fpga_brain_stem__DOT__pwm_counter = 
            ((0x000186a0U <= vlSelfRef.fpga_brain_stem__DOT__pwm_counter)
              ? 0U : ((IData)(1U) + vlSelfRef.fpga_brain_stem__DOT__pwm_counter));
        if ((0x000186a0U == vlSelfRef.fpga_brain_stem__DOT__pwm_counter)) {
            vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter 
                = ((0x0fffU <= (IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter))
                    ? 0U : (0x00000fffU & ((IData)(1U) 
                                           + (IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter))));
        }
        __Vdly__fpga_brain_stem__DOT__spi__DOT__clk_div 
            = (3U & ((IData)(1U) + (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__clk_div)));
        if ((1U == (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__clk_div))) {
            vlSelfRef.spi_sck = 1U;
        }
        if ((3U == (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__clk_div))) {
            vlSelfRef.spi_sck = 0U;
        }
        if (((~ (IData)(vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_active)) 
             & (0U != (0x000000ffU & vlSelfRef.data_in)))) {
            __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg 
                = (0x000000ffU & vlSelfRef.data_in);
            __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active = 1U;
            __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count = 0U;
        } else if (vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_active) {
            __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count 
                = (0x0000000fU & ((IData)(1U) + (IData)(vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_bit_count)));
            vlSelfRef.sdr_tx = (1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg));
            if ((7U == (IData)(vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_bit_count))) {
                __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active = 0U;
            }
            __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg 
                = (0x0000007fU & ((IData)(vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg) 
                                  >> 1U));
        }
        if ((0U == (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__state))) {
            if ((0x10U == (IData)(vlSelfRef.command))) {
                __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data 
                    = (0x000000ffU & (vlSelfRef.data_in 
                                      >> 8U));
                vlSelfRef.spi_ss_n = (0x000000ffU & 
                                      (~ VL_SHIFTL_III(8,32,8, (IData)(1U), (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__slave_select))));
                __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count = 0U;
                __Vdly__fpga_brain_stem__DOT__spi__DOT__state = 1U;
                vlSelfRef.fpga_brain_stem__DOT__spi__DOT__slave_select 
                    = (0x000000ffU & vlSelfRef.data_in);
            }
        } else if ((1U == (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__state))) {
            __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count 
                = (7U & ((IData)(1U) + (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__bit_count)));
            vlSelfRef.spi_mosi = (1U & ((IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__tx_data) 
                                        >> 7U));
            if ((7U == (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__bit_count))) {
                __Vdly__fpga_brain_stem__DOT__spi__DOT__state = 2U;
            }
            __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data 
                = ((0x000000feU & ((IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__tx_data) 
                                   << 1U)) | (IData)(vlSelfRef.spi_miso));
        } else if ((2U == (IData)(vlSelfRef.fpga_brain_stem__DOT__spi__DOT__state))) {
            vlSelfRef.spi_ss_n = 0xffU;
            __Vdly__fpga_brain_stem__DOT__spi__DOT__state = 0U;
        }
        vlSelfRef.data_out = ((1U == (IData)(vlSelfRef.command))
                               ? ((((2U & ((vlSelfRef.data_in 
                                            << 1U) 
                                           ^ (0xfffffffeU 
                                              & vlSelfRef.data_in))) 
                                    | (1U & (~ vlSelfRef.data_in))) 
                                   << 2U) | (((IData)(
                                                      (0U 
                                                       != 
                                                       (3U 
                                                        & vlSelfRef.data_in))) 
                                              << 1U) 
                                             | (IData)(
                                                       (3U 
                                                        == 
                                                        (3U 
                                                         & vlSelfRef.data_in)))))
                               : ((2U == (IData)(vlSelfRef.command))
                                   ? vlSelfRef.fpga_brain_stem__DOT__neural_output
                                   : ((3U == (IData)(vlSelfRef.command))
                                       ? vlSelfRef.fpga_brain_stem__DOT__eprom__DOT__memory
                                      [(0x00001fffU 
                                        & vlSelfRef.data_in)]
                                       : ((4U == (IData)(vlSelfRef.command))
                                           ? vlSelfRef.fpga_brain_stem__DOT__eeprom__DOT__memory
                                          [(0x000007ffU 
                                            & vlSelfRef.data_in)]
                                           : 0U))));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = vlSelfRef.fpga_brain_stem__DOT__neural__DOT__bias;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & vlSelfRef.data_in) 
                  * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [0U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & (vlSelfRef.data_in 
                                  >> 4U)) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [1U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & (vlSelfRef.data_in 
                                  >> 8U)) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [2U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & (vlSelfRef.data_in 
                                  >> 0x0cU)) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [3U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & (vlSelfRef.data_in 
                                  >> 0x10U)) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [4U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & (vlSelfRef.data_in 
                                  >> 0x14U)) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [5U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((0x0000000fU & (vlSelfRef.data_in 
                                  >> 0x18U)) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [6U]));
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
            = (vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum 
               + ((vlSelfRef.data_in >> 0x1cU) * vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights
                  [7U]));
        vlSelfRef.fpga_brain_stem__DOT__neural_output 
            = ((0U < vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum)
                ? vlSelfRef.fpga_brain_stem__DOT__neural__DOT__sum
                : 0U);
    } else {
        __Vdly__fpga_brain_stem__DOT__pwm_counter = 0U;
        vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter = 0U;
        __Vdly__fpga_brain_stem__DOT__spi__DOT__clk_div = 0U;
        vlSelfRef.spi_sck = 0U;
        vlSelfRef.sdr_tx = 0U;
        __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count = 0U;
        __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active = 0U;
        __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg = 0U;
        __Vdly__fpga_brain_stem__DOT__spi__DOT__state = 0U;
        vlSelfRef.spi_ss_n = 0xffU;
        vlSelfRef.spi_mosi = 0U;
        __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data = 0U;
        __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count = 0U;
        vlSelfRef.fpga_brain_stem__DOT__spi__DOT__slave_select = 0U;
        vlSelfRef.data_out = 0U;
        vlSelfRef.fpga_brain_stem__DOT__neural_output = 0U;
    }
    if ((1U & (~ (IData)(vlSelfRef.reset_n)))) {
        __VdlySet__fpga_brain_stem__DOT__neural__DOT__weights__v0 = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__bias = 0U;
    }
    vlSelfRef.ready = ((IData)(vlSelfRef.reset_n) && 
                       ((1U == (IData)(vlSelfRef.command)) 
                        || ((2U == (IData)(vlSelfRef.command)) 
                            || ((3U == (IData)(vlSelfRef.command)) 
                                || (4U == (IData)(vlSelfRef.command))))));
    vlSelfRef.fpga_brain_stem__DOT__pwm_counter = __Vdly__fpga_brain_stem__DOT__pwm_counter;
    vlSelfRef.fpga_brain_stem__DOT__spi__DOT__clk_div 
        = __Vdly__fpga_brain_stem__DOT__spi__DOT__clk_div;
    vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg 
        = __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg;
    vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_active 
        = __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_active;
    vlSelfRef.fpga_brain_stem__DOT__sdr__DOT__tx_bit_count 
        = __Vdly__fpga_brain_stem__DOT__sdr__DOT__tx_bit_count;
    vlSelfRef.fpga_brain_stem__DOT__spi__DOT__tx_data 
        = __Vdly__fpga_brain_stem__DOT__spi__DOT__tx_data;
    vlSelfRef.fpga_brain_stem__DOT__spi__DOT__bit_count 
        = __Vdly__fpga_brain_stem__DOT__spi__DOT__bit_count;
    vlSelfRef.fpga_brain_stem__DOT__spi__DOT__state 
        = __Vdly__fpga_brain_stem__DOT__spi__DOT__state;
    vlSelfRef.pwm_out = ((((((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                               < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                               [0x0fU]) << 3U) | (((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                   < 
                                                   vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                   [0x0eU]) 
                                                  << 2U)) 
                            | ((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                 < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                 [0x0dU]) << 1U) | 
                               ((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                [0x0cU]))) << 0x0000000cU) 
                          | ((((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                 < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                 [0x0bU]) << 3U) | 
                               (((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                 < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                 [0x0aU]) << 2U)) | 
                              ((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                 < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                 [9U]) << 1U) | ((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                 < 
                                                 vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                 [8U]))) 
                             << 8U)) | (((((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                             < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                             [7U]) 
                                            << 3U) 
                                           | (((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                               < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                               [6U]) 
                                              << 2U)) 
                                          | ((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                               < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                               [5U]) 
                                              << 1U) 
                                             | ((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                < vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                [4U]))) 
                                         << 4U) | (
                                                   ((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                      < 
                                                      vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                      [3U]) 
                                                     << 3U) 
                                                    | (((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                        < 
                                                        vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                        [2U]) 
                                                       << 2U)) 
                                                   | ((((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                        < 
                                                        vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                        [1U]) 
                                                       << 1U) 
                                                      | ((IData)(vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter) 
                                                         < 
                                                         vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle
                                                         [0U])))));
    if (__VdlySet__fpga_brain_stem__DOT__neural__DOT__weights__v0) {
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[0U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[1U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[2U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[3U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[4U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[5U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[6U] = 1U;
        vlSelfRef.fpga_brain_stem__DOT__neural__DOT__weights[7U] = 1U;
    }
}

void Vfpga_brain_stem___024root___nba_sequent__TOP__1(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___nba_sequent__TOP__1\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*3:0*/ __Vdly__fpga_brain_stem__DOT__jtag__DOT__state;
    __Vdly__fpga_brain_stem__DOT__jtag__DOT__state = 0;
    // Body
    __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
        = vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state;
    if (vlSelfRef.jtag_tms) {
        if ((8U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
            if ((4U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
                __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                    = ((2U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                        ? ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                            ? ((IData)(vlSelfRef.jtag_tms)
                                ? 2U : 1U) : ((IData)(vlSelfRef.jtag_tms)
                                               ? 0x0fU
                                               : 0x0bU))
                        : ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                            ? ((IData)(vlSelfRef.jtag_tms)
                                ? 0x0eU : 0x0dU) : 
                           ((IData)(vlSelfRef.jtag_tms)
                             ? 0x0fU : 0x0dU)));
            } else if ((2U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
                if ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
                    vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__ir 
                        = (((IData)(vlSelfRef.jtag_tdi) 
                            << 4U) | (0x0000000fU & 
                                      ((IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__ir) 
                                       >> 1U)));
                    __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                        = ((IData)(vlSelfRef.jtag_tms)
                            ? 0x0cU : 0x0bU);
                } else {
                    __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                        = ((IData)(vlSelfRef.jtag_tms)
                            ? 0x0cU : 0x0bU);
                }
            } else {
                __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                    = ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                        ? ((IData)(vlSelfRef.jtag_tms)
                            ? 0U : 0x0aU) : ((IData)(vlSelfRef.jtag_tms)
                                              ? 2U : 1U));
            }
        } else if ((4U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
            if ((2U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
                __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                    = ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                        ? ((IData)(vlSelfRef.jtag_tms)
                            ? 8U : 4U) : ((IData)(vlSelfRef.jtag_tms)
                                           ? 7U : 6U));
            } else if ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))) {
                __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                    = ((IData)(vlSelfRef.jtag_tms) ? 8U
                        : 6U);
            } else {
                vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__dr 
                    = (((IData)(vlSelfRef.jtag_tdi) 
                        << 0x0000001fU) | (vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__dr 
                                           >> 1U));
                __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                    = ((IData)(vlSelfRef.jtag_tms) ? 5U
                        : 4U);
            }
        } else {
            __Vdly__fpga_brain_stem__DOT__jtag__DOT__state 
                = ((2U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                    ? ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                        ? ((IData)(vlSelfRef.jtag_tms)
                            ? 5U : 4U) : ((IData)(vlSelfRef.jtag_tms)
                                           ? 9U : 3U))
                    : ((1U & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                        ? ((IData)(vlSelfRef.jtag_tms)
                            ? 2U : 1U) : ((IData)(vlSelfRef.jtag_tms)
                                           ? 0U : 1U)));
        }
    } else {
        __Vdly__fpga_brain_stem__DOT__jtag__DOT__state = 0U;
    }
    vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state 
        = __Vdly__fpga_brain_stem__DOT__jtag__DOT__state;
    vlSelfRef.jtag_tdo = (1U & ((4U == (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                                 ? vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__dr
                                 : ((0x0bU == (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state)) 
                                    & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__ir))));
}

void Vfpga_brain_stem___024root___eval_nba(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_nba\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((3ULL & vlSelfRef.__VnbaTriggered[0U])) {
        Vfpga_brain_stem___024root___nba_sequent__TOP__0(vlSelf);
    }
    if ((0x000000000000000cULL & vlSelfRef.__VnbaTriggered
         [0U])) {
        Vfpga_brain_stem___024root___nba_sequent__TOP__1(vlSelf);
    }
}

void Vfpga_brain_stem___024root___trigger_orInto__act(VlUnpacked<QData/*63:0*/, 1> &out, const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___trigger_orInto__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = (out[n] | in[n]);
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vfpga_brain_stem___024root___eval_phase__act(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_phase__act\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vfpga_brain_stem___024root___eval_triggers__act(vlSelf);
    Vfpga_brain_stem___024root___trigger_orInto__act(vlSelfRef.__VnbaTriggered, vlSelfRef.__VactTriggered);
    return (0U);
}

void Vfpga_brain_stem___024root___trigger_clear__act(VlUnpacked<QData/*63:0*/, 1> &out) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___trigger_clear__act\n"); );
    // Locals
    IData/*31:0*/ n;
    // Body
    n = 0U;
    do {
        out[n] = 0ULL;
        n = ((IData)(1U) + n);
    } while ((1U > n));
}

bool Vfpga_brain_stem___024root___eval_phase__nba(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_phase__nba\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VnbaExecute;
    // Body
    __VnbaExecute = Vfpga_brain_stem___024root___trigger_anySet__act(vlSelfRef.__VnbaTriggered);
    if (__VnbaExecute) {
        Vfpga_brain_stem___024root___eval_nba(vlSelf);
        Vfpga_brain_stem___024root___trigger_clear__act(vlSelfRef.__VnbaTriggered);
    }
    return (__VnbaExecute);
}

void Vfpga_brain_stem___024root___eval(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VnbaIterCount;
    // Body
    __VnbaIterCount = 0U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VnbaIterCount)))) {
#ifdef VL_DEBUG
            Vfpga_brain_stem___024root___dump_triggers__act(vlSelfRef.__VnbaTriggered, "nba"s);
#endif
            VL_FATAL_MT("fpga_brain_stem.v", 3, "", "NBA region did not converge after 100 tries");
        }
        __VnbaIterCount = ((IData)(1U) + __VnbaIterCount);
        vlSelfRef.__VactIterCount = 0U;
        do {
            if (VL_UNLIKELY(((0x00000064U < vlSelfRef.__VactIterCount)))) {
#ifdef VL_DEBUG
                Vfpga_brain_stem___024root___dump_triggers__act(vlSelfRef.__VactTriggered, "act"s);
#endif
                VL_FATAL_MT("fpga_brain_stem.v", 3, "", "Active region did not converge after 100 tries");
            }
            vlSelfRef.__VactIterCount = ((IData)(1U) 
                                         + vlSelfRef.__VactIterCount);
        } while (Vfpga_brain_stem___024root___eval_phase__act(vlSelf));
    } while (Vfpga_brain_stem___024root___eval_phase__nba(vlSelf));
}

#ifdef VL_DEBUG
void Vfpga_brain_stem___024root___eval_debug_assertions(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_debug_assertions\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if (VL_UNLIKELY(((vlSelfRef.clk & 0xfeU)))) {
        Verilated::overWidthError("clk");
    }
    if (VL_UNLIKELY(((vlSelfRef.reset_n & 0xfeU)))) {
        Verilated::overWidthError("reset_n");
    }
    if (VL_UNLIKELY(((vlSelfRef.spi_miso & 0xfeU)))) {
        Verilated::overWidthError("spi_miso");
    }
    if (VL_UNLIKELY(((vlSelfRef.jtag_tck & 0xfeU)))) {
        Verilated::overWidthError("jtag_tck");
    }
    if (VL_UNLIKELY(((vlSelfRef.jtag_tms & 0xfeU)))) {
        Verilated::overWidthError("jtag_tms");
    }
    if (VL_UNLIKELY(((vlSelfRef.jtag_tdi & 0xfeU)))) {
        Verilated::overWidthError("jtag_tdi");
    }
    if (VL_UNLIKELY(((vlSelfRef.sdr_rx & 0xfeU)))) {
        Verilated::overWidthError("sdr_rx");
    }
}
#endif  // VL_DEBUG
