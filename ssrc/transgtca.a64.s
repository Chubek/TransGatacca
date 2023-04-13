// TransGatacca ABI: DNA to Protein [Reverse] Translator
// Aarch64 version (see transgtca.x64.s for x86-64 version)
// transgtca.a64.s
// 7547 bytes (sans comments)
// targeted for GNU Assembler
// subroutines compatible with C's calling convention

// subroutines:
/* 
	extern void transgtca_translate(
		char *dna, 
		char *lut, 
		char *resultptr
	);
	extern void transgtca_revtranslate(
		char *protein, 
		char *lut, 
		unsigned long *freqlut, 
		unsigned long minfreq, c
		har *resultptr
	);
*/

// this code is micro-optmized. It does not use opcodes with high execution
// latencies. For ease of inter-architecture adoption of the code, macros have
// been utilized. You can view descriptions for these macros in OPT.md

.text

.ident transgtca_abi_translate
	.desc transgtca_translate, void transgtca_translate(char *dna, char *lut, char *resultptr)
	.def
		.tag void transgtca_translate(char *dna, char *lut, char *resultptr)
	.endef
	transgtca_translate:      
		MCPSH lr
		MCZRO TRN_LOC_NUC1
		MCZRO TRN_LOC_NUC2
		MCZRO TRN_LOC_NUC3
		MCZRO TRN_LOC_PEPT
		MCZRO TRN_LOC_TMPN

	1:
		MCMPI TRN_LOC_NUC1, TRN_DNA_ADDR, ldrb, #1
		MCMPI TRN_LOC_NUC2, TRN_DNA_ADDR, ldrb, #1
		MCMPI TRN_LOC_NUC3, TRN_DNA_ADDR, ldrb, #1

		MCAND TRN_LOC_TMPN, TRN_LOC_NUC1, TRN_LOC_NUC1
		MCTST TRN_LOC_TMPN, TRN_LOC_NUC2    
		MCBRC b.ne, 2f, b.eq, 3f

	2:
		MCSHR TRN_LOC_NUC1, TRN_LOC_NUC1, #1
		MCSHR TRN_LOC_NUC2, TRN_LOC_NUC2, #1
		MCSHR TRN_LOC_NUC3, TRN_LOC_NUC3, #1
		MCAND TRN_LOC_NUC1, TRN_LOC_NUC1, #3
		MCAND TRN_LOC_NUC2, TRN_LOC_NUC2, #3
		MCAND TRN_LOC_NUC3, TRN_LOC_NUC3, #3


		MCMOV TRN_LOC_TMPN, wzr        
		MCORS TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC1, lsl, #4  
		MCORS TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC2, lsl, #2
		MCORR TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC3   

		MCMIF TRN_LOC_PEPT, TRN_LUT_ADDR, ldrb, TRN_LOC_TMPN
		MCMPI TRN_LOC_PEPT, TRN_RES_ADDR. strb, #1

		MCJMP 1b

	3:
		MCPOP lr
		ret

