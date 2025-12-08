// Verilated -*- C++ -*-
// DESCRIPTION: Verilator output: Design implementation internals
// See Vfpga_brain_stem.h for the primary calling header

#include "Vfpga_brain_stem__pch.h"

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_static(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_static\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__Vtrigprevexpr___TOP__clk__0 = vlSelfRef.clk;
    vlSelfRef.__Vtrigprevexpr___TOP__reset_n__0 = vlSelfRef.reset_n;
    vlSelfRef.__Vtrigprevexpr___TOP__jtag_tck__0 = vlSelfRef.jtag_tck;
    vlSelfRef.__Vtrigprevexpr___TOP__jtag_tms__0 = vlSelfRef.jtag_tms;
}

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_initial__TOP(Vfpga_brain_stem___024root* vlSelf);

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_initial(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_initial\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    Vfpga_brain_stem___024root___eval_initial__TOP(vlSelf);
}

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_initial__TOP(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_initial__TOP\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ fpga_brain_stem__DOT__eprom__DOT__i;
    fpga_brain_stem__DOT__eprom__DOT__i = 0;
    IData/*31:0*/ fpga_brain_stem__DOT__eeprom__DOT__i;
    fpga_brain_stem__DOT__eeprom__DOT__i = 0;
    // Body
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[1U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[2U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[3U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[4U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[5U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[6U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[7U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[8U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[9U] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0x0aU] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0x0bU] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0x0cU] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0x0dU] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0x0eU] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__duty_cycle[0x0fU] = 0x0800U;
    vlSelfRef.fpga_brain_stem__DOT__pwm__DOT__counter = 0U;
    fpga_brain_stem__DOT__eprom__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00002000U, fpga_brain_stem__DOT__eprom__DOT__i)) {
        vlSelfRef.fpga_brain_stem__DOT__eprom__DOT__memory[(0x00001fffU 
                                                            & fpga_brain_stem__DOT__eprom__DOT__i)] 
            = (0x0000ffffU & fpga_brain_stem__DOT__eprom__DOT__i);
        fpga_brain_stem__DOT__eprom__DOT__i = ((IData)(1U) 
                                               + fpga_brain_stem__DOT__eprom__DOT__i);
    }
    fpga_brain_stem__DOT__eeprom__DOT__i = 0U;
    while (VL_GTS_III(32, 0x00000800U, fpga_brain_stem__DOT__eeprom__DOT__i)) {
        vlSelfRef.fpga_brain_stem__DOT__eeprom__DOT__memory[(0x000007ffU 
                                                             & fpga_brain_stem__DOT__eeprom__DOT__i)] = 0U;
        fpga_brain_stem__DOT__eeprom__DOT__i = ((IData)(1U) 
                                                + fpga_brain_stem__DOT__eeprom__DOT__i);
    }
}

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_final(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_final\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
}

#ifdef VL_DEBUG
VL_ATTR_COLD void Vfpga_brain_stem___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag);
#endif  // VL_DEBUG
VL_ATTR_COLD bool Vfpga_brain_stem___024root___eval_phase__stl(Vfpga_brain_stem___024root* vlSelf);

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_settle(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_settle\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    IData/*31:0*/ __VstlIterCount;
    // Body
    __VstlIterCount = 0U;
    vlSelfRef.__VstlFirstIteration = 1U;
    do {
        if (VL_UNLIKELY(((0x00000064U < __VstlIterCount)))) {
#ifdef VL_DEBUG
            Vfpga_brain_stem___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
#endif
            VL_FATAL_MT("fpga_brain_stem.v", 3, "", "Settle region did not converge after 100 tries");
        }
        __VstlIterCount = ((IData)(1U) + __VstlIterCount);
    } while (Vfpga_brain_stem___024root___eval_phase__stl(vlSelf));
}

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_triggers__stl(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_triggers__stl\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    vlSelfRef.__VstlTriggered[0U] = ((0xfffffffffffffffeULL 
                                      & vlSelfRef.__VstlTriggered
                                      [0U]) | (IData)((IData)(vlSelfRef.__VstlFirstIteration)));
    vlSelfRef.__VstlFirstIteration = 0U;
#ifdef VL_DEBUG
    if (VL_UNLIKELY(vlSymsp->_vm_contextp__->debug())) {
        Vfpga_brain_stem___024root___dump_triggers__stl(vlSelfRef.__VstlTriggered, "stl"s);
    }
#endif
}

