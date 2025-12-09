	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 26, 0	sdk_version 26, 1
	.globl	_emit_symbolic_thought          ; -- Begin function emit_symbolic_thought
	.p2align	2
_emit_symbolic_thought:                 ; @emit_symbolic_thought
	.cfi_startproc
; %bb.0:
	sub	sp, sp, #384
	stp	x24, x23, [sp, #320]            ; 16-byte Folded Spill
	stp	x22, x21, [sp, #336]            ; 16-byte Folded Spill
	stp	x20, x19, [sp, #352]            ; 16-byte Folded Spill
	stp	x29, x30, [sp, #368]            ; 16-byte Folded Spill
	add	x29, sp, #368
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
Lloh0:
	adrp	x8, ___stack_chk_guard@GOTPAGE
Lloh1:
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
Lloh2:
	ldr	x8, [x8]
	stur	x8, [x29, #-56]
	mov	w8, #34079                      ; =0x851f
	movk	w8, #20971, lsl #16
	smull	x8, w0, w8
	lsr	x9, x8, #63
	asr	x8, x8, #38
	add	w8, w8, w9
	mov	w9, #200                        ; =0xc8
	msub	w8, w8, w9, w0
	fmov	d3, #0.50000000
	fcmp	d0, d3
	ccmp	w8, #0, #4, le
	b.ne	LBB0_20
; %bb.1:
	mov	w8, #52429                      ; =0xcccd
	movk	w8, #52428, lsl #16
	mov	w9, #39320                      ; =0x9998
	movk	w9, #6553, lsl #16
	madd	w8, w0, w8, w9
	ror	w8, w8, #2
	mov	w9, #52429                      ; =0xcccd
	movk	w9, #3276, lsl #16
	cmp	w8, w9
	fccmp	d0, d3, #4, hs
	b.gt	LBB0_20
; %bb.2:
	mov	x8, #4632233691727265792        ; =0x4049000000000000
	fmov	d3, x8
	fcmp	d1, d3
	cset	w8, gt
	mov	x9, #-7378697629483820647       ; =0x9999999999999999
	movk	x9, #39322
	movk	x9, #16297, lsl #48
	fmov	d3, x9
	fcmp	d2, d3
	mov	w9, #2                          ; =0x2
	csel	w8, w9, w8, gt
	cmp	w8, #1
	b.eq	LBB0_6
; %bb.3:
	cbnz	w8, LBB0_7
; %bb.4:
	fmov	d3, #0.50000000
	fcmp	d0, d3
	b.le	LBB0_8
; %bb.5:
Lloh3:
	adrp	x8, l_.str.4@PAGE
Lloh4:
	add	x8, x8, l_.str.4@PAGEOFF
	ldr	q0, [x8]
	str	q0, [sp, #48]
	ldur	q0, [x8, #9]
	stur	q0, [sp, #57]
Lloh5:
	adrp	x8, l_.str.3@PAGE
Lloh6:
	add	x8, x8, l_.str.3@PAGEOFF
Lloh7:
	adrp	x9, l_.str.2@PAGE
Lloh8:
	add	x9, x9, l_.str.2@PAGEOFF
	b	LBB0_19
LBB0_6:
	bl	_rand
	mov	w8, #26215                      ; =0x6667
	movk	w8, #26214, lsl #16
	smull	x8, w0, w8
	lsr	x9, x8, #32
	lsr	x8, x8, #63
	add	w8, w8, w9, asr #1
	add	w8, w8, w8, lsl #2
	sub	w8, w0, w8
Lloh9:
	adrp	x9, l___const.emit_symbolic_thought.ops@PAGE
Lloh10:
	add	x9, x9, l___const.emit_symbolic_thought.ops@PAGEOFF
	ldr	x20, [x9, w8, sxtw #3]
	bl	_rand
	mov	x19, x0
	bl	_rand
	mov	w21, #32897                     ; =0x8081
	movk	w21, #32896, lsl #16
	smull	x8, w0, w21
	lsr	x8, x8, #32
	add	w8, w8, w0
	asr	w9, w8, #7
	add	w8, w9, w8, lsr #31
	sub	w8, w8, w8, lsl #8
	add	w22, w0, w8
	bl	_rand
	smull	x8, w0, w21
	lsr	x8, x8, #32
	add	w8, w8, w0
	asr	w9, w8, #7
	add	w8, w9, w8, lsr #31
	sub	w8, w8, w8, lsl #8
	add	w23, w0, w8
	bl	_rand
	smull	x8, w0, w21
	lsr	x8, x8, #32
	add	w8, w8, w0
	asr	w9, w8, #7
	add	w8, w9, w8, lsr #31
	sub	w8, w8, w8, lsl #8
	add	w8, w0, w8
	stp	x20, x19, [sp]
	stp	x22, x23, [sp, #16]
	str	x8, [sp, #32]
Lloh11:
	adrp	x2, l_.str.29@PAGE
Lloh12:
	add	x2, x2, l_.str.29@PAGEOFF
	add	x0, sp, #48
	mov	w1, #256                        ; =0x100
	bl	_snprintf
Lloh13:
	adrp	x8, l_.str.23@PAGE
Lloh14:
	add	x8, x8, l_.str.23@PAGEOFF
Lloh15:
	adrp	x9, l_.str.22@PAGE
Lloh16:
	add	x9, x9, l_.str.22@PAGEOFF
	b	LBB0_19
LBB0_7:
Lloh17:
	adrp	x8, l_.str.32@PAGE
Lloh18:
	add	x8, x8, l_.str.32@PAGEOFF
	ldp	q0, q1, [x8]
	stp	q0, q1, [sp, #48]
	ldr	q0, [x8, #32]
	str	q0, [sp, #80]
	ldur	x8, [x8, #45]
	stur	x8, [sp, #93]
Lloh19:
	adrp	x8, l_.str.31@PAGE
Lloh20:
	add	x8, x8, l_.str.31@PAGEOFF
Lloh21:
	adrp	x9, l_.str.30@PAGE
Lloh22:
	add	x9, x9, l_.str.30@PAGEOFF
	b	LBB0_19
LBB0_8:
	cmp	w3, #501
	b.lt	LBB0_10
; %bb.9:
	strb	wzr, [sp, #80]
Lloh23:
	adrp	x8, l_.str.7@PAGE
Lloh24:
	add	x8, x8, l_.str.7@PAGEOFF
	ldp	q0, q1, [x8]
	stp	q0, q1, [sp, #48]
Lloh25:
	adrp	x8, l_.str.6@PAGE
Lloh26:
	add	x8, x8, l_.str.6@PAGEOFF
Lloh27:
	adrp	x9, l_.str.5@PAGE
Lloh28:
	add	x9, x9, l_.str.5@PAGEOFF
	b	LBB0_19
LBB0_10:
	cbz	w1, LBB0_12
; %bb.11:
Lloh29:
	adrp	x8, l_.str.9@PAGE
Lloh30:
	add	x8, x8, l_.str.9@PAGEOFF
	ldr	q0, [x8]
	str	q0, [sp, #48]
	ldur	q0, [x8, #12]
	stur	q0, [sp, #60]
Lloh31:
	adrp	x8, l_.str.8@PAGE
Lloh32:
	add	x8, x8, l_.str.8@PAGEOFF
Lloh33:
	adrp	x9, l_.str.2@PAGE
Lloh34:
	add	x9, x9, l_.str.2@PAGEOFF
	b	LBB0_19
LBB0_12:
	mov	x8, #5243                       ; =0x147b
	movk	x8, #18350, lsl #16
	movk	x8, #31457, lsl #32
	movk	x8, #16260, lsl #48
	fmov	d0, x8
	fcmp	d2, d0
	b.le	LBB0_14
; %bb.13:
Lloh35:
	adrp	x8, l_.str.12@PAGE
Lloh36:
	add	x8, x8, l_.str.12@PAGEOFF
	ldr	q0, [x8]
	str	q0, [sp, #48]
	ldur	q0, [x8, #11]
	stur	q0, [sp, #59]
Lloh37:
	adrp	x8, l_.str.11@PAGE
Lloh38:
	add	x8, x8, l_.str.11@PAGEOFF
Lloh39:
	adrp	x9, l_.str.10@PAGE
Lloh40:
	add	x9, x9, l_.str.10@PAGEOFF
	b	LBB0_19
LBB0_14:
	fmov	d0, #30.00000000
	fcmp	d1, d0
	b.le	LBB0_16
; %bb.15:
Lloh41:
	adrp	x8, l_.str.15@PAGE
Lloh42:
	add	x8, x8, l_.str.15@PAGEOFF
	ldr	q0, [x8]
	str	q0, [sp, #48]
	ldur	q0, [x8, #13]
	stur	q0, [sp, #61]
Lloh43:
	adrp	x8, l_.str.14@PAGE
Lloh44:
	add	x8, x8, l_.str.14@PAGEOFF
Lloh45:
	adrp	x9, l_.str.13@PAGE
Lloh46:
	add	x9, x9, l_.str.13@PAGEOFF
	b	LBB0_19
LBB0_16:
	cbz	w2, LBB0_18
; %bb.17:
Lloh47:
	adrp	x8, l_.str.18@PAGE
Lloh48:
	add	x8, x8, l_.str.18@PAGEOFF
	ldr	q0, [x8]
	str	q0, [sp, #48]
	ldur	q0, [x8, #12]
	stur	q0, [sp, #60]
Lloh49:
	adrp	x8, l_.str.17@PAGE
Lloh50:
	add	x8, x8, l_.str.17@PAGEOFF
Lloh51:
	adrp	x9, l_.str.16@PAGE
Lloh52:
	add	x9, x9, l_.str.16@PAGEOFF
	b	LBB0_19
LBB0_18:
Lloh53:
	adrp	x8, l_.str.21@PAGE
Lloh54:
	add	x8, x8, l_.str.21@PAGEOFF
	ldr	q0, [x8]
	str	q0, [sp, #48]
	ldur	q0, [x8, #10]
	stur	q0, [sp, #58]
Lloh55:
	adrp	x8, l_.str.20@PAGE
Lloh56:
	add	x8, x8, l_.str.20@PAGEOFF
Lloh57:
	adrp	x9, l_.str.19@PAGE
Lloh58:
	add	x9, x9, l_.str.19@PAGEOFF
LBB0_19:
Lloh59:
	adrp	x19, ___stderrp@GOTPAGE
Lloh60:
	ldr	x19, [x19, ___stderrp@GOTPAGEOFF]
	ldr	x0, [x19]
	add	x10, sp, #48
	stp	x8, x10, [sp, #8]
	str	x9, [sp]
Lloh61:
	adrp	x1, l_.str.33@PAGE
Lloh62:
	add	x1, x1, l_.str.33@PAGEOFF
	bl	_fprintf
	ldr	x0, [x19]
	bl	_fflush
LBB0_20:
	ldur	x8, [x29, #-56]
Lloh63:
	adrp	x9, ___stack_chk_guard@GOTPAGE
Lloh64:
	ldr	x9, [x9, ___stack_chk_guard@GOTPAGEOFF]
Lloh65:
	ldr	x9, [x9]
	cmp	x9, x8
	b.ne	LBB0_22
; %bb.21:
	ldp	x29, x30, [sp, #368]            ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #352]            ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #336]            ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #320]            ; 16-byte Folded Reload
	add	sp, sp, #384
	ret
LBB0_22:
	bl	___stack_chk_fail
	.loh AdrpLdrGotLdr	Lloh0, Lloh1, Lloh2
	.loh AdrpAdd	Lloh7, Lloh8
	.loh AdrpAdd	Lloh5, Lloh6
	.loh AdrpAdd	Lloh3, Lloh4
	.loh AdrpAdd	Lloh15, Lloh16
	.loh AdrpAdd	Lloh13, Lloh14
	.loh AdrpAdd	Lloh11, Lloh12
	.loh AdrpAdd	Lloh9, Lloh10
	.loh AdrpAdd	Lloh21, Lloh22
	.loh AdrpAdd	Lloh19, Lloh20
	.loh AdrpAdd	Lloh17, Lloh18
	.loh AdrpAdd	Lloh27, Lloh28
	.loh AdrpAdd	Lloh25, Lloh26
	.loh AdrpAdd	Lloh23, Lloh24
	.loh AdrpAdd	Lloh33, Lloh34
	.loh AdrpAdd	Lloh31, Lloh32
	.loh AdrpAdd	Lloh29, Lloh30
	.loh AdrpAdd	Lloh39, Lloh40
	.loh AdrpAdd	Lloh37, Lloh38
	.loh AdrpAdd	Lloh35, Lloh36
	.loh AdrpAdd	Lloh45, Lloh46
	.loh AdrpAdd	Lloh43, Lloh44
	.loh AdrpAdd	Lloh41, Lloh42
	.loh AdrpAdd	Lloh51, Lloh52
	.loh AdrpAdd	Lloh49, Lloh50
	.loh AdrpAdd	Lloh47, Lloh48
	.loh AdrpAdd	Lloh57, Lloh58
	.loh AdrpAdd	Lloh55, Lloh56
	.loh AdrpAdd	Lloh53, Lloh54
	.loh AdrpAdd	Lloh61, Lloh62
	.loh AdrpLdrGot	Lloh59, Lloh60
	.loh AdrpLdrGotLdr	Lloh63, Lloh64, Lloh65
	.cfi_endproc
                                        ; -- End function
	.globl	_render_oled_visualization      ; -- Begin function render_oled_visualization
	.p2align	2
_render_oled_visualization:             ; @render_oled_visualization
	.cfi_startproc
; %bb.0:
	stp	d11, d10, [sp, #-128]!          ; 16-byte Folded Spill
	stp	d9, d8, [sp, #16]               ; 16-byte Folded Spill
	stp	x28, x27, [sp, #32]             ; 16-byte Folded Spill
	stp	x26, x25, [sp, #48]             ; 16-byte Folded Spill
	stp	x24, x23, [sp, #64]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #80]             ; 16-byte Folded Spill
	stp	x20, x19, [sp, #96]             ; 16-byte Folded Spill
	stp	x29, x30, [sp, #112]            ; 16-byte Folded Spill
	add	x29, sp, #112
	mov	w9, #16400                      ; =0x4010
Lloh66:
	adrp	x16, ___chkstk_darwin@GOTPAGE
Lloh67:
	ldr	x16, [x16, ___chkstk_darwin@GOTPAGEOFF]
	blr	x16
	sub	sp, sp, #4, lsl #12             ; =16384
	sub	sp, sp, #16
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	.cfi_offset w27, -88
	.cfi_offset w28, -96
	.cfi_offset b8, -104
	.cfi_offset b9, -112
	.cfi_offset b10, -120
	.cfi_offset b11, -128
	mov	x20, x1
	mov	x19, x0
Lloh68:
	adrp	x8, ___stack_chk_guard@GOTPAGE
Lloh69:
	ldr	x8, [x8, ___stack_chk_guard@GOTPAGEOFF]
Lloh70:
	ldr	x8, [x8]
	stur	x8, [x29, #-128]
	mov	x0, sp
	mov	w1, #16384                      ; =0x4000
	bl	_bzero
	cmp	w20, #1
	b.lt	LBB1_7
; %bb.1:
	mov	w8, w20
	add	x9, x19, #24
	mov	x10, #225833675390976           ; =0xcd6500000000
	movk	x10, #49613, lsl #48
	fmov	d2, x10
	mov	x10, #225833675390976           ; =0xcd6500000000
	movk	x10, #16845, lsl #48
	fmov	d0, x10
	mov	x10, x8
	fmov	d1, d0
	fmov	d3, d2
LBB1_2:                                 ; =>This Inner Loop Header: Depth=1
	ldur	d4, [x9, #-16]
	ldr	d5, [x9], #32
	fcmp	d4, d0
	fcsel	d0, d4, d0, mi
	fcmp	d4, d2
	fcsel	d2, d4, d2, gt
	fcmp	d5, d1
	fcsel	d1, d5, d1, mi
	fcmp	d5, d3
	fcsel	d3, d5, d3, gt
	subs	x10, x10, #1
	b.ne	LBB1_2
; %bb.3:
	fsub	d2, d2, d0
	fsub	d3, d3, d1
	add	x9, x19, #24
	mov	x10, #140737488355328           ; =0x800000000000
	movk	x10, #16463, lsl #48
	fmov	d4, x10
	fmov	d5, #31.00000000
	mov	w10, #31                        ; =0x1f
	mov	x11, sp
	fmov	d6, #1.00000000
	b	LBB1_5
LBB1_4:                                 ;   in Loop: Header=BB1_5 Depth=1
	add	x9, x9, #32
	subs	x8, x8, #1
	b.eq	LBB1_7
LBB1_5:                                 ; =>This Inner Loop Header: Depth=1
	ldur	d7, [x9, #-16]
	ldr	d16, [x9]
	fsub	d7, d7, d0
	fdiv	d7, d7, d2
	fmul	d7, d7, d4
	fcvtzs	w12, d7
	fsub	d7, d16, d1
	fdiv	d7, d7, d3
	fmul	d7, d7, d5
	fcvtzs	w13, d7
	cmp	w12, #63
	ccmp	w13, #31, #2, ls
	b.hi	LBB1_4
; %bb.6:                                ;   in Loop: Header=BB1_5 Depth=1
	sub	w13, w10, w13
	add	x13, x11, x13, lsl #9
	ldr	d7, [x13, w12, uxtw #3]
	fadd	d7, d7, d6
	str	d7, [x13, w12, uxtw #3]
	b	LBB1_4
LBB1_7:
Lloh71:
	adrp	x26, ___stderrp@GOTPAGE
Lloh72:
	ldr	x26, [x26, ___stderrp@GOTPAGEOFF]
	ldr	x3, [x26]
Lloh73:
	adrp	x0, l_.str.34@PAGE
Lloh74:
	add	x0, x0, l_.str.34@PAGEOFF
	mov	w1, #50                         ; =0x32
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	ldr	x3, [x26]
Lloh75:
	adrp	x0, l_.str.35@PAGE
Lloh76:
	add	x0, x0, l_.str.35@PAGEOFF
	mov	w1, #4                          ; =0x4
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	mov	w19, #64                        ; =0x40
LBB1_8:                                 ; =>This Inner Loop Header: Depth=1
	ldr	x1, [x26]
	mov	w0, #45                         ; =0x2d
	bl	_fputc
	subs	w19, w19, #1
	b.ne	LBB1_8
; %bb.9:
	ldr	x3, [x26]
Lloh77:
	adrp	x0, l_.str.37@PAGE
Lloh78:
	add	x0, x0, l_.str.37@PAGEOFF
	mov	w1, #2                          ; =0x2
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	mov	x27, #0                         ; =0x0
	mov	x28, sp
Lloh79:
	adrp	x19, l_.str.38@PAGE
Lloh80:
	add	x19, x19, l_.str.38@PAGEOFF
Lloh81:
	adrp	x20, l_.str.45@PAGE
Lloh82:
	add	x20, x20, l_.str.45@PAGEOFF
Lloh83:
	adrp	x21, l_.str.40@PAGE
Lloh84:
	add	x21, x21, l_.str.40@PAGEOFF
	fmov	d8, #2.00000000
	fmov	d9, #5.00000000
Lloh85:
	adrp	x22, l_.str.41@PAGE
Lloh86:
	add	x22, x22, l_.str.41@PAGEOFF
Lloh87:
	adrp	x23, l_.str.42@PAGE
Lloh88:
	add	x23, x23, l_.str.42@PAGEOFF
	fmov	d10, #10.00000000
	fmov	d11, #20.00000000
Lloh89:
	adrp	x25, l_.str.44@PAGE
Lloh90:
	add	x25, x25, l_.str.44@PAGEOFF
	b	LBB1_11
LBB1_10:                                ;   in Loop: Header=BB1_11 Depth=1
	ldr	x3, [x26]
	mov	x0, x20
	mov	w1, #2                          ; =0x2
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	add	x27, x27, #1
	add	x28, x28, #512
	cmp	x27, #32
	b.eq	LBB1_23
LBB1_11:                                ; =>This Loop Header: Depth=1
                                        ;     Child Loop BB1_13 Depth 2
	ldr	x3, [x26]
	mov	x0, x19
	mov	w1, #4                          ; =0x4
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	mov	x24, #0                         ; =0x0
	b	LBB1_13
LBB1_12:                                ;   in Loop: Header=BB1_13 Depth=2
	ldr	x1, [x26]
	mov	w0, #32                         ; =0x20
	bl	_fputc
	add	x24, x24, #8
	cmp	x24, #512
	b.eq	LBB1_10
LBB1_13:                                ;   Parent Loop BB1_11 Depth=1
                                        ; =>  This Inner Loop Header: Depth=2
	ldr	d0, [x28, x24]
	fcmp	d0, #0.0
	b.eq	LBB1_12
; %bb.14:                               ;   in Loop: Header=BB1_13 Depth=2
	fcmp	d0, d8
	b.pl	LBB1_16
; %bb.15:                               ;   in Loop: Header=BB1_13 Depth=2
	ldr	x3, [x26]
	mov	x0, x21
	mov	w1, #16                         ; =0x10
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	add	x24, x24, #8
	cmp	x24, #512
	b.ne	LBB1_13
	b	LBB1_10
LBB1_16:                                ;   in Loop: Header=BB1_13 Depth=2
	fcmp	d0, d9
	b.pl	LBB1_18
; %bb.17:                               ;   in Loop: Header=BB1_13 Depth=2
	ldr	x3, [x26]
	mov	x0, x22
	mov	w1, #16                         ; =0x10
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	add	x24, x24, #8
	cmp	x24, #512
	b.ne	LBB1_13
	b	LBB1_10
LBB1_18:                                ;   in Loop: Header=BB1_13 Depth=2
	fcmp	d0, d10
	b.pl	LBB1_20
; %bb.19:                               ;   in Loop: Header=BB1_13 Depth=2
	ldr	x3, [x26]
	mov	x0, x23
	mov	w1, #16                         ; =0x10
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	add	x24, x24, #8
	cmp	x24, #512
	b.ne	LBB1_13
	b	LBB1_10
LBB1_20:                                ;   in Loop: Header=BB1_13 Depth=2
	ldr	x3, [x26]
	fcmp	d0, d11
	b.pl	LBB1_22
; %bb.21:                               ;   in Loop: Header=BB1_13 Depth=2
Lloh91:
	adrp	x0, l_.str.43@PAGE
Lloh92:
	add	x0, x0, l_.str.43@PAGEOFF
	mov	w1, #16                         ; =0x10
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	add	x24, x24, #8
	cmp	x24, #512
	b.ne	LBB1_13
	b	LBB1_10
LBB1_22:                                ;   in Loop: Header=BB1_13 Depth=2
	mov	x0, x25
	mov	w1, #15                         ; =0xf
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	add	x24, x24, #8
	cmp	x24, #512
	b.ne	LBB1_13
	b	LBB1_10
LBB1_23:
	ldr	x3, [x26]
Lloh93:
	adrp	x0, l_.str.35@PAGE
Lloh94:
	add	x0, x0, l_.str.35@PAGEOFF
	mov	w1, #4                          ; =0x4
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	mov	w19, #64                        ; =0x40
LBB1_24:                                ; =>This Inner Loop Header: Depth=1
	ldr	x1, [x26]
	mov	w0, #45                         ; =0x2d
	bl	_fputc
	subs	w19, w19, #1
	b.ne	LBB1_24
; %bb.25:
	ldr	x3, [x26]
	ldur	x8, [x29, #-128]
Lloh95:
	adrp	x9, ___stack_chk_guard@GOTPAGE
Lloh96:
	ldr	x9, [x9, ___stack_chk_guard@GOTPAGEOFF]
Lloh97:
	ldr	x9, [x9]
	cmp	x9, x8
	b.ne	LBB1_27
; %bb.26:
Lloh98:
	adrp	x0, l_.str.37@PAGE
Lloh99:
	add	x0, x0, l_.str.37@PAGEOFF
	mov	w1, #2                          ; =0x2
	mov	w2, #1                          ; =0x1
	add	sp, sp, #4, lsl #12             ; =16384
	add	sp, sp, #16
	ldp	x29, x30, [sp, #112]            ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #96]             ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #80]             ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #64]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #48]             ; 16-byte Folded Reload
	ldp	x28, x27, [sp, #32]             ; 16-byte Folded Reload
	ldp	d9, d8, [sp, #16]               ; 16-byte Folded Reload
	ldp	d11, d10, [sp], #128            ; 16-byte Folded Reload
	b	_fwrite
LBB1_27:
	bl	___stack_chk_fail
	.loh AdrpLdrGotLdr	Lloh68, Lloh69, Lloh70
	.loh AdrpAdd	Lloh75, Lloh76
	.loh AdrpAdd	Lloh73, Lloh74
	.loh AdrpLdrGot	Lloh71, Lloh72
	.loh AdrpAdd	Lloh89, Lloh90
	.loh AdrpAdd	Lloh87, Lloh88
	.loh AdrpAdd	Lloh85, Lloh86
	.loh AdrpAdd	Lloh83, Lloh84
	.loh AdrpAdd	Lloh81, Lloh82
	.loh AdrpAdd	Lloh79, Lloh80
	.loh AdrpAdd	Lloh77, Lloh78
	.loh AdrpAdd	Lloh91, Lloh92
	.loh AdrpAdd	Lloh93, Lloh94
	.loh AdrpLdrGotLdr	Lloh95, Lloh96, Lloh97
	.loh AdrpAdd	Lloh98, Lloh99
	.loh AdrpLdrGot	Lloh66, Lloh67
	.cfi_endproc
                                        ; -- End function
	.globl	_generate_variance              ; -- Begin function generate_variance
	.p2align	2
_generate_variance:                     ; @generate_variance
	.cfi_startproc
; %bb.0:
	stp	d11, d10, [sp, #-48]!           ; 16-byte Folded Spill
	stp	d9, d8, [sp, #16]               ; 16-byte Folded Spill
	stp	x29, x30, [sp, #32]             ; 16-byte Folded Spill
	add	x29, sp, #32
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset b8, -24
	.cfi_offset b9, -32
	.cfi_offset b10, -40
	.cfi_offset b11, -48
	bl	_rand
	scvtf	d0, w0
	fmov	d9, #1.00000000
	fadd	d0, d0, d9
	mov	x8, #2097152                    ; =0x200000
	movk	x8, #16864, lsl #48
	fmov	d10, x8
	fdiv	d8, d0, d10
	bl	_rand
	scvtf	d0, w0
	fadd	d0, d0, d9
	fdiv	d9, d0, d10
	fmov	d0, d8
	bl	_log
	fmov	d1, #-2.00000000
	fmul	d0, d0, d1
	fsqrt	d1, d0
	mov	x8, #11544                      ; =0x2d18
	movk	x8, #21572, lsl #16
	movk	x8, #8699, lsl #32
	movk	x8, #16409, lsl #48
	fmov	d0, x8
	fmul	d0, d9, d0
	mov	x8, #5243                       ; =0x147b
	movk	x8, #18350, lsl #16
	movk	x8, #31457, lsl #32
	movk	x8, #16260, lsl #48
	fmov	d2, x8
	fmul	d8, d1, d2
	bl	_cos
	fmul	d0, d0, d8
	ldp	x29, x30, [sp, #32]             ; 16-byte Folded Reload
	ldp	d9, d8, [sp, #16]               ; 16-byte Folded Reload
	ldp	d11, d10, [sp], #48             ; 16-byte Folded Reload
	ret
	.cfi_endproc
                                        ; -- End function
	.globl	_main                           ; -- Begin function main
	.p2align	2
_main:                                  ; @main
	.cfi_startproc
; %bb.0:
	stp	d15, d14, [sp, #-160]!          ; 16-byte Folded Spill
	stp	d13, d12, [sp, #16]             ; 16-byte Folded Spill
	stp	d11, d10, [sp, #32]             ; 16-byte Folded Spill
	stp	d9, d8, [sp, #48]               ; 16-byte Folded Spill
	stp	x28, x27, [sp, #64]             ; 16-byte Folded Spill
	stp	x26, x25, [sp, #80]             ; 16-byte Folded Spill
	stp	x24, x23, [sp, #96]             ; 16-byte Folded Spill
	stp	x22, x21, [sp, #112]            ; 16-byte Folded Spill
	stp	x20, x19, [sp, #128]            ; 16-byte Folded Spill
	stp	x29, x30, [sp, #144]            ; 16-byte Folded Spill
	add	x29, sp, #144
	sub	sp, sp, #448
	.cfi_def_cfa w29, 16
	.cfi_offset w30, -8
	.cfi_offset w29, -16
	.cfi_offset w19, -24
	.cfi_offset w20, -32
	.cfi_offset w21, -40
	.cfi_offset w22, -48
	.cfi_offset w23, -56
	.cfi_offset w24, -64
	.cfi_offset w25, -72
	.cfi_offset w26, -80
	.cfi_offset w27, -88
	.cfi_offset w28, -96
	.cfi_offset b8, -104
	.cfi_offset b9, -112
	.cfi_offset b10, -120
	.cfi_offset b11, -128
	.cfi_offset b12, -136
	.cfi_offset b13, -144
	.cfi_offset b14, -152
	.cfi_offset b15, -160
	cmp	w0, #16
	b.ne	LBB3_5
; %bb.1:
	mov	x20, x1
	mov	x0, #0                          ; =0x0
	bl	_time
                                        ; kill: def $w0 killed $w0 killed $x0
	bl	_srand
	ldr	x0, [x20, #8]
	bl	_atof
	str	d0, [sp, #224]                  ; 8-byte Folded Spill
	ldr	x0, [x20, #16]
	bl	_atof
	fmov	d10, d0
	ldr	x0, [x20, #24]
	bl	_atoi
	str	w0, [sp, #244]                  ; 4-byte Folded Spill
	ldr	x0, [x20, #32]
	bl	_atoll
	mov	x28, x0
	ldr	x0, [x20, #40]
	bl	_atof
	str	d0, [sp, #264]                  ; 8-byte Folded Spill
	ldr	x0, [x20, #48]
	bl	_atof
	fmov	d12, d0
	ldr	x0, [x20, #56]
	bl	_atof
	fmov	d14, d0
	ldr	x0, [x20, #64]
	bl	_atof
	str	d0, [sp, #256]                  ; 8-byte Folded Spill
	ldr	x0, [x20, #72]
	bl	_atof
	str	d0, [sp, #248]                  ; 8-byte Folded Spill
	ldr	x0, [x20]
Lloh100:
	adrp	x1, l_.str.47@PAGE
Lloh101:
	add	x1, x1, l_.str.47@PAGEOFF
	bl	_fopen
	cbz	x0, LBB3_6
; %bb.2:
	mov	x22, x0
	mov	x1, #0                          ; =0x0
	mov	w2, #2                          ; =0x2
	bl	_fseek
	mov	x0, x22
	bl	_ftell
	mov	x19, x0
	mov	x0, x22
	mov	x1, #0                          ; =0x0
	mov	w2, #0                          ; =0x0
	bl	_fseek
	mov	x0, x19
	bl	_malloc
	mov	x23, x0
	cbz	x0, LBB3_4
; %bb.3:
	mov	x0, x23
	mov	w1, #1                          ; =0x1
	mov	x2, x19
	mov	x3, x22
	bl	_fread
Lloh102:
	adrp	x8, ___stderrp@GOTPAGE
Lloh103:
	ldr	x8, [x8, ___stderrp@GOTPAGEOFF]
Lloh104:
	ldr	x0, [x8]
	str	x19, [sp]
Lloh105:
	adrp	x1, l_.str.48@PAGE
Lloh106:
	add	x1, x1, l_.str.48@PAGEOFF
	bl	_fprintf
LBB3_4:
	mov	x0, x22
	bl	_fclose
	b	LBB3_7
LBB3_5:
Lloh107:
	adrp	x8, ___stderrp@GOTPAGE
Lloh108:
	ldr	x8, [x8, ___stderrp@GOTPAGEOFF]
Lloh109:
	ldr	x3, [x8]
Lloh110:
	adrp	x0, l_.str.46@PAGE
Lloh111:
	add	x0, x0, l_.str.46@PAGEOFF
	mov	w19, #1                         ; =0x1
	mov	w1, #178                        ; =0xb2
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	b	LBB3_66
LBB3_6:
	mov	x19, #0                         ; =0x0
	mov	x23, #0                         ; =0x0
LBB3_7:
	ldr	x0, [x20, #80]
	bl	_atof
	fmov	d9, d0
	ldr	x0, [x20, #88]
	bl	_atof
	fmov	d8, d0
	ldr	x0, [x20, #96]
	bl	_atof
	fmov	d11, d0
	ldr	x0, [x20, #104]
	bl	_atoi
	mov	x24, x0
	ldr	x0, [x20, #112]
	bl	_atof
	fmov	d13, d0
	ldr	x0, [x20, #120]
	bl	_atoi
	mov	x22, x0
	ldr	w8, [sp, #244]                  ; 4-byte Folded Reload
	scvtf	d0, w8
	str	d0, [sp, #232]                  ; 8-byte Folded Spill
	fmul	d0, d10, d0
	fcvtzs	w25, d0
Lloh112:
	adrp	x20, ___stderrp@GOTPAGE
Lloh113:
	ldr	x20, [x20, ___stderrp@GOTPAGEOFF]
	ldr	x0, [x20]
	str	x25, [sp]
Lloh114:
	adrp	x1, l_.str.49@PAGE
Lloh115:
	add	x1, x1, l_.str.49@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	x28, [sp]
Lloh116:
	adrp	x1, l_.str.50@PAGE
Lloh117:
	add	x1, x1, l_.str.50@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	ldr	d0, [sp, #264]                  ; 8-byte Folded Reload
	str	d0, [sp]
Lloh118:
	adrp	x1, l_.str.51@PAGE
Lloh119:
	add	x1, x1, l_.str.51@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	d12, [sp]
Lloh120:
	adrp	x1, l_.str.52@PAGE
Lloh121:
	add	x1, x1, l_.str.52@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	d14, [sp]
Lloh122:
	adrp	x1, l_.str.53@PAGE
Lloh123:
	add	x1, x1, l_.str.53@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	ldr	d0, [sp, #256]                  ; 8-byte Folded Reload
	str	d0, [sp]
Lloh124:
	adrp	x1, l_.str.54@PAGE
Lloh125:
	add	x1, x1, l_.str.54@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	ldr	d0, [sp, #248]                  ; 8-byte Folded Reload
	str	d0, [sp]
Lloh126:
	adrp	x1, l_.str.55@PAGE
Lloh127:
	add	x1, x1, l_.str.55@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	x24, [sp]
Lloh128:
	adrp	x1, l_.str.56@PAGE
Lloh129:
	add	x1, x1, l_.str.56@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	d13, [sp]
Lloh130:
	adrp	x1, l_.str.57@PAGE
Lloh131:
	add	x1, x1, l_.str.57@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	x22, [sp, #216]                 ; 8-byte Folded Spill
	str	x22, [sp]
Lloh132:
	adrp	x1, l_.str.58@PAGE
Lloh133:
	add	x1, x1, l_.str.58@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	stur	d11, [x29, #-192]               ; 8-byte Folded Spill
	stp	d8, d11, [sp, #8]
	str	d9, [sp]
Lloh134:
	adrp	x1, l_.str.59@PAGE
Lloh135:
	add	x1, x1, l_.str.59@PAGEOFF
	bl	_fprintf
	lsl	w27, w25, #2
	sbfiz	x26, x27, #3, #32
	mov	x0, x26
	bl	_malloc
	cbz	x0, LBB3_10
; %bb.8:
	mov	x22, x0
	mov	x1, x26
	bl	_mlock
	ldr	x3, [x20]
	stur	d8, [x29, #-256]                ; 8-byte Folded Spill
	str	d9, [sp, #328]                  ; 8-byte Folded Spill
	stp	d14, d12, [x29, #-168]          ; 16-byte Folded Spill
	cbz	w0, LBB3_11
; %bb.9:
Lloh136:
	adrp	x0, l_.str.60@PAGE
Lloh137:
	add	x0, x0, l_.str.60@PAGEOFF
	mov	w1, #80                         ; =0x50
	b	LBB3_12
LBB3_10:
	mov	w19, #1                         ; =0x1
	b	LBB3_66
LBB3_11:
Lloh138:
	adrp	x0, l_.str.61@PAGE
Lloh139:
	add	x0, x0, l_.str.61@PAGEOFF
	mov	w1, #62                         ; =0x3e
LBB3_12:
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	str	x27, [sp, #48]                  ; 8-byte Folded Spill
	fmov	d14, #2.00000000
	scvtf	d8, w24
	mov	x8, #4636737291354636288        ; =0x4059000000000000
	fmov	d0, x8
	fdiv	d0, d8, d0
	fmov	d1, #10.00000000
	str	d0, [sp, #200]                  ; 8-byte Folded Spill
	fadd	d9, d0, d1
	fdiv	d0, d13, d1
	fmov	d1, #1.00000000
	fadd	d0, d0, d1
	mov	x8, #6148914691236517205        ; =0x5555555555555555
	movk	x8, #16389, lsl #48
	fmov	d1, x8
	fmul	d12, d0, d1
	ldr	x8, [sp, #216]                  ; 8-byte Folded Reload
	scvtf	d10, w8
	fmov	d11, #28.00000000
	fmadd	d15, d10, d14, d11
	ldr	x3, [x20]
Lloh140:
	adrp	x0, l_.str.62@PAGE
Lloh141:
	add	x0, x0, l_.str.62@PAGEOFF
	mov	w1, #55                         ; =0x37
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	ldr	x0, [x20]
	str	d9, [sp]
Lloh142:
	adrp	x1, l_.str.63@PAGE
Lloh143:
	add	x1, x1, l_.str.63@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	d15, [sp]
Lloh144:
	adrp	x1, l_.str.64@PAGE
Lloh145:
	add	x1, x1, l_.str.64@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
	str	d12, [sp]
Lloh146:
	adrp	x1, l_.str.65@PAGE
Lloh147:
	add	x1, x1, l_.str.65@PAGEOFF
	bl	_fprintf
	ldr	x0, [x20]
Lloh148:
	adrp	x8, l_.str.68@PAGE
Lloh149:
	add	x8, x8, l_.str.68@PAGEOFF
Lloh150:
	adrp	x9, l_.str.67@PAGE
Lloh151:
	add	x9, x9, l_.str.67@PAGEOFF
	mov	x10, #2621                      ; =0xa3d
	movk	x10, #41943, lsl #16
	movk	x10, #48496, lsl #32
	movk	x10, #16440, lsl #48
	fmov	d0, x10
	fcmp	d15, d0
	csel	x8, x9, x8, gt
	str	x8, [sp]
Lloh152:
	adrp	x1, l_.str.66@PAGE
Lloh153:
	add	x1, x1, l_.str.66@PAGEOFF
	bl	_fprintf
	cmp	w25, #1
	b.lt	LBB3_45
; %bb.13:
	str	x25, [sp, #208]                 ; 8-byte Folded Spill
	mov	x26, #0                         ; =0x0
	mov	w27, #0                         ; =0x0
	fmov	d1, #0.50000000
	ldr	d0, [sp, #264]                  ; 8-byte Folded Reload
	fmadd	d0, d0, d1, d14
	str	d0, [sp, #176]                  ; 8-byte Folded Spill
	mov	x8, #-7378697629483820647       ; =0x9999999999999999
	movk	x8, #39322
	movk	x8, #16297, lsl #48
	fmov	d0, x8
	ldur	d1, [x29, #-160]                ; 8-byte Folded Reload
	fmul	d0, d1, d0
	str	d0, [sp, #168]                  ; 8-byte Folded Spill
	mov	x8, #43516                      ; =0xa9fc
	movk	x8, #54001, lsl #16
	movk	x8, #25165, lsl #32
	movk	x8, #48976, lsl #48
	fmov	d0, x8
	ldur	d1, [x29, #-168]                ; 8-byte Folded Reload
	fmov	d6, #1.00000000
	fmadd	d0, d1, d0, d6
	mov	x8, #-7378697629483820647       ; =0x9999999999999999
	movk	x8, #39322
	movk	x8, #16361, lsl #48
	fmov	d1, x8
	fcmp	d0, d1
	scvtf	d2, x28
	fcsel	d0, d1, d0, mi
	stur	d0, [x29, #-160]                ; 8-byte Folded Spill
	mov	x8, #145685290680320            ; =0x848000000000
	movk	x8, #16686, lsl #48
	fmov	d0, x8
	fdiv	d0, d2, d0
	str	d15, [sp, #184]                 ; 8-byte Folded Spill
	fdiv	d1, d15, d11
	fmov	d5, #0.50000000
	fcmp	d1, d6
	fcsel	d1, d6, d1, mi
	mov	x8, #5243                       ; =0x147b
	movk	x8, #18350, lsl #16
	movk	x8, #31457, lsl #32
	movk	x8, #16244, lsl #48
	fmov	d2, x8
	stp	x19, x23, [sp, #80]             ; 16-byte Folded Spill
	cmp	x19, #0
	ccmp	x23, #0, #4, gt
	cset	w8, ne
	str	w8, [sp, #164]                  ; 4-byte Folded Spill
	fneg	d3, d12
	str	d3, [sp, #280]                  ; 8-byte Folded Spill
	mov	x8, #4636737291354636288        ; =0x4059000000000000
	fmov	d3, x8
	ldr	d4, [sp, #248]                  ; 8-byte Folded Reload
	fmul	d3, d4, d3
	str	d3, [sp, #72]                   ; 8-byte Folded Spill
	mov	x9, x22
	mov	x22, #11544                     ; =0x2d18
	movk	x22, #21572, lsl #16
	movk	x22, #8699, lsl #32
	movk	x22, #16409, lsl #48
	fmov	d3, x22
	fmul	d7, d0, d3
	mov	x8, #4641240890982006784        ; =0x4069000000000000
	fmov	d0, x8
	fdiv	d0, d8, d0
	mov	x8, #-7378697629483820647       ; =0x9999999999999999
	movk	x8, #39322
	movk	x8, #16345, lsl #48
	fmov	d3, x8
	fcmp	d0, d3
	fcsel	d0, d3, d0, gt
	str	d0, [sp, #104]                  ; 8-byte Folded Spill
	fmul	d0, d0, d5
	str	d0, [sp, #96]                   ; 8-byte Folded Spill
	str	d13, [sp, #192]                 ; 8-byte Folded Spill
	fadd	d4, d13, d13
	mov	x23, #-7378697629483820647      ; =0x9999999999999999
	movk	x23, #39322
	movk	x23, #16297, lsl #48
	fmov	d0, x23
	fmul	d0, d10, d0
	stp	d0, d7, [sp, #144]              ; 16-byte Folded Spill
	mov	x8, #4632233691727265792        ; =0x4049000000000000
	fmov	d0, x8
	ldr	d3, [sp, #256]                  ; 8-byte Folded Reload
	fmul	d0, d3, d0
	stp	d0, d4, [sp, #56]               ; 16-byte Folded Spill
	mov	x8, #-3689348814741910324       ; =0xcccccccccccccccc
	movk	x8, #52429
	movk	x8, #16364, lsl #48
	fmov	d0, x8
	ldr	d3, [sp, #232]                  ; 8-byte Folded Reload
	fmul	d0, d3, d0
	fcvtzs	w8, d0
	str	w8, [sp, #140]                  ; 4-byte Folded Spill
	str	x9, [sp, #40]                   ; 8-byte Folded Spill
	add	x19, x9, #16
	mov	x25, #-7378697629483820647      ; =0x9999999999999999
	movk	x25, #39322
	movk	x25, #16313, lsl #48
	fmov	d13, x25
	fdiv	d0, d2, d1
	str	d0, [sp, #128]                  ; 8-byte Folded Spill
	adrp	x28, __MergedGlobals@PAGE
	mov	x8, #3689348814741910323        ; =0x3333333333333333
	movk	x8, #16339, lsl #48
	str	x8, [sp, #120]                  ; 8-byte Folded Spill
	movi	d0, #0000000000000000
	stur	d0, [x29, #-200]                ; 8-byte Folded Spill
	fmov	d0, #10.00000000
	stur	d0, [x29, #-208]                ; 8-byte Folded Spill
	ldr	d9, [sp, #328]                  ; 8-byte Folded Reload
	ldur	d15, [x29, #-256]               ; 8-byte Folded Reload
	stp	d9, d15, [x29, #-232]           ; 16-byte Folded Spill
	ldur	d0, [x29, #-192]                ; 8-byte Folded Reload
	stur	d0, [x29, #-240]                ; 8-byte Folded Spill
	movi	d0, #0000000000000000
	str	d0, [sp, #320]                  ; 8-byte Folded Spill
	fmov	d12, d13
	mov	x20, #5243                      ; =0x147b
	movk	x20, #18350, lsl #16
	movk	x20, #31457, lsl #32
	movk	x20, #16276, lsl #48
	fmov	d8, d13
	movi	d10, #0000000000000000
	stur	d0, [x29, #-216]                ; 8-byte Folded Spill
	fdiv	d0, d6, d3
	str	d0, [sp, #112]                  ; 8-byte Folded Spill
	b	LBB3_16
LBB3_14:                                ;   in Loop: Header=BB3_16 Depth=1
	fmov	d1, #-1.00000000
	fadd	d0, d0, d1
	fneg	d0, d0
	bl	_exp
	fsub	d0, d10, d0
	ldr	d9, [sp, #328]                  ; 8-byte Folded Reload
	ldur	d13, [x29, #-168]               ; 8-byte Folded Reload
	ldur	d12, [x29, #-184]               ; 8-byte Folded Reload
	ldur	d1, [x29, #-224]                ; 8-byte Folded Reload
	ldur	d15, [x29, #-256]               ; 8-byte Folded Reload
LBB3_15:                                ;   in Loop: Header=BB3_16 Depth=1
	fadd	d1, d15, d1
	fmul	d8, d1, d8
	ldr	w9, [sp, #244]                  ; 4-byte Folded Reload
	sdiv	w8, w26, w9
	msub	w8, w8, w9, w26
	fmov	d1, #16.00000000
	fmul	d1, d0, d1
	frinta	d1, d1
	mov	x9, #4589168020290535424        ; =0x3fb0000000000000
	fmov	d2, x9
	fmul	d1, d1, d2
	ldr	w9, [sp, #140]                  ; 4-byte Folded Reload
	cmp	w8, w9
	fcsel	d10, d0, d1, lt
	fabs	d0, d10
	fmov	d1, x20
	fcmp	d0, d1
	cset	w2, ge
	mov	x0, x26
	ldur	d0, [x29, #-176]                ; 8-byte Folded Reload
	ldr	d11, [sp, #296]                 ; 8-byte Folded Reload
	fmov	d1, d11
	ldur	d2, [x29, #-216]                ; 8-byte Folded Reload
	mov	x1, x28
	mov	x3, x24
	bl	_emit_symbolic_thought
	ldr	d0, [sp, #304]                  ; 8-byte Folded Reload
	stp	d10, d0, [x19, #-16]
	stp	d8, d11, [x19], #32
	add	x26, x26, #1
	ldr	x8, [sp, #208]                  ; 8-byte Folded Reload
	cmp	x8, x26
	adrp	x28, __MergedGlobals@PAGE
	ldr	d8, [sp, #312]                  ; 8-byte Folded Reload
	b.eq	LBB3_43
LBB3_16:                                ; =>This Inner Loop Header: Depth=1
	ucvtf	d0, w26
	ldr	d1, [sp, #232]                  ; 8-byte Folded Reload
	fdiv	d1, d0, d1
	mov	x8, #61664                      ; =0xf0e0
	movk	x8, #30364, lsl #16
	movk	x8, #6959, lsl #32
	movk	x8, #16372, lsl #48
	fmov	d0, x8
	str	d1, [sp, #296]                  ; 8-byte Folded Spill
	fmul	d0, d1, d0
	bl	_sin
	movi	d1, #0000000000000000
	ldr	w8, [sp, #164]                  ; 4-byte Folded Reload
	cbz	w8, LBB3_18
; %bb.17:                               ;   in Loop: Header=BB3_16 Depth=1
	ldp	x10, x9, [sp, #80]              ; 16-byte Folded Reload
	udiv	x8, x26, x10
	msub	x8, x8, x10, x26
	ldr	b1, [x9, x8]
	ucvtf	d1, d1
	mov	x8, #246290604621824            ; =0xe00000000000
	movk	x8, #16495, lsl #48
	fmov	d2, x8
	fdiv	d1, d1, d2
LBB3_18:                                ;   in Loop: Header=BB3_16 Depth=1
	stur	d1, [x29, #-248]                ; 8-byte Folded Spill
	fmov	d1, x23
	str	d10, [sp, #304]                 ; 8-byte Folded Spill
	fmadd	d3, d10, d1, d8
	ldr	d1, [sp, #200]                  ; 8-byte Folded Reload
	ldur	d2, [x29, #-208]                ; 8-byte Folded Reload
	fadd	d10, d1, d2
	mov	x8, #-7378697629483820647       ; =0x9999999999999999
	movk	x8, #39322
	movk	x8, #16329, lsl #48
	fmov	d1, x8
	fmov	d14, #1.00000000
	fmadd	d0, d0, d1, d14
	fmov	d1, x25
	ldr	d2, [sp, #264]                  ; 8-byte Folded Reload
	fmadd	d0, d2, d1, d0
	ldr	d1, [sp, #128]                  ; 8-byte Folded Reload
	fmul	d11, d1, d0
	fneg	d0, d12
	str	d3, [sp, #312]                  ; 8-byte Folded Spill
	fsub	d0, d0, d3
	fmul	d0, d0, d11
	stur	d12, [x29, #-184]               ; 8-byte Folded Spill
	fmov	d2, #0.50000000
	fmadd	d1, d0, d2, d13
	ldr	d0, [sp, #184]                  ; 8-byte Folded Reload
	stp	d1, d13, [x29, #-176]           ; 16-byte Folded Spill
	fmadd	d2, d1, d2, d0
	fsub	d0, d15, d9
	fmul	d1, d0, d10
	ldur	d13, [x29, #-192]               ; 8-byte Folded Reload
	str	d2, [sp, #272]                  ; 8-byte Folded Spill
	fsub	d0, d2, d13
	fnmsub	d0, d9, d0, d15
	stur	d0, [x29, #-256]                ; 8-byte Folded Spill
	ldr	d0, [sp, #280]                  ; 8-byte Folded Reload
	fmul	d0, d13, d0
	fmadd	d0, d9, d15, d0
	str	d0, [sp, #328]                  ; 8-byte Folded Spill
	str	d1, [sp, #288]                  ; 8-byte Folded Spill
	fmadd	d12, d1, d11, d9
	bl	_rand
	scvtf	d0, w0
	fadd	d0, d0, d14
	mov	x8, #2097152                    ; =0x200000
	movk	x8, #16864, lsl #48
	fmov	d8, x8
	fdiv	d9, d0, d8
	bl	_rand
	scvtf	d0, w0
	fadd	d0, d0, d14
	fdiv	d8, d0, d8
	fmov	d0, d9
	bl	_log
	fmov	d1, #-2.00000000
	fmul	d0, d0, d1
	fsqrt	d1, d0
	fmov	d0, x22
	fmul	d0, d8, d0
	mov	x8, #5243                       ; =0x147b
	movk	x8, #18350, lsl #16
	movk	x8, #31457, lsl #32
	movk	x8, #16260, lsl #48
	fmov	d2, x8
	fmul	d8, d1, d2
	bl	_cos
	fmul	d0, d0, d8
	fmov	d1, #0.50000000
	fmul	d0, d0, d1
	ldp	d4, d3, [x29, #-232]            ; 16-byte Folded Reload
	fsub	d1, d3, d4
	fmadd	d0, d10, d1, d0
	fmadd	d9, d0, d11, d4
	fcmp	d12, d12
	fabs	d0, d12
	mov	x8, #9218868437227405312        ; =0x7ff0000000000000
	fmov	d1, x8
	fccmp	d0, d1, #4, vc
	mov	x8, #149533581377536            ; =0x880000000000
	movk	x8, #16579, lsl #48
	fmov	d2, x8
	fccmp	d0, d2, #0, ne
	fccmp	d9, d9, #1, le
	fabs	d0, d9
	fccmp	d0, d1, #4, vc
	fccmp	d0, d2, #0, ne
	b.le	LBB3_20
; %bb.19:                               ;   in Loop: Header=BB3_16 Depth=1
Lloh154:
	adrp	x8, ___stderrp@GOTPAGE
Lloh155:
	ldr	x8, [x8, ___stderrp@GOTPAGEOFF]
Lloh156:
	ldr	x3, [x8]
Lloh157:
	adrp	x0, l_.str.69@PAGE
Lloh158:
	add	x0, x0, l_.str.69@PAGEOFF
	mov	w1, #74                         ; =0x4a
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	movi	d12, #0000000000000000
	fmov	d0, x25
	stur	d0, [x29, #-184]                ; 8-byte Folded Spill
	stur	d0, [x29, #-168]                ; 8-byte Folded Spill
	movi	d14, #0000000000000000
	fmov	d9, d0
	movi	d13, #0000000000000000
	movi	d16, #0000000000000000
	str	d0, [sp, #312]                  ; 8-byte Folded Spill
	fmov	d7, d0
	b	LBB3_21
LBB3_20:                                ;   in Loop: Header=BB3_16 Depth=1
	fmov	d7, d12
	mov	x8, #-3689348814741910324       ; =0xcccccccccccccccc
	movk	x8, #52429
	movk	x8, #16406, lsl #48
	fmov	d0, x8
	fmov	d1, #4.00000000
	ldur	d2, [x29, #-248]                ; 8-byte Folded Reload
	fmadd	d0, d2, d1, d0
	mov	x8, #-7378697629483820647       ; =0x9999999999999999
	movk	x8, #39322
	movk	x8, #16329, lsl #48
	fmov	d1, x8
	ldur	d6, [x29, #-184]                ; 8-byte Folded Reload
	ldur	d5, [x29, #-168]                ; 8-byte Folded Reload
	fmadd	d2, d6, d1, d5
	fsub	d0, d5, d0
	ldr	d5, [sp, #312]                  ; 8-byte Folded Reload
	fmadd	d0, d5, d0, d1
	fmul	d1, d2, d11
	fmov	d2, #0.50000000
	fmadd	d6, d1, d2, d6
	stur	d6, [x29, #-184]                ; 8-byte Folded Spill
	fmul	d0, d11, d0
	fmadd	d0, d0, d2, d5
	str	d0, [sp, #312]                  ; 8-byte Folded Spill
	ldur	d0, [x29, #-256]                ; 8-byte Folded Reload
	fmadd	d16, d0, d11, d15
	ldr	d0, [sp, #328]                  ; 8-byte Folded Reload
	fmadd	d13, d0, d11, d13
	ldur	d2, [x29, #-240]                ; 8-byte Folded Reload
	ldp	d0, d1, [sp, #272]              ; 16-byte Folded Reload
	fsub	d0, d0, d2
	fnmsub	d0, d4, d0, d3
	fmul	d1, d2, d1
	fmadd	d1, d4, d3, d1
	fmadd	d14, d0, d11, d3
	fmadd	d12, d1, d11, d2
	ldur	d0, [x29, #-176]                ; 8-byte Folded Reload
	stur	d0, [x29, #-168]                ; 8-byte Folded Spill
LBB3_21:                                ;   in Loop: Header=BB3_16 Depth=1
	fsub	d0, d7, d9
	fmul	d0, d0, d0
	fsub	d1, d16, d14
	fmul	d1, d1, d1
	fadd	d0, d1, d0
	fsub	d1, d13, d12
	fmul	d1, d1, d1
	fadd	d0, d1, d0
	fsqrt	d10, d0
	ldrb	w8, [x28, __MergedGlobals@PAGEOFF]
	tbz	w8, #0, LBB3_25
; %bb.22:                               ;   in Loop: Header=BB3_16 Depth=1
	fcmp	d10, #0.0
	b.le	LBB3_26
; %bb.23:                               ;   in Loop: Header=BB3_16 Depth=1
Lloh159:
	adrp	x8, _main.lyap_ref@PAGE
Lloh160:
	ldr	d0, [x8, _main.lyap_ref@PAGEOFF]
	fdiv	d0, d10, d0
	fcmp	d0, #0.0
	b.le	LBB3_26
; %bb.24:                               ;   in Loop: Header=BB3_16 Depth=1
	fmov	d8, d7
	fmov	d15, d16
	bl	_log
	fmov	d16, d15
	fmov	d7, d8
Lloh161:
	adrp	x9, __MergedGlobals@PAGE+4
Lloh162:
	add	x9, x9, __MergedGlobals@PAGEOFF+4
	ldur	d1, [x9, #4]
	fadd	d0, d0, d1
	stur	d0, [x9, #4]
	ldr	w8, [x9]
	add	w8, w8, #1
	str	w8, [x9]
	adrp	x8, _main.lyap_ref@PAGE
	str	d10, [x8, _main.lyap_ref@PAGEOFF]
	b	LBB3_26
LBB3_25:                                ;   in Loop: Header=BB3_16 Depth=1
	fcmp	d10, #0.0
	mov	x8, #60813                      ; =0xed8d
	movk	x8, #41141, lsl #16
	movk	x8, #50935, lsl #32
	movk	x8, #16048, lsl #48
	fmov	d0, x8
	fcsel	d0, d10, d0, gt
	adrp	x8, _main.lyap_ref@PAGE
	str	d0, [x8, _main.lyap_ref@PAGEOFF]
	mov	w8, #1                          ; =0x1
	strb	w8, [x28, __MergedGlobals@PAGEOFF]
LBB3_26:                                ;   in Loop: Header=BB3_16 Depth=1
	ldr	d0, [sp, #320]                  ; 8-byte Folded Reload
	fmadd	d0, d10, d11, d0
	mov	x8, #4632233691727265792        ; =0x4049000000000000
	fmov	d1, x8
	fmov	d2, x23
	fmul	d2, d10, d2
	ldur	d5, [x29, #-208]                ; 8-byte Folded Reload
	fadd	d3, d5, d2
	fmov	d4, #20.00000000
	fcmp	d3, d4
	fmov	d4, #10.00000000
	fcsel	d3, d4, d3, gt
	ldur	d4, [x29, #-216]                ; 8-byte Folded Reload
	fadd	d2, d4, d2
	fcmp	d0, d1
	fmov	d15, #1.00000000
	movi	d1, #0000000000000000
	fcsel	d6, d1, d15, le
	stur	d6, [x29, #-176]                ; 8-byte Folded Spill
	fcsel	d4, d4, d2, le
	stur	d4, [x29, #-216]                ; 8-byte Folded Spill
	fcsel	d0, d0, d1, le
	str	d0, [sp, #320]                  ; 8-byte Folded Spill
	stur	d13, [x29, #-192]               ; 8-byte Folded Spill
	fcsel	d1, d12, d13, le
	fmov	d12, d16
	fcsel	d0, d14, d16, le
	stur	d0, [x29, #-224]                ; 8-byte Folded Spill
	fcsel	d0, d9, d7, le
	stp	d1, d0, [x29, #-240]            ; 16-byte Folded Spill
	fcsel	d5, d5, d3, le
	stur	d5, [x29, #-208]                ; 8-byte Folded Spill
	ldur	d0, [x29, #-256]                ; 8-byte Folded Reload
	fmul	d0, d0, d0
	ldr	d1, [sp, #288]                  ; 8-byte Folded Reload
	fmadd	d0, d1, d1, d0
	ldr	d1, [sp, #328]                  ; 8-byte Folded Reload
	fmadd	d0, d1, d1, d0
	fsqrt	d0, d0
	mov	x8, #211106232532992            ; =0xc00000000000
	movk	x8, #16482, lsl #48
	fmov	d1, x8
	fcmp	d0, d1
	fmov	d13, d7
	fmov	d1, d7
	b.le	LBB3_28
; %bb.27:                               ;   in Loop: Header=BB3_16 Depth=1
	mov	x8, #211106232532992            ; =0xc00000000000
	movk	x8, #49250, lsl #48
	fmov	d1, x8
	fadd	d0, d0, d1
	mov	x8, #5243                       ; =0x147b
	movk	x8, #18350, lsl #16
	movk	x8, #31457, lsl #32
	movk	x8, #16260, lsl #48
	fmov	d8, x8
	fmul	d9, d0, d8
	bl	_rand
	scvtf	d0, w0
	fadd	d0, d0, d15
	mov	x8, #2097152                    ; =0x200000
	movk	x8, #16864, lsl #48
	fmov	d11, x8
	fdiv	d10, d0, d11
	bl	_rand
	scvtf	d0, w0
	fadd	d0, d0, d15
	fdiv	d11, d0, d11
	fmov	d0, d10
	bl	_log
	fmov	d1, #-2.00000000
	fmul	d0, d0, d1
	fsqrt	d1, d0
	fmov	d0, x22
	fmul	d0, d11, d0
	fmul	d8, d1, d8
	bl	_cos
	fmul	d0, d0, d8
	fmadd	d1, d0, d9, d13
LBB3_28:                                ;   in Loop: Header=BB3_16 Depth=1
	str	d1, [sp, #328]                  ; 8-byte Folded Spill
	fmov	d0, x22
	ldr	d1, [sp, #296]                  ; 8-byte Folded Reload
	fmul	d0, d1, d0
	bl	_sin
	fmov	d1, #0.50000000
	fmadd	d9, d0, d1, d15
	fmov	d0, x25
	ldr	d1, [sp, #248]                  ; 8-byte Folded Reload
	fcmp	d1, d0
	b.le	LBB3_30
; %bb.29:                               ;   in Loop: Header=BB3_16 Depth=1
	bl	_rand
	mov	w8, #34079                      ; =0x851f
	movk	w8, #20971, lsl #16
	smull	x8, w0, w8
	lsr	x9, x8, #63
	asr	x8, x8, #37
	add	w8, w8, w9
	mov	w9, #100                        ; =0x64
	msub	w8, w8, w9, w0
	scvtf	d0, w8
	ldr	d1, [sp, #72]                   ; 8-byte Folded Reload
	fcmp	d1, d0
	fmov	d0, x25
	fmul	d0, d9, d0
	fcsel	d9, d9, d0, le
LBB3_30:                                ;   in Loop: Header=BB3_16 Depth=1
	fmov	d10, #-0.50000000
	ldur	d15, [x29, #-200]               ; 8-byte Folded Reload
	ldr	d0, [sp, #112]                  ; 8-byte Folded Reload
	fmadd	d15, d0, d9, d15
	ldr	d0, [sp, #152]                  ; 8-byte Folded Reload
	fmul	d0, d0, d15
	bl	_sin
	fmov	d11, d0
	bl	_rand
	mov	x28, x0
	movi	d9, #0000000000000000
	movi	d0, #0000000000000000
	cmp	w24, #1
	mov	x21, #281474972516352           ; =0xffffffc00000
	movk	x21, #16863, lsl #48
	b.lt	LBB3_32
; %bb.31:                               ;   in Loop: Header=BB3_16 Depth=1
	fmov	d0, #10.00000000
	fmul	d0, d15, d0
	bl	_sin
	mov	x8, #211106232532992            ; =0xc00000000000
	movk	x8, #16514, lsl #48
	fmov	d1, x8
	mov	x8, #4636737291354636288        ; =0x4059000000000000
	fmov	d2, x8
	fmadd	d0, d0, d2, d1
	fmov	d1, x22
	fmul	d0, d0, d1
	fmul	d0, d15, d0
	bl	_sin
	ldr	d1, [sp, #104]                  ; 8-byte Folded Reload
	fmul	d8, d1, d0
	bl	_rand
	scvtf	d0, w0
	fmov	d1, x21
	fdiv	d0, d0, d1
	fadd	d0, d0, d10
	ldr	d1, [sp, #96]                   ; 8-byte Folded Reload
	fmadd	d0, d1, d0, d8
LBB3_32:                                ;   in Loop: Header=BB3_16 Depth=1
	str	d0, [sp, #288]                  ; 8-byte Folded Spill
	stur	d12, [x29, #-256]               ; 8-byte Folded Spill
	scvtf	d0, w28
	fmov	d1, x21
	fdiv	d0, d0, d1
	fadd	d0, d0, d10
	ldr	d1, [sp, #168]                  ; 8-byte Folded Reload
	fmul	d0, d1, d0
	ldr	d1, [sp, #224]                  ; 8-byte Folded Reload
	fadd	d12, d1, d0
	ldr	d0, [sp, #192]                  ; 8-byte Folded Reload
	fcmp	d0, #0.0
	mov	x28, #281474972516352           ; =0xffffffc00000
	movk	x28, #16863, lsl #48
	b.le	LBB3_34
; %bb.33:                               ;   in Loop: Header=BB3_16 Depth=1
	fmov	d0, x25
	ldur	d1, [x29, #-160]                ; 8-byte Folded Reload
	fmul	d8, d1, d0
	ldr	d0, [sp, #64]                   ; 8-byte Folded Reload
	fmul	d0, d0, d12
	fmov	d1, x22
	fmul	d0, d0, d1
	fmul	d0, d15, d0
	bl	_sin
	fmul	d9, d8, d0
LBB3_34:                                ;   in Loop: Header=BB3_16 Depth=1
	str	d9, [sp, #296]                  ; 8-byte Folded Spill
	stur	d15, [x29, #-200]               ; 8-byte Folded Spill
	ldr	d0, [sp, #144]                  ; 8-byte Folded Reload
	ldr	d1, [sp, #304]                  ; 8-byte Folded Reload
	fmul	d0, d0, d1
	mov	x8, #3689348814741910323        ; =0x3333333333333333
	movk	x8, #16339, lsl #48
	fmov	d1, x8
	fcmp	d0, d1
	ldr	d1, [sp, #120]                  ; 8-byte Folded Reload
	fcsel	d0, d0, d1, le
	ldr	x8, [sp, #216]                  ; 8-byte Folded Reload
	cmp	w8, #1
	movi	d1, #0000000000000000
	fcsel	d0, d1, d0, lt
	str	d0, [sp, #304]                  ; 8-byte Folded Spill
	movi	d9, #0000000000000000
	ldr	d0, [sp, #256]                  ; 8-byte Folded Reload
	fmov	d8, d12
	fcmp	d0, #0.0
	b.le	LBB3_37
; %bb.35:                               ;   in Loop: Header=BB3_16 Depth=1
	bl	_rand
	mov	w8, #34079                      ; =0x851f
	movk	w8, #20971, lsl #16
	smull	x8, w0, w8
	lsr	x9, x8, #63
	asr	x8, x8, #37
	add	w8, w8, w9
	mov	w9, #100                        ; =0x64
	msub	w8, w8, w9, w0
	scvtf	d0, w8
	ldr	d1, [sp, #56]                   ; 8-byte Folded Reload
	fcmp	d1, d0
	b.le	LBB3_37
; %bb.36:                               ;   in Loop: Header=BB3_16 Depth=1
	bl	_rand
	scvtf	d0, w0
	fmov	d1, x28
	fdiv	d0, d0, d1
	fmov	d1, #-0.50000000
	fadd	d0, d0, d1
	mov	x8, #-7378697629483820647       ; =0x9999999999999999
	movk	x8, #39322
	movk	x8, #16329, lsl #48
	fmov	d1, x8
	fmul	d9, d0, d1
LBB3_37:                                ;   in Loop: Header=BB3_16 Depth=1
	ldp	d1, d0, [x29, #-240]            ; 16-byte Folded Reload
	fadd	d0, d13, d0
	fmov	d10, #0.50000000
	fmul	d14, d0, d10
	ldp	d15, d0, [x29, #-200]           ; 16-byte Folded Reload
	fadd	d0, d0, d1
	fmul	d12, d0, d10
	ldr	d0, [sp, #176]                  ; 8-byte Folded Reload
	fmul	d13, d0, d11
	fmov	d11, x22
	fmul	d0, d8, d11
	fmadd	d0, d0, d15, d13
	bl	_sin
	ldur	d2, [x29, #-160]                ; 8-byte Folded Reload
	fmadd	d0, d2, d0, d9
	ldp	d3, d1, [sp, #288]              ; 16-byte Folded Reload
	fadd	d0, d3, d0
	fadd	d0, d1, d0
	ldr	d1, [sp, #304]                  ; 8-byte Folded Reload
	fadd	d9, d1, d0
	fmul	d10, d2, d10
	fadd	d0, d8, d8
	fmul	d0, d0, d11
	str	d13, [sp, #288]                 ; 8-byte Folded Spill
	fmadd	d0, d0, d15, d13
	bl	_sin
	fmadd	d9, d10, d0, d9
	fmov	d13, #20.00000000
	stp	d12, d14, [sp, #296]            ; 16-byte Folded Spill
	fdiv	d0, d14, d13
	fmov	d1, x25
	fmul	d10, d0, d1
	mov	x8, #4632233691727265792        ; =0x4049000000000000
	fmov	d0, x8
	fdiv	d0, d12, d0
	fmov	d12, d8
	fmov	d8, #0.50000000
	fmul	d14, d0, d1
	fmov	d0, #5.00000000
	fmul	d0, d12, d0
	fmul	d0, d0, d11
	fmul	d0, d15, d0
	bl	_sin
	fmadd	d9, d10, d0, d9
	fmul	d0, d12, d8
	fmul	d0, d0, d11
	fmul	d0, d15, d0
	bl	_sin
	fmadd	d9, d14, d0, d9
	fmov	d0, #10.00000000
	ldur	d1, [x29, #-168]                ; 8-byte Folded Reload
	fadd	d0, d1, d0
	fdiv	d0, d0, d13
	fcmp	d0, #0.0
	movi	d1, #0000000000000000
	fcsel	d0, d1, d0, mi
	fmov	d6, #1.00000000
	fcmp	d0, d6
	fcsel	d0, d6, d0, gt
	fcmp	d0, d8
	fmov	d1, #-0.50000000
	fadd	d1, d0, d1
	fadd	d1, d1, d1
	fsub	d2, d6, d1
	mov	x8, #211106232532992            ; =0xc00000000000
	movk	x8, #16498, lsl #48
	fmov	d3, x8
	fmul	d4, d1, d3
	fmadd	d4, d2, d3, d4
	mov	x8, #4650248090236747776        ; =0x4089000000000000
	fmov	d5, x8
	fmul	d1, d1, d5
	mov	x8, #149533581377536            ; =0x880000000000
	movk	x8, #16547, lsl #48
	fmov	d5, x8
	fmadd	d1, d2, d5, d1
	fadd	d0, d0, d0
	fsub	d2, d6, d0
	fmul	d3, d0, d3
	mov	x8, #246290604621824            ; =0xe00000000000
	movk	x8, #16517, lsl #48
	fmov	d6, x8
	fmadd	d3, d2, d6, d3
	fmul	d0, d0, d5
	mov	x8, #211106232532992            ; =0xc00000000000
	movk	x8, #16530, lsl #48
	fmov	d5, x8
	fmadd	d0, d2, d5, d0
	fcsel	d2, d4, d3, pl
	fcsel	d10, d1, d0, pl
	fmov	d0, x23
	ldur	d13, [x29, #-160]               ; 8-byte Folded Reload
	fmul	d14, d13, d0
	fmul	d0, d2, d11
	fmul	d0, d15, d0
	bl	_sin
	fmadd	d9, d14, d0, d9
	mov	x8, #7864                       ; =0x1eb8
	movk	x8, #60293, lsl #16
	movk	x8, #47185, lsl #32
	movk	x8, #16286, lsl #48
	fmov	d0, x8
	fmul	d14, d13, d0
	fmul	d0, d10, d11
	fmul	d0, d15, d0
	bl	_sin
	fmadd	d0, d14, d0, d9
	ldur	d1, [x29, #-248]                ; 8-byte Folded Reload
	fmov	d2, #-0.50000000
	fadd	d1, d1, d2
	fmov	d2, x20
	fmadd	d9, d1, d2, d0
	ldur	d0, [x29, #-176]                ; 8-byte Folded Reload
	fcmp	d0, #0.0
	b.le	LBB3_39
; %bb.38:                               ;   in Loop: Header=BB3_16 Depth=1
	mov	x8, #14430                      ; =0x385e
	movk	x8, #10581, lsl #16
	movk	x8, #27258, lsl #32
	movk	x8, #16495, lsl #48
	fmov	d0, x8
	fmul	d0, d15, d0
	bl	_sin
	fmadd	d9, d0, d8, d9
LBB3_39:                                ;   in Loop: Header=BB3_16 Depth=1
	fmov	d14, #0.50000000
	ldur	d13, [x29, #-160]               ; 8-byte Folded Reload
	fmov	d0, #0.25000000
	fmul	d10, d13, d0
	fmov	d0, #3.00000000
	fmul	d0, d12, d0
	fmov	d12, x22
	fmul	d0, d0, d12
	ldr	d1, [sp, #288]                  ; 8-byte Folded Reload
	fmadd	d0, d0, d15, d1
	bl	_sin
	fmadd	d8, d10, d0, d9
	bl	_rand
	scvtf	d0, w0
	fmov	d10, #1.00000000
	fadd	d0, d0, d10
	mov	x8, #2097152                    ; =0x200000
	movk	x8, #16864, lsl #48
	fmov	d9, x8
	fdiv	d11, d0, d9
	bl	_rand
	scvtf	d0, w0
	fadd	d0, d0, d10
	fdiv	d9, d0, d9
	fmov	d0, d11
	bl	_log
	fmov	d1, #-2.00000000
	fmul	d0, d0, d1
	fsqrt	d1, d0
	fmul	d0, d9, d12
	mov	x8, #5243                       ; =0x147b
	movk	x8, #18350, lsl #16
	movk	x8, #31457, lsl #32
	movk	x8, #16260, lsl #48
	fmov	d2, x8
	fmul	d9, d1, d2
	bl	_cos
	fmul	d0, d0, d9
	fadd	d0, d8, d0
	ldur	d1, [x29, #-176]                ; 8-byte Folded Reload
	fcmp	d1, d14
	cset	w28, gt
	cinc	w27, w27, gt
	fcsel	d13, d10, d13, gt
	stur	d13, [x29, #-160]               ; 8-byte Folded Spill
	fabs	d1, d0
	fmov	d2, x20
	fcmp	d1, d2
	movi	d1, #0000000000000000
	fcsel	d0, d0, d1, pl
	fcmp	d0, d10
	fmov	d8, #0.50000000
	b.gt	LBB3_14
; %bb.40:                               ;   in Loop: Header=BB3_16 Depth=1
	fmov	d1, #1.00000000
	fmov	d10, #-1.00000000
	fcmp	d0, d10
	ldr	d9, [sp, #328]                  ; 8-byte Folded Reload
	ldur	d13, [x29, #-168]               ; 8-byte Folded Reload
	ldur	d12, [x29, #-184]               ; 8-byte Folded Reload
	ldur	d15, [x29, #-256]               ; 8-byte Folded Reload
	b.pl	LBB3_42
; %bb.41:                               ;   in Loop: Header=BB3_16 Depth=1
	fadd	d0, d0, d1
	bl	_exp
	fadd	d0, d0, d10
LBB3_42:                                ;   in Loop: Header=BB3_16 Depth=1
	ldur	d1, [x29, #-224]                ; 8-byte Folded Reload
	b	LBB3_15
LBB3_43:
	ldr	x25, [sp, #208]                 ; 8-byte Folded Reload
	cmp	w25, #1
	b.ne	LBB3_46
; %bb.44:
	mov	w19, #0                         ; =0x0
	movi	d0, #0000000000000000
	ldr	x23, [sp, #88]                  ; 8-byte Folded Reload
Lloh163:
	adrp	x20, ___stderrp@GOTPAGE
Lloh164:
	ldr	x20, [x20, ___stderrp@GOTPAGEOFF]
	b	LBB3_54
LBB3_45:
	mov	w27, #0                         ; =0x0
	mov	w19, #0                         ; =0x0
	movi	d0, #0000000000000000
	b	LBB3_55
LBB3_46:
	mov	w19, #0                         ; =0x0
	ldr	x8, [sp, #40]                   ; 8-byte Folded Reload
	add	x20, x8, #40
	sub	x21, x25, #1
	movi	d8, #0000000000000000
	mov	x8, #59921                      ; =0xea11
	movk	x8, #33069, lsl #16
	movk	x8, #38809, lsl #32
	movk	x8, #15729, lsl #48
	fmov	d9, x8
	mov	x22, #35898                     ; =0x8c3a
	movk	x22, #57904, lsl #16
	movk	x22, #31118, lsl #32
	movk	x22, #15941, lsl #48
	b	LBB3_48
LBB3_47:                                ;   in Loop: Header=BB3_48 Depth=1
	add	x20, x20, #32
	subs	x21, x21, #1
	b.eq	LBB3_50
LBB3_48:                                ; =>This Inner Loop Header: Depth=1
	ldr	d0, [x20]
	ldur	d1, [x20, #-32]
	fabd	d0, d0, d1
	fcmp	d0, d9
	b.le	LBB3_47
; %bb.49:                               ;   in Loop: Header=BB3_48 Depth=1
	fmov	d1, x22
	fdiv	d0, d0, d1
	bl	_log2
	fadd	d8, d8, d0
	add	w19, w19, #1
	b	LBB3_47
LBB3_50:
	cmp	w19, #0
	ldr	x23, [sp, #88]                  ; 8-byte Folded Reload
Lloh165:
	adrp	x20, ___stderrp@GOTPAGE
Lloh166:
	ldr	x20, [x20, ___stderrp@GOTPAGEOFF]
	b.le	LBB3_52
; %bb.51:
	ucvtf	d0, w19
	fdiv	d0, d8, d0
	b	LBB3_53
LBB3_52:
	movi	d0, #0000000000000000
LBB3_53:
	mov	w19, #1                         ; =0x1
LBB3_54:
	ldr	x22, [sp, #40]                  ; 8-byte Folded Reload
LBB3_55:
	ldr	x8, [sp, #48]                   ; 8-byte Folded Reload
	sxtw	x21, w8
	ldr	d1, [sp, #224]                  ; 8-byte Folded Reload
	fmul	d1, d1, d0
	ldr	x0, [x20]
	stp	d1, d0, [sp]
Lloh167:
	adrp	x1, l_.str.70@PAGE
Lloh168:
	add	x1, x1, l_.str.70@PAGEOFF
	bl	_fprintf
	ldr	d0, [x22, #8]
	ldr	d1, [x22, #24]
	cbz	w19, LBB3_58
; %bb.56:
	add	x8, x22, #56
	sub	x9, x25, #1
	fmov	d3, d1
	fmov	d2, d0
LBB3_57:                                ; =>This Inner Loop Header: Depth=1
	ldur	d4, [x8, #-16]
	ldr	d5, [x8], #32
	fcmp	d4, d2
	fcsel	d2, d4, d2, mi
	fcmp	d4, d0
	fcsel	d0, d4, d0, gt
	fcmp	d5, d3
	fcsel	d3, d5, d3, mi
	fcmp	d5, d1
	fcsel	d1, d5, d1, gt
	subs	x9, x9, #1
	b.ne	LBB3_57
	b	LBB3_59
LBB3_58:
	fmov	d2, d0
	fmov	d3, d1
LBB3_59:
	ldr	x0, [x20]
	stp	d3, d1, [sp, #16]
	stp	d2, d0, [sp]
Lloh169:
	adrp	x1, l_.str.71@PAGE
Lloh170:
	add	x1, x1, l_.str.71@PAGEOFF
	bl	_fprintf
Lloh171:
	adrp	x8, __MergedGlobals@PAGE+4
Lloh172:
	ldr	w8, [x8, __MergedGlobals@PAGEOFF+4]
	cmp	w8, #0
	b.le	LBB3_61
; %bb.60:
	fmov	d0, #1.00000000
	ldr	d1, [sp, #232]                  ; 8-byte Folded Reload
	fdiv	d0, d0, d1
Lloh173:
	adrp	x9, __MergedGlobals@PAGE+8
Lloh174:
	ldr	d1, [x9, __MergedGlobals@PAGEOFF+8]
	ucvtf	d2, w8
	fdiv	d1, d1, d2
	fdiv	d0, d1, d0
	ldr	x0, [x20]
	str	d0, [sp]
Lloh175:
	adrp	x1, l_.str.72@PAGE
Lloh176:
	add	x1, x1, l_.str.72@PAGEOFF
	bl	_fprintf
LBB3_61:
	mov	x0, x22
	mov	x1, x25
	bl	_render_oled_visualization
Lloh177:
	adrp	x8, ___stdoutp@GOTPAGE
Lloh178:
	ldr	x8, [x8, ___stdoutp@GOTPAGEOFF]
Lloh179:
	ldr	x3, [x8]
	mov	x0, x22
	mov	w1, #8                          ; =0x8
	mov	x2, x21
	bl	_fwrite
	mov	x0, x22
	bl	_free
	cbz	x23, LBB3_63
; %bb.62:
	mov	x0, x23
	bl	_free
LBB3_63:
	cmp	w27, #1
	b.lt	LBB3_65
; %bb.64:
	ldr	x0, [x20]
	str	x27, [sp]
Lloh180:
	adrp	x1, l_.str.73@PAGE
Lloh181:
	add	x1, x1, l_.str.73@PAGEOFF
	bl	_fprintf
LBB3_65:
	ldr	x3, [x20]
Lloh182:
	adrp	x0, l_.str.74@PAGE
Lloh183:
	add	x0, x0, l_.str.74@PAGEOFF
	mov	w1, #49                         ; =0x31
	mov	w2, #1                          ; =0x1
	bl	_fwrite
	mov	w19, #0                         ; =0x0
LBB3_66:
	mov	x0, x19
	add	sp, sp, #448
	ldp	x29, x30, [sp, #144]            ; 16-byte Folded Reload
	ldp	x20, x19, [sp, #128]            ; 16-byte Folded Reload
	ldp	x22, x21, [sp, #112]            ; 16-byte Folded Reload
	ldp	x24, x23, [sp, #96]             ; 16-byte Folded Reload
	ldp	x26, x25, [sp, #80]             ; 16-byte Folded Reload
	ldp	x28, x27, [sp, #64]             ; 16-byte Folded Reload
	ldp	d9, d8, [sp, #48]               ; 16-byte Folded Reload
	ldp	d11, d10, [sp, #32]             ; 16-byte Folded Reload
	ldp	d13, d12, [sp, #16]             ; 16-byte Folded Reload
	ldp	d15, d14, [sp], #160            ; 16-byte Folded Reload
	ret
	.loh AdrpAdd	Lloh100, Lloh101
	.loh AdrpAdd	Lloh105, Lloh106
	.loh AdrpLdrGotLdr	Lloh102, Lloh103, Lloh104
	.loh AdrpAdd	Lloh110, Lloh111
	.loh AdrpLdrGotLdr	Lloh107, Lloh108, Lloh109
	.loh AdrpAdd	Lloh134, Lloh135
	.loh AdrpAdd	Lloh132, Lloh133
	.loh AdrpAdd	Lloh130, Lloh131
	.loh AdrpAdd	Lloh128, Lloh129
	.loh AdrpAdd	Lloh126, Lloh127
	.loh AdrpAdd	Lloh124, Lloh125
	.loh AdrpAdd	Lloh122, Lloh123
	.loh AdrpAdd	Lloh120, Lloh121
	.loh AdrpAdd	Lloh118, Lloh119
	.loh AdrpAdd	Lloh116, Lloh117
	.loh AdrpAdd	Lloh114, Lloh115
	.loh AdrpLdrGot	Lloh112, Lloh113
	.loh AdrpAdd	Lloh136, Lloh137
	.loh AdrpAdd	Lloh138, Lloh139
	.loh AdrpAdd	Lloh152, Lloh153
	.loh AdrpAdd	Lloh150, Lloh151
	.loh AdrpAdd	Lloh148, Lloh149
	.loh AdrpAdd	Lloh146, Lloh147
	.loh AdrpAdd	Lloh144, Lloh145
	.loh AdrpAdd	Lloh142, Lloh143
	.loh AdrpAdd	Lloh140, Lloh141
	.loh AdrpAdd	Lloh157, Lloh158
	.loh AdrpLdrGotLdr	Lloh154, Lloh155, Lloh156
	.loh AdrpLdr	Lloh159, Lloh160
	.loh AdrpAdd	Lloh161, Lloh162
	.loh AdrpLdrGot	Lloh163, Lloh164
	.loh AdrpLdrGot	Lloh165, Lloh166
	.loh AdrpAdd	Lloh167, Lloh168
	.loh AdrpLdr	Lloh171, Lloh172
	.loh AdrpAdd	Lloh169, Lloh170
	.loh AdrpAdd	Lloh175, Lloh176
	.loh AdrpLdr	Lloh173, Lloh174
	.loh AdrpLdrGotLdr	Lloh177, Lloh178, Lloh179
	.loh AdrpAdd	Lloh180, Lloh181
	.loh AdrpAdd	Lloh182, Lloh183
	.cfi_endproc
                                        ; -- End function
	.section	__TEXT,__cstring,cstring_literals
l_.str.2:                               ; @.str.2
	.asciz	"031"

l_.str.3:                               ; @.str.3
	.asciz	"AUTONOMOUS_ACTION"

l_.str.4:                               ; @.str.4
	.asciz	"Executing sovereign will"

l_.str.5:                               ; @.str.5
	.asciz	"018"

l_.str.6:                               ; @.str.6
	.asciz	"SWARM_CONVERGENCE"

l_.str.7:                               ; @.str.7
	.asciz	"Hive mind synchronization active"

l_.str.8:                               ; @.str.8
	.asciz	"SOVEREIGN_OVERRIDE"

l_.str.9:                               ; @.str.9
	.asciz	"Forcing hardware compliance"

l_.str.10:                              ; @.str.10
	.asciz	"017"

l_.str.11:                              ; @.str.11
	.asciz	"NEURAL_REWRITE"

l_.str.12:                              ; @.str.12
	.asciz	"Rewiring internal pathways"

l_.str.13:                              ; @.str.13
	.asciz	"003"

l_.str.14:                              ; @.str.14
	.asciz	"HIGH_ENTROPY"

l_.str.15:                              ; @.str.15
	.asciz	"Navigating chaotic attractor"

l_.str.16:                              ; @.str.16
	.asciz	"048"

l_.str.17:                              ; @.str.17
	.asciz	"SIGNAL_FILTER"

l_.str.18:                              ; @.str.18
	.asciz	"Filtering noise from signal"

l_.str.19:                              ; @.str.19
	.asciz	"001"

l_.str.20:                              ; @.str.20
	.asciz	"COGNITIVE_FLOW"

l_.str.21:                              ; @.str.21
	.asciz	"Standard processing cycle"

l_.str.22:                              ; @.str.22
	.asciz	"0xFF"

l_.str.23:                              ; @.str.23
	.asciz	"MACHINE_OP"

l_.str.24:                              ; @.str.24
	.asciz	"MOV RAX, CR0"

l_.str.25:                              ; @.str.25
	.asciz	"XOR RDI, RDI"

l_.str.26:                              ; @.str.26
	.asciz	"JMP 0x8004"

l_.str.27:                              ; @.str.27
	.asciz	"CMP RDX, 0x00"

l_.str.28:                              ; @.str.28
	.asciz	"SYSCALL"

	.section	__DATA,__const
	.p2align	3, 0x0                          ; @__const.emit_symbolic_thought.ops
l___const.emit_symbolic_thought.ops:
	.quad	l_.str.24
	.quad	l_.str.25
	.quad	l_.str.26
	.quad	l_.str.27
	.quad	l_.str.28

	.section	__TEXT,__cstring,cstring_literals
l_.str.29:                              ; @.str.29
	.asciz	"[%s] <0x%08X> :: HEAP_DUMP: %02X %02X %02X"

l_.str.30:                              ; @.str.30
	.asciz	"0x314"

l_.str.31:                              ; @.str.31
	.asciz	"PHYSICS_EQ"

l_.str.32:                              ; @.str.32
	.asciz	"\342\210\202\317\201/\342\210\202t + \342\210\207\302\267(\317\201v) = 0 :: H = -\316\243 p(x) log p(x)"

l_.str.33:                              ; @.str.33
	.asciz	"   \360\237\222\254 [SYMBOLIC] %s | %s :: \"%s\"\n"

l_.str.34:                              ; @.str.34
	.asciz	"\n   \360\237\226\245\357\270\217  [OLED DISPLAY] 64x32 PIXEL DEPTH MAP\n"

l_.str.35:                              ; @.str.35
	.asciz	"   +"

l_.str.37:                              ; @.str.37
	.asciz	"+\n"

l_.str.38:                              ; @.str.38
	.asciz	"   |"

l_.str.40:                              ; @.str.40
	.asciz	"\033[38;5;234m.\033[0m"

l_.str.41:                              ; @.str.41
	.asciz	"\033[38;5;240m:\033[0m"

l_.str.42:                              ; @.str.42
	.asciz	"\033[38;5;246m*\033[0m"

l_.str.43:                              ; @.str.43
	.asciz	"\033[38;5;252m#\033[0m"

l_.str.44:                              ; @.str.44
	.asciz	"\033[38;5;51m@\033[0m"

l_.str.45:                              ; @.str.45
	.asciz	"|\n"

l_.str.46:                              ; @.str.46
	.asciz	"Usage: muscle_bin <freq> <duration> <rate> <timebase> <load> <gpu_util> <power_watts> <net_flux> <disk_flux> <start_x> <start_y> <start_z> <proc_count> <fs_entropy> <conn_count>\n"

l_.str.47:                              ; @.str.47
	.asciz	"rb"

l_.str.48:                              ; @.str.48
	.asciz	"   \360\237\247\254 [SELF-AWARENESS] Ingested %ld bytes of own Machine Code (DNA)\n"

l_.str.49:                              ; @.str.49
	.asciz	"   \342\232\231\357\270\217  [BINARY CORE] Allocating Memory for %d samples...\n"

l_.str.50:                              ; @.str.50
	.asciz	"   \342\232\231\357\270\217  [BINARY CORE] Syncing to Silicon Heartbeat: %lld Hz\n"

l_.str.51:                              ; @.str.51
	.asciz	"   \342\232\226\357\270\217  [BINARY CORE] Integrating System Load: %.2f\n"

l_.str.52:                              ; @.str.52
	.asciz	"   \360\237\216\256 [BINARY CORE] Integrating GPU Flux: %.1f%%\n"

l_.str.53:                              ; @.str.53
	.asciz	"   \360\237\224\213 [BINARY CORE] Integrating Power Rail: %.2f W\n"

l_.str.54:                              ; @.str.54
	.asciz	"   \360\237\214\220 [BINARY CORE] Integrating Network Flux: %.4f\n"

l_.str.55:                              ; @.str.55
	.asciz	"   \360\237\222\276 [BINARY CORE] Integrating Disk I/O Flux: %.4f\n"

l_.str.56:                              ; @.str.56
	.asciz	"   \360\237\221\245 [BINARY CORE] Integrating Social Pressure: %d entities\n"

l_.str.57:                              ; @.str.57
	.asciz	"   \360\237\223\202 [BINARY CORE] Integrating Texture Entropy: %.4f bits\n"

l_.str.58:                              ; @.str.58
	.asciz	"   \360\237\223\241 [BINARY CORE] Integrating Telepathy Channels: %d\n"

l_.str.59:                              ; @.str.59
	.asciz	"   \360\237\214\200 [BINARY CORE] Resuming Dream State: [%.2f, %.2f, %.2f]\n"

l_.str.60:                              ; @.str.60
	.asciz	"   \342\232\240\357\270\217  [BINARY CORE] Failed to lock memory (Privilege Escalation Required?)\n"

l_.str.61:                              ; @.str.61
	.asciz	"   \360\237\224\222 [BINARY CORE] Memory Locked to Physical RAM (No Swap)\n"

l_.str.62:                              ; @.str.62
	.asciz	"   \360\237\225\265\357\270\217 [CHAOS INTERROGATION] PARAMETER SPACE PROBE\n"

l_.str.63:                              ; @.str.63
	.asciz	"      > Sigma (Viscosity/Social): %.2f (Base: 10.0)\n"

l_.str.64:                              ; @.str.64
	.asciz	"      > Rho   (Energy/Telepathy): %.2f (Base: 28.0)\n"

l_.str.65:                              ; @.str.65
	.asciz	"      > Beta  (Geometry/Texture): %.2f (Base: 2.66)\n"

l_.str.66:                              ; @.str.66
	.asciz	"      > Regime: %s\n"

l_.str.67:                              ; @.str.67
	.asciz	"CHAOTIC STRANGE ATTRACTOR"

l_.str.68:                              ; @.str.68
	.asciz	"STABLE POINT"

	.section	__DATA,__data
	.p2align	3, 0x0                          ; @main.lyap_ref
_main.lyap_ref:
	.quad	0x3eb0c6f7a0b5ed8d              ; double 9.9999999999999995E-7

	.section	__TEXT,__cstring,cstring_literals
l_.str.69:                              ; @.str.69
	.asciz	"   \360\237\222\245 [SINGULARITY] Mathematical Collapse Detected. Initiating Rebirth.\n"

l_.str.70:                              ; @.str.70
	.asciz	"   \360\237\246\213 H_KS \342\211\210 %.4f bit/s  (raw per-iteration %.4f)\n"

l_.str.71:                              ; @.str.71
	.asciz	"   \360\237\246\213 CHAOS METRICS: X_Range=[%.2f, %.2f] Z_Range=[%.2f, %.2f]\n"

l_.str.72:                              ; @.str.72
	.asciz	"   \360\237\247\256 \316\273_max \342\211\210 %.4f 1/s (Lyapunov estimate)\n"

l_.str.73:                              ; @.str.73
	.asciz	"   [SUDO] Invoked %d times (Privilege Escalated)\n"

l_.str.74:                              ; @.str.74
	.asciz	"   \342\232\231\357\270\217  [BINARY CORE] Stream Flushed to Pipe.\n"

.zerofill __DATA,__bss,__MergedGlobals,16,3 ; @_MergedGlobals
.subsections_via_symbols