.ident transgtca_abi_revtranslate
	.desc transgtca_revtranslate, void transgtca_translate(char *protein, char *lut, unsigned long *freqlut, unsigned long minfreq, char *resultptr)
	.def
		.tag transgtca_revtranslate, void transgtca_translate(char *protein, char *lut, unsigned long *freqlut, unsigned long minfreq, char *resultptr)
	.endef
	transgtca_revtranslate:
		MCPSH lr
		MCZRO REV_LOC_NUC1
		MCZRO REV_LOC_NUC2
		MCZRO REV_LOC_NUC3
		MCZRO REV_LOC_PEPD
		MCZRO REV_LOC_TMPN
		MCZRO REV_LOC_NIDX
	1:
		MCMPI REV_LOC_PEPW, REV_PRT_ADDR, ldrb, #1

		MCTST REV_LOC_PEPW, REV_LOC_PEPW
		MCBRC b.ne, 2f, b.eq, 7f  

	2:
		MCSUB REV_LOC_PEPW, REV_LOC_PEPW, #65
		MCMOF REV_LOC_ENCD, REV_LUT_ADDR, ldr, REV_LOC_PEPD

		MCAND REV_LOC_NTRP, REV_LOC_PEPD, #15
		MCMVI REV_LOC_NTVI, REV_LOC_NTRP
		MCPSH REV_LOC_NTRP
		MCMVZ REV_LOC_NTRP, #64
		MCSUB REV_LOC_NTRP, REV_LOC_NTRP, REV_LOC_NTVI
		MCSHR REV_LOC_ENCD, REV_LOC_ENCD, REV_LOC_NTRP
		MCPOP REV_LOC_NTRP
		MCZRO REV_LOC_SIDX
	3:
		MCPSH REV_LOC_ENCD
		MCXTR REV_LOC_ENCD, REV_LOC_ENCD, #63, REV_LOC_SIDX

		MCXTR REV_LOC_NUC1, REV_LOC_ENCW, #3, #0
		MCXTR REV_LOC_NUC2, REV_LOC_ENCW, #3, #12
		MCXTR REV_LOC_NUC3, REV_LOC_ENCW, #3, #48   

		MCORS REV_LOC_FIDW, REV_LOC_NUC1, REV_LOC_NUC2, lsl, #1
		MCXOR REV_LOC_FIDW, REV_LOC_NUC1, REV_LOC_NUC3
		MCORS REV_LOC_FIDW, REV_LOC_FIDX, REV_LOC_PEPW, lsl, #3

		MCPOP REV_LOC_ENCD

		MCMOF REV_LOC_TMPN, REV_FRQ_ADDR, ldrb, REV_LOC_FIDX
		MCPSH REV_LOC_TMPN
		
		MCADD REV_LOC_SIDX, REV_LOC_SIDX, #1
		MCCMP REV_LOC_SIDX, REV_LOC_NTRP
		MCBRC b.eq, 4f, b.ne 3b
	4:
		MCZRO REV_LOC_SIDX
		MCJMP 5f
	5:
		MCPOP REV_LOC_FREQ
		MCCMP REV_LOC_FREQ, REV_FRQ_MINM
		MCBRC b.gt, 5b, b.le, 6f
	6:
		MCSHL REV_LOC_NUC1, REV_LOC_NUC1, #3
		MCSHR REV_LOC_NUC1, ENCODED_NUCS, REV_LOC_NUC1
		MCAND REV_LOC_NUC1, REV_LOC_NUC1, #255

		MCSHL REV_LOC_NUC2, REV_LOC_NUC2, #3
		MCSHR REV_LOC_NUC2, ENCODED_NUCS, REV_LOC_NUC2
		MCAND REV_LOC_NUC2, REV_LOC_NUC2, #255

		MCSHL REV_LOC_NUC3, REV_LOC_NUC3, #3
		MCSHR REV_LOC_NUC3, ENCODED_NUCS, REV_LOC_NUC3
		MCAND REV_LOC_NUC3, REV_LOC_NUC3, #255 

		MCMIF REV_LOC_NUC1, REV_RES_ADDR, strb, REV_LOC_NIDX
		MCADD REV_LOC_NIDX, REV_LOC_NIDX, #1
		MCMIF REV_LOC_NUC2, REV_RES_ADDR, strb, REV_LOC_NIDX
		MCADD REV_LOC_NIDX, REV_LOC_NIDX, #1
		MCMIF REV_LOC_NUC3, REV_RES_ADDR, strb, REV_LOC_NIDX

		MCADD REV_LOC_SIDX, REV_LOC_SIDX, #1
		MCCMP REV_LOC_SIDX, REV_LOC_NTRP
		MCBRC b.eq, 1b, b.ne 5f
	5:
		MCSUB REV_LOC_NIDX, REV_LOC_NIDX, #2
		MCJMP 5b
	7:
		MPOP lr
		ret

