.arch armv8-a

.data

    .equ NUM_TRPS, 64
    .equ PROT_RXW, 7
    .equ MAP_FLAGS, 22
    .equ FD_NULL, -1
    .equ OFFSET, 0
    .equ SYS_munmap, 215
    .equ SYS_mremap, 216
    .equ SYS_mmap, 222

    .set NUCW1,  w9
    .set NUCW2,  w10
    .set NUCW3,  w11
    .set NUCX1,  x9
    .set NUCX2,  x10
    .set NUCX3,  x11
    .set PEPW,   w12
    .set PEPX,   x12
    .set ENCW,   w13
    .set ENCX,   x13   
    .set LENW,   w14
    .set LENX,   x14

    .set SPTR,   x20
    .set TPTR,   x21
    .set FPTR,   x22
    .set RPTR,   x23

    .set ARG1,   x0
    .set ARG2,   x1
    .set ARG3,   x2
    .set ARG4,   x3
    .set ARG5,   x4
    .set ARG6,   x5
    .set RETR,   x0
    .set SYSC,   x8

    .set CSX1,  x25
    .set CSX2,  x26
    .set CSW1,  w25
    .set CSW2,  w26

    .set CRX1,  w15
    .set CRX2,  x16
    .set CRW1,  w16
    .set CRX2,  x16
   
    .set BYTEW, w18
    .set BYTEX, x18

    decode_shifts:
        .word 0x47544341
    
    .global transgtca_translate
    .global transgtca_revtranslate



.text

/*           Translate        */

// void L_translate_p2n(char *dna, size_t *peptide_lut, char *res)
L_translate_n2p:
    ldrb NUCW1, [ARG1], #1     
    ldrb NUCW2, [ARG1], #1  
    ldrb NUCW3, [ARG1], #1     

    cmp NUCW1, #0
    b.eq 1

    lsr NUCW1, NUCW1, #1  
    lsr NUCW2, NUCW2, #1  
    lsr NUCW3, NUCW3, #1   
    and NUCW1, NUCW1, #3 
    and NUCW2, NUCW2, #3  
    and NUCW3, NUCW3, #3 

    mov ENCW, wzr        
    orr ENCW, ENCW, NUCW1 lsl #4  
    orr ENCW, ENCW, NUCW2 lsl #2 
    orr ENCW, ENCW, NUCW3   

    mov PEPW, [ARG2, ENCW]     
    strb PEPW, [ARG3], #1   

    b.ne L_translate_n2p  

1:
    strb #0, [ARG3], #1 
    ret