VL_ATTR_COLD bool Vfpga_brain_stem___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vfpga_brain_stem___024root___dump_triggers__stl(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___dump_triggers__stl\n"); );
    // Body
    if ((1U & (~ (IData)(Vfpga_brain_stem___024root___trigger_anySet__stl(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: Internal 'stl' trigger - first iteration\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD bool Vfpga_brain_stem___024root___trigger_anySet__stl(const VlUnpacked<QData/*63:0*/, 1> &in) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___trigger_anySet__stl\n"); );
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

VL_ATTR_COLD void Vfpga_brain_stem___024root___stl_sequent__TOP__0(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___stl_sequent__TOP__0\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
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
    vlSelfRef.jtag_tdo = (1U & ((4U == (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state))
                                 ? vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__dr
                                 : ((0x0bU == (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__state)) 
                                    & (IData)(vlSelfRef.fpga_brain_stem__DOT__jtag__DOT__ir))));
}

VL_ATTR_COLD void Vfpga_brain_stem___024root___eval_stl(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_stl\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    if ((1ULL & vlSelfRef.__VstlTriggered[0U])) {
        Vfpga_brain_stem___024root___stl_sequent__TOP__0(vlSelf);
    }
}

VL_ATTR_COLD bool Vfpga_brain_stem___024root___eval_phase__stl(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___eval_phase__stl\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Locals
    CData/*0:0*/ __VstlExecute;
    // Body
    Vfpga_brain_stem___024root___eval_triggers__stl(vlSelf);
    __VstlExecute = Vfpga_brain_stem___024root___trigger_anySet__stl(vlSelfRef.__VstlTriggered);
    if (__VstlExecute) {
        Vfpga_brain_stem___024root___eval_stl(vlSelf);
    }
    return (__VstlExecute);
}

bool Vfpga_brain_stem___024root___trigger_anySet__act(const VlUnpacked<QData/*63:0*/, 1> &in);

#ifdef VL_DEBUG
VL_ATTR_COLD void Vfpga_brain_stem___024root___dump_triggers__act(const VlUnpacked<QData/*63:0*/, 1> &triggers, const std::string &tag) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___dump_triggers__act\n"); );
    // Body
    if ((1U & (~ (IData)(Vfpga_brain_stem___024root___trigger_anySet__act(triggers))))) {
        VL_DBG_MSGS("         No '" + tag + "' region triggers active\n");
    }
    if ((1U & (IData)(triggers[0U]))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 0 is active: @(posedge clk)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 1U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 1 is active: @(negedge reset_n)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 2U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 2 is active: @(posedge jtag_tck)\n");
    }
    if ((1U & (IData)((triggers[0U] >> 3U)))) {
        VL_DBG_MSGS("         '" + tag + "' region trigger index 3 is active: @(negedge jtag_tms)\n");
    }
}
#endif  // VL_DEBUG

VL_ATTR_COLD void Vfpga_brain_stem___024root___ctor_var_reset(Vfpga_brain_stem___024root* vlSelf) {
    VL_DEBUG_IF(VL_DBG_MSGF("+    Vfpga_brain_stem___024root___ctor_var_reset\n"); );
    Vfpga_brain_stem__Syms* const __restrict vlSymsp VL_ATTR_UNUSED = vlSelf->vlSymsp;
    auto& vlSelfRef = std::ref(*vlSelf).get();
    // Body
    const uint64_t __VscopeHash = VL_MURMUR64_HASH(vlSelf->name());
    vlSelf->clk = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16707436170211756652ull);
    vlSelf->reset_n = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 14129604614540204776ull);
    vlSelf->command = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 13453452394900071627ull);
    vlSelf->data_in = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10574596302020702150ull);
    vlSelf->data_out = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11675680895196038875ull);
    vlSelf->ready = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 898948264233693212ull);
    vlSelf->pwm_out = VL_SCOPED_RAND_RESET_I(16, __VscopeHash, 17193619615457380819ull);
    vlSelf->spi_sck = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7598659639805510901ull);
    vlSelf->spi_ss_n = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 7410407827027220975ull);
    vlSelf->spi_mosi = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 852284730959930751ull);
    vlSelf->spi_miso = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 12140560756394917646ull);
    vlSelf->jtag_tck = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 10500983681776930247ull);
    vlSelf->jtag_tms = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 16224335879666074583ull);
    vlSelf->jtag_tdi = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5289790260552907825ull);
    vlSelf->jtag_tdo = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 293125711922884863ull);
    vlSelf->sdr_tx = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 1285470776080645086ull);
    vlSelf->sdr_rx = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9528084123955541716ull);
    vlSelf->fpga_brain_stem__DOT__pwm_counter = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 55309411285384867ull);
    vlSelf->fpga_brain_stem__DOT__neural_output = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 11351888778742068480ull);
    for (int __Vi0 = 0; __Vi0 < 8; ++__Vi0) {
        vlSelf->fpga_brain_stem__DOT__neural__DOT__weights[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 8336842652329673100ull);
    }
    vlSelf->fpga_brain_stem__DOT__neural__DOT__bias = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 1715878080071686506ull);
    vlSelf->fpga_brain_stem__DOT__neural__DOT__sum = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 2242217292962930618ull);
    for (int __Vi0 = 0; __Vi0 < 16; ++__Vi0) {
        vlSelf->fpga_brain_stem__DOT__pwm__DOT__duty_cycle[__Vi0] = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 5154311289812975177ull);
    }
    vlSelf->fpga_brain_stem__DOT__pwm__DOT__counter = VL_SCOPED_RAND_RESET_I(12, __VscopeHash, 17383057506735121210ull);
    vlSelf->fpga_brain_stem__DOT__spi__DOT__state = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9391715793647450240ull);
    vlSelf->fpga_brain_stem__DOT__spi__DOT__tx_data = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 762823113108809736ull);
    vlSelf->fpga_brain_stem__DOT__spi__DOT__bit_count = VL_SCOPED_RAND_RESET_I(3, __VscopeHash, 9160361746645358917ull);
    vlSelf->fpga_brain_stem__DOT__spi__DOT__slave_select = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 9735064387784907757ull);
    vlSelf->fpga_brain_stem__DOT__spi__DOT__clk_div = VL_SCOPED_RAND_RESET_I(2, __VscopeHash, 10178964697199416655ull);
    vlSelf->fpga_brain_stem__DOT__jtag__DOT__state = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 4627711013729516596ull);
    vlSelf->fpga_brain_stem__DOT__jtag__DOT__dr = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 10222707205520063619ull);
    vlSelf->fpga_brain_stem__DOT__jtag__DOT__ir = VL_SCOPED_RAND_RESET_I(5, __VscopeHash, 7049436332834561177ull);
    vlSelf->fpga_brain_stem__DOT__sdr__DOT__tx_bit_count = VL_SCOPED_RAND_RESET_I(4, __VscopeHash, 17423848837304148897ull);
    vlSelf->fpga_brain_stem__DOT__sdr__DOT__tx_shift_reg = VL_SCOPED_RAND_RESET_I(8, __VscopeHash, 1168188938474756762ull);
    vlSelf->fpga_brain_stem__DOT__sdr__DOT__tx_active = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 5453175898709876750ull);
    for (int __Vi0 = 0; __Vi0 < 8192; ++__Vi0) {
        vlSelf->fpga_brain_stem__DOT__eprom__DOT__memory[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 3587825039453473674ull);
    }
    for (int __Vi0 = 0; __Vi0 < 2048; ++__Vi0) {
        vlSelf->fpga_brain_stem__DOT__eeprom__DOT__memory[__Vi0] = VL_SCOPED_RAND_RESET_I(32, __VscopeHash, 15280764540217606146ull);
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VstlTriggered[__Vi0] = 0;
    }
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VactTriggered[__Vi0] = 0;
    }
    vlSelf->__Vtrigprevexpr___TOP__clk__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 9526919608049418986ull);
    vlSelf->__Vtrigprevexpr___TOP__reset_n__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 13318404360585350920ull);
    vlSelf->__Vtrigprevexpr___TOP__jtag_tck__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 7802969833557952973ull);
    vlSelf->__Vtrigprevexpr___TOP__jtag_tms__0 = VL_SCOPED_RAND_RESET_I(1, __VscopeHash, 8855904465262179287ull);
    for (int __Vi0 = 0; __Vi0 < 1; ++__Vi0) {
        vlSelf->__VnbaTriggered[__Vi0] = 0;
    }
}