.bss
	.section transgtca_macros, b
		.macro mcmov dst, src, 
			mov \dst, \src
		.endm

		.macro mcmvz dst, src, 
			movz \dst, \src
		.endm

		.macro mcmvs dst, src, shop, shn
			movk \dst, \src, \shop \shn
		.endm
		
		.macro mcand dst, src, value  
			and \dst, \src, \value
		.endm

		.macro mcans dst, src, value, shop, shn  
			ands \dst, \src, \value, \shop \shn
		.endm

		.macro mcorr dst, src, value  
			orr \dst, \src, \value
		.endm

		.macro mcors dst, src, value, shop, shn  
			orr \dst, \src, \value, \shop \shn
		.endm

		.macro mcxor dst, src, value  
			eor \dst, \src, \value
		.endm

		.macro mcsub dst, src, value  
			sub \dst, \src, \value
		.endm

		.macro mcadd dst, src, value  
			add \dst, \src, \value
		.endm

		.macro mcshr dst, src, value
			lsr \dst, \src, \value
		.endm

		.macro mcshl dst, src, value
			lsl \dst, \src, \value
		.endm

		.macro mcclz dst, value
			clz \dst, \value
		.endm

		.macro mctst val1, val2
			tst \val1, \val2
		.endm

		.macro mccmp val1, val2
			cmp \val1, \val2
		.endm

		.macro mcbrc cond1, jmp1, cond2, jmp2
			\cond1 \jmp1
			\cond2 \jmp2
		.endm

		.macro mcmpi dst, addr, lsop, idx
			\lsop \dst, [\addr], \idx
		.endm      

		.macro mcmip dst, addr, lsop, idx
			\lsop \dst, [\addr, \idx]!
		.endm      

		.macro mcmif dst, addr, lsop, offst
			\lsop \dst, [\addr, \offst]
		.endm      

		.macro mcpsh reg
			str \reg, [sp, #-8]!
		.endm

		.macro mcpop reg
			ldr \reg, [sp], #8
		.endm

		.macro mcjmp label
			bl \label
		.endm

		.macro mczro reg
			eor \reg, \reg, \reg
		.endm

		.macro mcxtr dst, src, mask, shiftamnt
			and \dst, \src, \mask
			lsr \dst, \dst, \shiftamnt
		.endm

		.macro mcmvi dst, src
			eor \dst, \dst, \dst
			.rept 2
				movk \dst, \src, \src, lsl #1
				add \dst, \dst, \src
			.endr
		.endm

	.section transgtca_aliases, b
		.ident transgtca_translate_aliases       
			TRN_DNA_ADDR    .req    x0
			TRN_LUT_ADDR    .req    x1
			TRN_RES_ADDR    .req    x2

			TRN_LOC_NUC1    .req    w8
			TRN_LOC_NUC1    .req    w9
			TRN_LOC_NUC2    .req    w10
			TRN_LOC_PEPT    .req    w11
			TRN_LOC_TMPN    .req    w12

		.ident transgtca_revtranslate_aliases            
			REV_PRT_ADDR    .req    x0
			REV_LUT_ADDR    .req    x1
			REV_FRQ_ADDR    .req    x2
			REV_FRQ_MINM    .req    x3
			REV_RES_ADDR    .req    x4

			REV_LOC_NUC1    .req    w8
			REV_LOC_NUC1    .req    w9
			REV_LOC_NUC2    .req    w10
			REV_LOC_PEPW    .req    w11
			REV_LOC_PEPD    .req    x11
			REV_LOC_ENCD    .req    x12
			REV_LOC_TMPN    .req    x13
			REV_LOC_NTRP    .req    x14
			REV_LOC_NTVI    .req    x15
			REV_LOC_SIDX    .req    x16
			REV_LOC_FIDX    .req    x17
			REV_LOC_FIDW    .req    w17
			REV_LOC_NIDX    .req    x18
			REV_LOC_FREQ    .req    x13

.data
	.ident transgtca_magic
		.equ ENCODED_NUCS, 0x47544341

	.ident transgtca_externdec
		.global transgtca_translate
		.global transgtca_revtranslate
