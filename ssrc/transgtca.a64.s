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

.text
	.ident transgtca_abi_translate
		.desc transgtca_translate, void transgtca_translate(char *dna, char *lut, char *resultptr)
		.def
			.tag void transgtca_translate(char *dna, char *lut, char *resultptr)
		.endef
		transgtca_translate:    
			MCSRS
			MCZRO TRN_LOC_NUC1
			MCZRO TRN_LOC_NUC2
			MCZRO TRN_LOC_NUC3
			MCZRO TRN_LOC_PEPT
			MCZRO TRN_LOC_TMPN

		1:
			MCMPI TRN_LOC_NUC1, TRN_DNA_ADDR, IDT_LDBY, LIT_NUNO
			MCMPI TRN_LOC_NUC2, TRN_DNA_ADDR, IDT_LDBY, LIT_NUNO
			MCMPI TRN_LOC_NUC3, TRN_DNA_ADDR, IDT_LDBY, LIT_NUNO

			MCAND TRN_LOC_TMPN, TRN_LOC_NUC1, TRN_LOC_NUC1
			MCTST TRN_LOC_TMPN, TRN_LOC_NUC2    
			MCBRC IDT_ISNE, 2f, IDT_ISEQ, 3f

		2:
			MCSHR TRN_LOC_NUC1, TRN_LOC_NUC1, LIT_NUNO
			MCSHR TRN_LOC_NUC2, TRN_LOC_NUC2, LIT_NUNO
			MCSHR TRN_LOC_NUC3, TRN_LOC_NUC3, LIT_NUNO
			MCAND TRN_LOC_NUC1, TRN_LOC_NUC1, LIT_NTRI
			MCAND TRN_LOC_NUC2, TRN_LOC_NUC2, LIT_NTRI
			MCAND TRN_LOC_NUC3, TRN_LOC_NUC3, LIT_NTRI


			MCZRO TRN_LOC_TMPN      
			MCORS TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC1, IDT_SHFL, LIT_NQAT  
			MCORS TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC2, IDT_SHFL, LIT_NDUO
			MCORR TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC3   

			MCMIF TRN_LOC_PEPT, TRN_LUT_ADDR, IDT_LDBY, TRN_LOC_TMPN
			MCMPI TRN_LOC_PEPT, TRN_RES_ADDR. IDT_SRBY LIT_NUNO

			MCJMP 1b

		3:
			MCSRR

	.ident transgtca_abi_revtranslate
		.desc transgtca_revtranslate, void transgtca_translate(char *protein, char *lut, unsigned long *freqlut, unsigned long minfreq, char *resultptr)
		.def
			.tag transgtca_revtranslate, void transgtca_translate(char *protein, char *lut, unsigned long *freqlut, unsigned long minfreq, char *resultptr)
		.endef
		transgtca_revtranslate:
			MCSRS
			MCZRO REV_LOC_NUC1
			MCZRO REV_LOC_NUC2
			MCZRO REV_LOC_NUC3
			MCZRO REV_LOC_PEPD
			MCZRO REV_LOC_TMPN
			MCZRO REV_LOC_NIDX
		1:
			MCMPI REV_LOC_PEPW, REV_PRT_ADDR, IDT_LDBY, LIT_NUNO

			MCTST REV_LOC_PEPW, REV_LOC_PEPW
			MCBRC IDT_ISNE, 2f, IDT_ISEQ, 7f

		2:
			MCSUB REV_LOC_PEPW, REV_LOC_PEPW, LIT_NSQU
			MCMOF REV_LOC_ENCD, REV_LUT_ADDR, ldr, REV_LOC_PEPD

			MCAND REV_LOC_NTRP, REV_LOC_PEPD, LIT_NUNO5
			MCPSH REV_LOC_NTRP
			MCPSH REV_LOC_NTRP
			MCMVI REV_LOC_NTRP, REV_LOC_NTRP
			MCSSF REV_LOC_NTRP, REV_LOC_NTRP
			MCSHR REV_LOC_ENCD, REV_LOC_ENCD, REV_LOC_NTRP
			MCPOP REV_LOC_NTRP
			MCSHL REV_LOC_NTRP, REV_LOC_NTRP, LIT_NTRI
			MCSSP REV_LOC_SSSP
		3:
			MCZRO REV_LOC_TIDX
			MCSSP REV_LOC_TIDX
			MCSUB REV_LOC_TIDX, REV_LOC_SSSP, REV_LOC_TIDX
			MCSHR REV_LOC_TIDX, REV_LOC_TIDX, LIT_NTRI
			MCSUB REV_LOC_TIDX, REV_LOC_TIDX, LIT_NDUO
			MCMVI REV_LOC_TIDX, REV_LOC_TIDX
			MCPSH REV_LOC_ENCD
			MCXTR REV_LOC_ENCD, REV_LOC_ENCD, #63, REV_LOC_TIDX

			MCXTR REV_LOC_NUC1, REV_LOC_ENCW, LIT_NTRI, LIT_NNIL
			MCXTR REV_LOC_NUC2, REV_LOC_ENCW, LIT_NTRI, LIT_NUNO2
			MCXTR REV_LOC_NUC3, REV_LOC_ENCW, LIT_NTRI, LIT_NQAT8   

			MCZRO REV_LOC_TIDX
			MCORS REV_LOC_TIDW, REV_LOC_NUC1, REV_LOC_NUC2, IDT_SHFL, LIT_NUNO
			MCXOR REV_LOC_TIDW, REV_LOC_NUC1, REV_LOC_NUC3
			MCORS REV_LOC_TIDW, REV_LOC_TIDW, REV_LOC_PEPW, IDT_SHFL, LIT_NTRI

			MCPOP REV_LOC_ENCD
			
			MCMOF REV_LOC_TMPN, REV_FRQ_ADDR, IDT_LDBY, REV_LOC_TIDX
			MCPSH REV_LOC_TMPN

			MCZRO REV_LOC_TIDX
			MCSSP REV_LOC_TIDX
			MCSUB REV_LOC_TIDX, REV_LOC_TIDX, REV_LOC_SSSP
			MCCMP REV_LOC_TIDX, REV_LOC_NTRP
			MCBRC IDT_ISEQ, 4f, IDT_ISNE, 3b
		4:
			MCSSP REV_LOC_SSSP
			MCJMP 5f
		5:
			MCPOP REV_LOC_FREQ
			MCCMP REV_LOC_FREQ, REV_FRQ_MINM
			MCBRC b.gt, 5b, b.le, 6f
		6:
			MCSHL REV_LOC_NUC1, REV_LOC_NUC1, LIT_NTRI
			MCSHR REV_LOC_NUC1, ENCODED_NUCS, REV_LOC_NUC1
			MCAND REV_LOC_NUC1, REV_LOC_NUC1, LIT_NDUO55

			MCSHL REV_LOC_NUC2, REV_LOC_NUC2, LIT_NTRI
			MCSHR REV_LOC_NUC2, ENCODED_NUCS, REV_LOC_NUC2
			MCAND REV_LOC_NUC2, REV_LOC_NUC2, LIT_NDUO55

			MCSHL REV_LOC_NUC3, REV_LOC_NUC3, LIT_NTRI
			MCSHR REV_LOC_NUC3, ENCODED_NUCS, REV_LOC_NUC3
			MCAND REV_LOC_NUC3, REV_LOC_NUC3, LIT_NDUO55 

			MCMPI REV_LOC_NUC1, REV_RES_ADDR, IDT_SRBY LIT_NUNO
			MCMPI REV_LOC_NUC2, REV_RES_ADDR, IDT_SRBY LIT_NUNO
			MCMPI REV_LOC_NUC3, REV_RES_ADDR, IDT_SRBY LIT_NUNO

			MCZRO REV_LOC_TIDX
			MCSSP REV_LOC_TIDX
			MCSUB REV_LOC_TIDX, REV_LOC_SSSP, REV_LOC_TIDX
			MCCMP REV_LOC_TIDX, REV_LOC_NTRP
			MCBRC IDT_ISEQ, 4f, IDT_ISNE, 3b
		5:
			MCSUB REV_RES_ADDR, LIT_NTRI
			MCJMP 5b
		7:
			MCSRR

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
			ldr \reg, [sp], LIT_NOCT
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
				movk \dst, \src, \src, lsl LIT_NUNO
				add \dst, \dst, \src
			.endr
		.endm

		.macro mcssf dst, val
			lsl \val, \val, LIT_NUNO
			sub \dst, \val, LIT_NSQT
			lsr \dst, \dst, LIT_NUNO
			lsr \val, \val, LIT_NUNO
		.endm

		.macro mcssp dst
			mov \dst, sp
		.endm

		.macro mcsrr
			MCPOP lr
			ret
		.endm

		.macro mcsrs
			MCPSH lr
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
			REV_LOC_NTRP    .req    x13
			REV_LOC_FREQ    .req    w11
			REV_LOC_SSSP	.req	x6
			REV_LOC_TIDX	.req	x5
			REV_LOC_TIDW	.req	x5

		.ident transgtca_global_literals
			LIT_NNIL		.req	#0
			LIT_NUNO		.req	#1
			LIT_NDUO		.req	#2
			LIT_NTRI		.req	#3
			LIT_NQAT		.req	#4
			LIT_NOCT		.req	#8
			LIT_NSQT		.req	#64
			LIT_NSQU		.req	#65
		
		.ident transgtca_global_idents
			IDT_ISEQ		.req    b.eq
			IDT_ISNE		.req 	b.ne
			IDT_LDBY		.req	ldrb
			IDT_SRBY		.req	strb
			IDT_SHFL		.req	lsl

.data
	.ident transgtca_magic
		.equ ENCODED_NUCS, 0x47544341

	.ident transgtca_externdec
		.global transgtca_translate
		.global transgtca_revtranslate
