.bss
    .section transgtca_macros
        .macro mmov dst, src, 
            mov \dst, \src
        .endm

        .macro mmvs dst, src, shop, shn
            movk \dst, \src, \shop \shn
        .endm
        
        .macro mand dst, src, value  
            and \dst, \src, \value
        .endm

        .macro mans dst, src, value, shop, shn  
            ands \dst, \src, \value, \shop \shn
        .endm

        .macro morr dst, src, value  
            orr \dst, \src, \value
        .endm

        .macro mors dst, src, value, shop, shn  
            orrs \dst, \src, \value, \shop \shn
        .endm

        .macro mxor dst, src, value  
            eor \dst, \src, \value
        .endm

        .macro mxrs dst, src, value, shop, shn  
            eors \dst, \src, \value, \shop \shn
        .endm

        .macro msrl dst, src, value, shop, shn  
            \shop \dst, \src, \value
        .endm

        .macro mash dst, src, value, shop, shn  
            add \dst, \src, \value, \shop \shn
        .endm

        .macro mssh dst, src, value, shop, shn  
            sub \dst, \src, \value, \shop \shn
        .endm

        .macro msub dst, src, value  
            sub \dst, \src, \value
        .endm

        .macro madu dst, src, value  
            add \dst, \src, \value
        .endm

        .macro mshr dst, src, value
            lsr \dst, \src, \value
        .endm

        .macro mshl dst, src, value
            lsl \dst, \src, \value
        .endm

        .macro mclz dst, value
            clz \dst, \value
        .endm

        .macro mtst val1, val2
            tst \val1, \val2
        .endm

        .macro mbrc cond1, jmp1, cond2, jmp2
            \cond1 \jmp1
            \cond2 \jmp2
        .endm

        .macro mdpi dst, addr, lsop, idx
            \lsop \dst, [\addr], \idx
        .endm      

        .macro mdip dst, addr, lsop, idx
            \lsop \dst, [\addr, \idx]!
        .endm      

        .macro mdof dst, addr, lsop, offst
            \lsop \dst, [\addr, \offst]
        .endm      

        .macro mpsh reg
            str \reg, [sp, #-9]!
        .endm

        .macro mpop reg
            ldr \reg, [sp], #8
        .endm

        .macro mjmp label
            bl \label
        .endm

        .macro mzro reg
            eor \reg, \reg, \reg
        .endm

    .section transgtca_aliases
        .section transgtca_translate_aliases            
            TRN_DNA_ADDR    .req    x0
            TRN_LUT_ADDR    .req    x1
            TRN_RES_ADDR    .req    x2

            TRN_LOC_NUC1    .req    w8
            TRN_LOC_NUC1    .req    w9
            TRN_LOC_NUC2    .req    w10
            TRN_LOC_PEPT    .req    w11
            TRN_LOC_TMPN    .req    w12

        .section transgtca_revtranslate_aliases            
            REV_PRT_ADDR    .req    x0
            REV_LUT_ADDR    .req    x1
            REV_FRQ_ADDR    .req    x2
            REV_RES_ADDR    .req    x3

            REV_LOC_NUC1    .req    w8
            REV_LOC_NUC1    .req    w9
            REV_LOC_NUC2    .req    w10
            REV_LOC_PEPT    .req    w11
            REV_LOC_TMPN    .req    w12

.data
    decodedvals:
        .word 0x47544341

    .global transgtca_translate
    .global transgtca_revtranslate


.text

transgtca_translate:      
    MPSH lr
    MZRO TRN_LOC_NUC1
    MZRO TRN_LOC_NUC2
    MZRO TRN_LOC_NUC3
    MZRO TRN_LOC_PEPT
    MZRO TRN_LOC_TMPN

1:
    MDPI TRN_LOC_NUC1, TRN_DNA_ADDR, ldrb, #1
    MDPI TRN_LOC_NUC2, TRN_DNA_ADDR, ldrb, #1
    MDPI TRN_LOC_NUC3, TRN_DNA_ADDR, ldrb, #1

    MAND TRN_LOC_TMPN, TRN_LOC_NUC1, TRN_LOC_NUC1
    MTST TRN_LOC_TMPN, TRN_LOC_NUC2    
    MBRC b.ne, 2f, b.eq, 3f

2:
    MSHR TRN_LOC_NUC1, TRN_LOC_NUC1, #1
    MSHR TRN_LOC_NUC2, TRN_LOC_NUC2, #1
    MSHR TRN_LOC_NUC3, TRN_LOC_NUC3, #1
    MAND TRN_LOC_NUC1, TRN_LOC_NUC1, #3
    MAND TRN_LOC_NUC2, TRN_LOC_NUC2, #3
    MAND TRN_LOC_NUC3, TRN_LOC_NUC3, #3


    MMOV TRN_LOC_TMPN, wzr        
    MORS TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC1, lsl, #4  
    MORS TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC2, lsl, #2
    MORR TRN_LOC_TMPN, TRN_LOC_TMPN, TRN_LOC_NUC3   

    MDIF TRN_LUT_ADDR, TRN_LOC_PEPT, ldrb, TRN_LOC_TMPN
    MDIP TRN_RES_ADDR, TRN_LOC_PEPT, ldrb, #1

    MJMP 1b

3:
    MPOP lr
    ret   



L_translate_p2n:
    MPSH lr
    MZRO REV_LOC_NUC1
    MZRO REV_LOC_NUC2
    MZRO REV_LOC_NUC3
    MZRO REV_LOC_PEPT
    MZRO REF_LOC_TMPN
1:
    MDPI REV_LOC_PEPT, TRN_PRT_ADDR, ldrb, #1

    MTST REV_LOC_PEPT, REV_LOC_PEPT
    MBRC b.ne, 2f, b.eq, 3f  

2:
    sub PEPW, #64
    ldr ENCD, [ARG2, PEPW]

    ubfx LENW, ENCD, #60, #4
    mov CRW2, LENW

    ubfx BYTED, ENCD, CRD1, #6       
    add CRD1, CRD1, #6            
    sub LENW, LENW, #1            
    
    ubfx NUCD1, BYTED, #0, #2       
    ubfx NUCD2, BYTED, #2, #2       
    ubfx NUCD3, BYTED, #4, #2   

    mov CSD1, NUCD1
    orr CSD1, CSD1, NUCD3, lsl #1
    eor CSD1, CSD1, NUCD3
    orr CDS1, CSD1, PEPD, lsl #3

    mov CRD1, [ARG3, CSD1]
    stp CRD1, NUCD1 [sp, #-2]!
    stp NUCD2, NUCD3 [sp, #-2]!

    cmp LENW, #0
    b.eq 3
    b.ne 2

3:
    mov CRD1, xzr
    mov CSD1, xzr
    mov CSD2, xzr

4:   
    cmp CRD2, #0
    b.eq translate_n2p_set_trip_fin
    b.ne 5

5:
    ldp CRD1, NUCD1 [sp], #2
    ldp NUCD2, NUCD3 [sp], #2
    sub CRD2, #1
    cmp CSD1, CSD2
    b.gt translate_p2n_set_trip_temp
    b.lt 4

6:
    lsl NUCW1, NUCW1, #3
    lsl NUCW2, NUCW2, #3
    lsl NUCW3, NUCW3, #3
    
    mov CRW1, decodedvals
    lsr NUCW1, CRD1, NUCW1
    lsr NUCW2, CRD1, NUCW2
    lsr NUCW3, CRD1, NUCW3

    strb NUCW1, [ARG4], #1
    strb NUCW2, [ARG4], #1
    strb NUCW3, [ARG4], #1

    bl L_translate_p2n

7:
    ret

// extern void transgtca_revtranslate(char *protein, size_t *triplets_lut, size_t *freqs_lut)
transgtca_revtranslate:
    str lr, [sp, -#8]!            
    stp CSD1, CSD2, [sp, #-16]!
    stp SPTR, TPTR,  [sp, #-16]!
    stp FPTR, RPTR, [sp, #-16]!
   
    mov SPTR, ARG1      
    mov  TPTR, ARG2              
    mov FPTR, ARG3              

    mov ARG1, SPTR
    bl stlen
    mul ARG1, ARG1, #3
    mov ARG2, #8
    stp SPTR, TPTR,  [sp, #-16]!
    bl dynoalloc
    ldp SPTR, TPTR,  [sp], #16
    mov RPTR, RETR
                      
    mov ENCD, xzr
    mov NUCD1, xzr            
    mov NUCD2, xzr            
    mov NUCD3, xzr  
    mov PEPD, xzr
    
    mov ARG1, SPTR
    mov ARG2, TPTR
     mov ARG3, FPTR
    mov ARG4, RPTR
    bl L_translate_p2n

    ldr FPTR, RPTR, [sp], #16
    ldr SPTR, TPTR  [sp], #16 
    ldr CSD1, CSD2, [sp], #16
    ldr lr, [sp], #8            
    ret
