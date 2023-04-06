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

    decode_shifts:
        .align 1
        .byte 0, 0, 2, 0
    
    .global transgtca_translate
    .global transgtca_revtranslate

    #define NUCW1  w9
    #define NUCW2  w10
    #define NUCW3  w11
    #define NUCX1  x9
    #define NUCX2  x10
    #define NUCX3  x11
    #define PEPW   w12
    #define PEPX   x12
    #define ENCW   w13
    #define ENCX   x13   
    #define LENW   w14
    #define LENX   x14

    #define SPTR   x4
    #define TPTR   x5
    #define FPTR   x6
    #define RPTR   x7
    #defome LENV   #x0

    #define ARG1   x0
    #define ARG2   x1
    #define ARG3   x2
    #define ARG4   x3
    #define ARG5   x4
    #define ARG6   x5
    #define RETR   x0
    #define SYSC   x8

    #define CSX1  x25
    #define CSX2  x26
    #define CSW1  w25
    #define CSW2  w26

    #define CRX1  x10
    #define CRX2  x11
    #define CRW1  w10
    #define CRW2  w11

    #define BYTEW   w14
    #define BYTEX   x14



.text

/*           Translate        */

translate_n2p:
    ldrb NUCW1, [ARG1], #1     
    ldrb NUCW2, [ARG1], #1  
    ldrb NUCW3, [ARG1], #1     

    cmp NUCW1, #0
    b.eq translate_n2p_fin

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

    b.ne translate_n2p  

translate_n2p_fin:
    strb #0, [ARG3], #1 
    ret


transgtca_translate:
    str lr, [sp, -#8]!            
    stp CSX1, CSX2, [sp, -16]!

    mov SPTR, ARG1              
    mov ARG1, SPTR
    bl stlen
    udiv ARG1, ARG1, #3        
    mov ARG2, #8              
    bl dynoalloc
    mov RPTR, RETR              

    mov NUCX1, xzr            
    mov NUCX2, xzr            
    mov NUCX3, xzr      
    mov PEPX, xzr

    mov ARG1, SPTR
    mov ARG2, TPTR
    mov ARG3, RPTR
    bl translate_n2p    

    mov RETR, ARG3              
    ldr CSX1, CSX2, [sp], #16
    ldr lr, [sp], #8            
    ret


/*        Reverse Translate         */

translate_p2n:
    ldrb PEPW, [ARG1], #1

    sub PEPW, #64
    ldr ENCX, [ARG2, PEPW]

    ubfx LENW, ENCX, #60, #4
    mov CRX1, xzr
translate_p2n_decode_loop:
    ubfx BYTEX, ENCX, CRX1, #6       
    add CRX1, CRX1, #6            
    sub LENW, LENW, #1            
    
    ubfx , x14, #0, #2       
    ubfx x16, x14, #2, #2       
    ubfx x17, x14, #4, #2       

    and x15, x15, x15, lsl #

translate_p2n_decode_fin:


transgtca_revtranslate:
    str lr, [sp, -#8]!            
    stp CSX1, CSX2, [sp, -16]!
   
    mov SPTR, ARG1              
    mov TPTR, ARG2              
    mov FPTR, ARG3              

    mov ARG1, SPTR
    bl stlen
    mul ARG1, ARG1, #3
    mov ARG2, #8
    bl dynoalloc
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
    bl translate_p2n
    
    
    ldr CSX1, CSX2, [sp], #16
    ldr lr, [sp], #8            
    ret


/*          Utils           */

stlen: 
    str CSX1, [sp]           
    mov CSX1, ARG1             
    ldrb BYTE, [CSX1], #1      
    cmp BYTE, #0              
    b.eq strlen_fin         
    b.ne stlen              
stlen_fin:
    sub RETR, CSX1, ARG1         
    ldr CSX1, [sp]           
    ret




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




dynorealloc:
    mul ARG2, ARG2, ARG4           
    mul ARG3, ARG3, ARG4      
    
    mov SYSC, SYS_mremap      
    mov ARG4, #0              
    mov ARG5, xzr             
    svc #0                  

    
    ret




dynounalloc:
    mul ARG2, ARG2, ARG3

    mov SYSC, SYS_munmap       
    svc #0

    ret