// char *transgtca(char *dna, size_t *peptide_lut)
transgtca_translate:
    str lr, [sp, -#8]!            
    stp CSX1, CSX2, [sp, #-16]!
    stp SPTR, TPTR, [sp, #-16]!
    stp FPTR, RPTR, [sp, #-16]!

    mov SPTR, ARG1
    mov TPTR, ARG2

    mov ARG1, SPTR
    bl stlen
    udiv ARG1, ARG1, #3        
    mov ARG2, #8  
    stp SPTR, TPTR, [sp, #-16]!
    bl dynoalloc
    ldp SPTR, TPTR, [sp], #16
    mov RPTR, RETR      
    ldr ARG2, [sp], #8        

    mov NUCX1, xzr            
    mov NUCX2, xzr            
    mov NUCX3, xzr      
    mov PEPX, xzr

    mov ARG1, SPTR
    mov ARG2, TPTR
    mov ARG3, RPTR
    bl L_translate_n2p    

    mov RETR, ARG3             
    ldr FPTR, RPTR, [sp], #16
    ldr SPTR, TPTR [sp], #16 
    ldr CSX1, CSX2, [sp], #16
    ldr lr, [sp], #8            
    ret


/*        Reverse Translate         */


// void L_translate_p2n(char *protein, size_t *triplets_lut, size_t *freqs_lut, char *res)
L_translate_p2n:
    ldrb PEPW, [ARG1], #1
    cmp PEPW, #0
    b.eq 7
    b.ne 1

    mov CRX1, xzr
    mov CRX2, xzr
    mov CSX1, xzr
    mov CSX2, xzr

1:
    sub PEPW, #64
    ldr ENCX, [ARG2, PEPW]

    ubfx LENW, ENCX, #60, #4
    mov CRW2, LENW

2:    
    ubfx BYTEX, ENCX, CRX1, #6       
    add CRX1, CRX1, #6            
    sub LENW, LENW, #1            
    
    ubfx NUCX1, BYTEX, #0, #2       
    ubfx NUCX2, BYTEX, #2, #2       
    ubfx NUCX3, BYTEX, #4, #2   

    mov CSX1, NUCX1
    orr CSX1, CSX1, NUCX3, lsl #1
    eor CSX1, CSX1, NUCX3
    orr CXS1, CSX1, PEPX, lsl #3

    mov CRX1, [ARG3, CSX1]
    stp CRX1, NUCX1 [sp, #-2]!
    stp NUCX2, NUCX3 [sp, #-2]!

    cmp LENW, #0
    b.eq 3
    b.ne 2

3:
    mov CRX1, xzr
    mov CSX1, xzr
    mov CSX2, xzr

4:   
    cmp CRX2, #0
    b.eq translate_n2p_set_trip_fin
    b.ne 5

5:
    ldp CRX1, NUCX1 [sp], #2
    ldp NUCX2, NUCX3 [sp], #2
    sub CRX2, #1
    cmp CSX1, CSX2
    b.gt translate_p2n_set_trip_temp
    b.lt 4

6:
    lsl NUCW1, NUCW1, #3
    lsl NUCW2, NUCW2, #3
    lsl NUCW3, NUCW3, #3
    
    mov CRW1, decode_shifts
    lsr NUCW1, CRX1, NUCW1
    lsr NUCW2, CRX1, NUCW2
    lsr NUCW3, CRX1, NUCW3

    strb NUCW1, [ARG4], #1
    strb NUCW2, [ARG4], #1
    strb NUCW3, [ARG4], #1

    bl L_translate_p2n

7:
    ret

// extern char *transgtca_revtranslate(char *protein, size_t *triplets_lut, size_t *freqs_lut)
transgtca_revtranslate:
    str lr, [sp, -#8]!            
    stp CSX1, CSX2, [sp, #-16]!
    stp SPTR, TPTR, [sp, #-16]!
    stp FPTR, RPTR, [sp, #-16]!
   
    mov SPTR, ARG1      
    mov TPTR, ARG2              
    mov FPTR, ARG3              

    mov ARG1, SPTR
    bl stlen
    mul ARG1, ARG1, #3
    mov ARG2, #8
    stp SPTR, TPTR, [sp, #-16]!
    bl dynoalloc
    ldp SPTR, TPTR, [sp], #16
    mov RPTR, RETR
                      
    mov ENCX, xzr
    mov NUCX1, xzr            
    mov NUCX2, xzr            
    mov NUCX3, xzr  
    mov PEPX, xzr
    
    mov ARG1, SPTR
    mov ARG2, TPTR
    mov ARG3, FPTR
    mov ARG4, RPTR
    bl L_translate_p2n

    ldr FPTR, RPTR, [sp], #16
    ldr SPTR, TPTR [sp], #16 
    ldr CSX1, CSX2, [sp], #16
    ldr lr, [sp], #8            
    ret


/*          Utils           */


// stlen(char *null_terminate_str)
stlen: 
    str CSX1, [sp]           
    mov CSX1, ARG1             
    ldrb BYTE, [CSX1], #1      
    cmp BYTE, #0              
    b.eq strlen_fin         
    b.ne stlen              
1:
    sub RETR, CSX1, ARG1         
    ldr CSX1, [sp]           
    ret



// void *dynoalloc(size_t size, size_t bitnum)
dynoalloc:
    str CSX1, [sp, #8]!
    
    mov CX1, ARG1             
    mul CX1, CX1, ARG2             

    mov SYSC, SYS_mmap        
    mov ARG1, xzr             
    mov ARG2, CX1             
    mov ARG3, PROT_RXW        
    mov ARG4, MAP_FLAGS       
    mov ARG5, FD_NULL         
    mov ARG6, #0              
    svc #0                  
    
    
    ldr CSX1, [sp], #8
    ret



// void *dynorealloc(void *ptr, size_t old_size, size_t new_size, size_t bit_num)
dynorealloc:
    mul ARG2, ARG2, ARG4           
    mul ARG3, ARG3, ARG4      
    
    mov SYSC, SYS_mremap      
    mov ARG4, #0              
    mov ARG5, xzr             
    svc #0                  

    
    ret

// void dynounalloc(void *addr, size_t sze, size_t bitnum)
dynounalloc:
    mul ARG2, ARG2, ARG3

    mov SYSC, SYS_munmap       
    svc #0

    ret