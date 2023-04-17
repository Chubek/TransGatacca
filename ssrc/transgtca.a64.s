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
	.section transgtca_abi_translate, b
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

	.section transgtca_abi_revtranslate, b
		.desc transgtca_revtranslate, void transgtca_translate(char *protein, char *lut, unsigned long *freqlut, unsigned long minfreq, char *resultptr)
		.def
			.tag transgtca_revtranslate, void transgtca_translate(char *protein, char *lut, unsigned long *freqlut, unsigned long minfreq, char *resultptr)
		.endef
		transgtca_revtranslate:
			MCSRS
		1:
			MCZRO REV_LOC_NUC1
			MCZRO REV_LOC_NUC2
			MCZRO REV_LOC_NUC3
			MCZRO REV_LOC_PEPD
			MCZRO REV_LOC_ENCD
			MCZRO REV_LOC_NTRP
			
			MCMPI REV_LOC_PEPW, REV_PRT_ADDR, IDT_LDBY, LIT_NUNO

			MCTST REV_LOC_PEPW, REV_LOC_PEPW
			MCBRC IDT_ISNE, 2f, IDT_ISEQ, 7f

		2:
			MCSUB REV_LOC_PEPW, REV_LOC_PEPW, LIT_NXQU
			MCMOF REV_LOC_ENCD, REV_LUT_ADDR, IDT_LDRQ, REV_LOC_PEPD

			MCAND REV_LOC_NTRP, REV_LOC_NTRP, LIT_NQCM

			MCPSH REV_LOC_NTRP
			MCSHL REV_LOC_NTRP, REV_LOC_NTRP, LIT_NUNO
			MCPOP REV_LOC_NTRP

			MCSHL REV_LOC_ENCD, REV_LOC_ENCD, LIT_NDUO
		3:
			MCZRO REV_LOC_NUCS
			MCZRO REV_LOC_TIDX

			MCSHR REV_LOC_ENCD, REV_LOC_ENCD, LIT_NSEN
			MCAND REV_LOC_NUCS, REV_LOC_ENCD, LIT_NXTR
		
			MCSHL REV_LOC_TIDX, REV_LOC_PEPD, LIT_NTRI
			
			MCPSH REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI
			MCORR REV_LOC_TIDX, REV_LOC_TIDX, REV_LOC_NUCS
			MCPOP REV_LOC_NUCS
			
			MCPSH REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NSEN
			MCSHR REV_LOC_NUCS, REV_LOC_NUCS, LIT_NDUO
			MCSHL REV_LOC_NUCS, REV_LOC_NUCS, LIT_NUNO
			MCORR REV_LOC_TIDX, REV_LOC_TIDX, REV_LOC_NUCS
			MCPOP REV_LOC_NUCS

			MCPSH REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NDOD
			MCSHR REV_LOC_NUCS, REV_LOC_NUCS, LIT_NQAT
			MCXOR REV_LOC_TIDX, REV_LOC_TIDX, REV_LOC_NUCS
			MCPOP REV_LOC_NUCS
		

			MCZRO REV_LOC_TMPW
			MCMOF REV_LOC_TMPW, REV_FRQ_ADDR, IDT_LDBY, REV_LOC_TIDW
			MCORS REV_LOC_TMPX, REV_LOC_TMPX, REV_LOC_NUCS, IDT_SHFL, LIT_NOCT
			MCPUH REV_LOC_TMPW

			MCTST REV_LOC_ENCD, REV_LOC_ENCD
			MCBRC IDT_ISEQ, 4f, IDT_ISNE, 3b
		4:
			MCZRO REV_LOC_TIDX
			MCJMP 5f
		5:
			MCZRO REV_LOC_TMPX

			MCPOH REV_LOC_TMPW
			MCAND REV_LOC_FREQ, REV_LOC_TMPX, LIT_NCFF
			MCSHR REV_LOC_NUCS, REV_LOC_TMPX, LIT_NOCT
			MCCMP REV_LOC_FREQ, REV_FRQ_MINM

			MCBRC IDT_ISLT, 5b, IDT_ISGE, 6f
		6:
			MCZRO REV_LOC_TMPX

			MCPSH REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI
			MCSHL REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI
			MCSHR REV_LOC_NUCS, ENCODED_NUCS, REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NCFF
			MCORS REV_LOC_TMPX, REV_LOC_TMPX, REV_LOC_NUCS, IDT_SHFL, LIT_NVQT
			MCPOP REV_LOC_NUCS

			MCPSH REV_LOC_NUCS
			MCANS REV_LOC_NUCS, REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI, IDT_SHFR, LIT_NDUO
			MCSHL REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI
			MCSHR REV_LOC_NUCS, ENCODED_NUCS, REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NCFF
			MCORS REV_LOC_TMPX, REV_LOC_TMPX, REV_LOC_NUCS, IDT_SHFL, LIT_NHEX
			MCPOP REV_LOC_NUCS

			MCPSH REV_LOC_NUCS
			MCANS REV_LOC_NUCS, REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI, IDT_SHFR, LIT_NQAT
			MCSHL REV_LOC_NUCS, REV_LOC_NUCS, LIT_NTRI
			MCSHR REV_LOC_NUCS, ENCODED_NUCS, REV_LOC_NUCS
			MCAND REV_LOC_NUCS, REV_LOC_NUCS, LIT_NCFF
			MCORS REV_LOC_TMPX, REV_LOC_TMPX, REV_LOC_NUCS, IDT_SHFL, LIT_NOCT
			MCPOP REV_LOC_NUCS 

			MCORR REV_LOC_TMPW, REV_LOC_TMPW, LIT_NPIP
			MCMPI REV_LOC_TMPW, REV_RES_ADDR, IDT_SRFWW, LIT_NQAT
	
			MCADD REV_LOC_TIDX, REV_LOC_TIDX, LIT_NUNO
			MCCMP REV_LOC_TIDX, REV_LOC_NTRP
			MCBRC IDT_ISEQ, 1b, IDT_ISNE, 5b
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

		.macro mcand dst, src, value  
			and \dst, \src, \value
		.endm

		.macro mcorr dst, src, value  
			orr \dst, \src, \value
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

		.macro mcmvs dst, src, shop, shn
			movk \dst, \src, \shop \shn
		.endm

		.macro mcads dst, src, value, shop, shn  
			add \dst, \src, \value, \shop \shn
		.endm

		.macro mcsbs dst, src, value, shop, shn  
			sub \dst, \src, \value, \shop \shn
		.endm

		.macro mcans dst, src, value, shop, shn  
			and \dst, \src, \value, \shop \shn
		.endm

		.macro mcors dst, src, value, shop, shn  
			orr \dst, \src, \value, \shop \shn
		.endm

		.macro mcxrs dst, src, value, shop, shn
			eor \dst, \src, \value, \shop \shn
		.endm

		.macro mcbrc cond1, jmp1, cond2, jmp2
			\cond1 \jmp1
			\cond2 \jmp2
		.endm

		.macro mcsrr
			mcpop lr
			ret
		.endm

		.macro mcsrs
			mcpsh lr
		.endm

		.macro mctst val1, val2
			tst \val1, \val2
		.endm

		.macro mccmp val1, val2
			cmp \val1, \val2
		.endm

		.macro mcjmp label
			bl \label
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
			str \reg, [sp, LIT_NNCT]!
		.endm

		.macro mcpop reg
			ldr \reg, [sp], LIT_NOCT
		.end

		.macro mcpub reg
			mcmip \reg, sp, IDT_SRBY, LIT_NNUN
		.endm

		.macro mcpob reg
			mcmpi \reg, sp, IDT_LRBY, LIT_NUNO
		.endm

		.macro mcpuh reg
			mcmip \reg, sp, IDT_SRHW, LIT_NNDU
		.endm

		.macro mcpoh reg
			mcmpi \reg, sp, IDT_LRHW, LIT_NDUO
		.endm

		.macro mcdsp value
			mcsub IDT_SPRG, IDT_SPRG, \value
		.endm

		.macro mcisp value
			mcadd IDT_SPRG, IDT_SPRG, \value
		.endm

		.macro mczro reg
			mcxor \reg, \reg, \reg
		.endm

		.macro mcssp dst
			mcmvz \dst, sp
		.endm

		.macro mcmvi dst, src
			mcxor \dst, \dst, \dst
			.rept 2
				mcosl \dst, \src, \src, IDT_SHFL, LIT_NUNO
				mcadd \dst, \dst, \src
			.endr
		.endm

		.macro mcssf dst, val
			mcshl \val, \val, LIT_NUNO
			mcsub \dst, \val, LIT_NXQT
			\shiftop \dst, \dst, LIT_NUNO
			mcshl \val, \val, LIT_NUNO
		.endm

	.section transgtca_aliases, b
		.section transgtca_translate_aliases, b
			TRN_DNA_ADDR    .req    x0
			TRN_LUT_ADDR    .req    x1
			TRN_RES_ADDR    .req    x2

			TRN_LOC_NUC1    .req    w8
			TRN_LOC_NUC1    .req    w9
			TRN_LOC_NUC2    .req    w10
			TRN_LOC_PEPT    .req    w11
			TRN_LOC_TMPN    .req    w12

		.section transgtca_revtranslate_aliases, b
			REV_PRT_ADDR    .req    x0
			REV_LUT_ADDR    .req    x1
			REV_FRQ_ADDR    .req    x2
			REV_FRQ_MINM    .req    x3
			REV_RES_ADDR    .req    x4
			
			REV_LOC_NUCS	.req	x8
			REV_LOC_PEPW    .req    w9
			REV_LOC_PEPD    .req    x9
			REV_LOC_ENCD    .req    x10
			REV_LOC_ENCW    .req    w10
			REV_LOC_NTRP    .req    x11
			REV_LOC_FREQ    .req    w11
			REV_LOC_TIDX	.req	x12
			REV_LOC_SSSP	.req	x12
			REV_LOC_TMPX	.req	x13
			REV_LOC_TMPW	.req	w13
		
		.section transgtca_global_literals, b
			LIT_NNIL		.req	#0
			LIT_NUNO		.req	#1
			LIT_NDUO		.req	#2
			LIT_NTRI		.req	#3
			LIT_NQAT		.req	#4
			LIT_NSEN		.req	#6
			LIT_NSPT		.req	#7
			LIT_NOCT		.req	#8
			LIT_NDOD		.req	#12
			LIT_NQCM		.req	#15
			LIT_NHEX		,req	#16
			LIT_NVQT		.req	#24
			LIT_NQTO		.req	#48
			LIT_NXTR		.req	#63
			LIT_NXQT		.req	#64
			LIT_NXQU		.req	#65
			LIT_NPIP		.req	#124
			LIT_NCFF		.req	#255
			LIT_NTFZ		.req	#16128
			LIT_NNUN		.req 	#-1
			LIT_NNDU		.req	#-2
			LIT_NNQT		.req	#-4
			LIT_NNCT		.req	#-8
		
		.section transgtca_global_idents, b
			IDT_ISEQ		.req    b.eq
			IDT_ISNE		.req 	b.ne
			IDT_ISGE		.req    b.ge
			IDT_ISLT		.req 	b.lt
			IDT_LDBY		.req	ldrb
			IDT_SRBY		.req	strb
			IDT_LDHW		.req	ldrh
			IDT_SRHW		.req	strh
			IDT_LDFW		.req	ldrw
			IDT_SRFW		.req	strw
			IDT_SHFL		.req	lsl
			IDT_SHFR		.req	lsr
			IDT_LDRQ		.req	ldr
			IDT_STRQ		.req 	str
			IDT_SPRG		.req	sp

.data
	.section transgtca_magic, b
		.equ ENCODED_NUCS, 0x47544341

	.section transgtca_externdec, b
		.global transgtca_translate
		.global transgtca_revtranslate
