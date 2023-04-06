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
    
    .global transgtca_nuc2pep
    .global transgtca_pep2nuc


.text

// Translate DNA to Protein

translate_n2p:
    ldrb w0, [x5], #1       // nuc1 = dna[i] && i++
    ldrb w1, [x5], #1       // nuc2 = dna[i] && i++
    ldrb w2, [x5], #1       // nuc3 = dna[i] && i++

    cmp x0, #0
    b.eq translate_n2p_fin  // finish if nuc1 == 0

    and w0, w0 lsr #1, #3   // 3 & (nuc1 >> 1)
    and w1, w1 lsr #1, #3   // 3 & (nuc2 >> 1)
    and w2, w2 lsr #1, #3   // 3 & (nuc3 >> 1)

    mov w8, wzr             // enc_index = 0
    orr w8, w8, w0 lsl #4   // enc_index |= nuc1 << 4
    orr w8, w8, w1 lsl #2   // enc_index |= nuc2 << 2
    orr w8, w8, w2          // enc_index |= nuc3

    mov x3, [x6, w8]        // pep = genetic_table[enc_index]
    str x3, [x7], #1        // result[n] = pep && n++

    b.ne translate_n2p      // loop if string is not done

translate_n2p_fin:
    str xzr, [x7], #1       // null-terminate string
    ret

transgtca_nuc2pep:
    str lr, [sp]            // store link register on stack
    mov x5, x0              // pointer to DNA string
    mov x6, x1              // pointer to genetic table

    // get strlen, calloc space for result
    bl stlen
    udiv x0, x0, #3         // divide stlen by 3 to fit 3nuc = 1pep
    mov x1, #8              // 8 for number of bit in a byte
    bl dyalloc
    mov x7, x0              // pointer to result

    mov x0, xzr             // nuc1 = 0
    mov x1, xzr             // nuc2 = 0
    mov x2, xzr             // nuc3 = 0
    mov x3, xzr             // pep = 0

    str lr, [sp]            // store link register on stack
    bl translate_n2p
    
    ldr lr, [sp]            // load link register back
    mov x7, x0              // retuurn pointer to result string
    ret


// Reverse-Translate Protein to DNA

translate_p2n:
    ldrb x1, [x6], #1       // sc_nuc1 = dna[i] && i++
    ldrb x2, [x6], #1       // sc_nuc2 = dna[i] && i++
    ldrb x3, [x6], #1       // sc_nuc3 = dna[i] && i++

    ldrb x0, [x5]


transgtca_pep2nuc:
    strp x12, x13, [sp], -16    // possible triplet 1 & 2
    strp x14, x15, [sp], -16    // possible triplet 3 & 4
    strp x16, x17, [sp], -16    // possible triplet 5 & 6
    strp x18, x19, [sp], -16    // possible triplet 7 & 8
    strp x20, x21, [sp], -16    // possible triplet 9 & 10
    
    mov x5, x0              // pointer to original protein string
    mov x6, x1              // pointer to scrutinized nucleotide string
    mov x7, x2              // pointer to genetic table

    mov x0, xzr             // pep = 0
    mov x1, xzr             // sc_nuc1 = 0
    mov x2, xzr             // sc_nuc2 = 0
    mov x3, xzr             // sc_nuc3 = 0
    mov x4, xzr             // possible_trip_len = 0
    mov x8, xzr             // non-m

    str lr, [sp, -8]        // store link register on stack

    ldr lr, [sp, -8]        // load link register back


// in -> x5 = address to string
// out -> x0 = string length
stlen: 
    str x10, [sp]           // callee-save x10
    mov x5, x10             // make a copy of str pointer  
    ldrb w0, [x10], #1      // c = *str++    
    cmp w0, #0              // c == \0?
    b.eq strlen_fin         // if so, jump to return
    b.ne stlen              // otherwise, continue
stlen_fin:
    sub x0, x10, x5         // len = *str after inc - original *str
    ldr x10, [sp]           // restore x10
    ret


// in -> x0 = len; x1 = number of bits
// out -> x0: new address pointer
dyalloc:
    stp x11, x8, [sp], 16   // callee-save x0, x1
    stp x2, x3, [sp], 16    // callee-save x2, x3
    stp x4, x5, [sp], 16    // callee-save x4, x5
    
    mov x0, x11             // len to x11
    mul x11, x8             // multiply size by number of bits

    mov x8, SYS_mmap        // mmap syscall to x8
    mov x0, xzr             // addr = null
    mov x1, x11             // size = x11
    mov x2, PROT_RXW        // prot = Read/Exec/Write PROT flag
    mov x3, MAP_FLAGS       // flags = MAP_FLAGS
    mov x4, FD_NULL         // fd = -1
    mov x5, #0              // offset = 0
    svc #0                  // execute syscall to mmap
    
    // now pointer to dynamically-allocated string is in x0
    stp x4, x5, [sp], 16    // restore x4, x5       
    stp x2, x3, [sp], 16    // restore x2, x3
    stp x11, x8, [sp], 16   // restore x0, x1
    ret


// in -> x0 = old pointer; x1 = old size; x2 = new size; x3 = number of bits
// out -> x0 = new pointer
dynorealloc:
    mul x1, x1, x3           // multiply old size by bits num
    mul x2, x2, x3           /// multiply new size by bitnum
    
    mov x8, SYS_mremap      // mremap sycall to x8
    mov x3, #0              // flags
    mov x4, xzr             // new addr = null
    svc #0                  // execute mremap

    // address to reallocated memory is saved in x0
    ret


// in -> x0 = address; x1 = size; x2 = bit num
dynounalloc:
    mul x1, x1, x2

    mov x8, SYS_munmap       // munmap syscall to x
    svc #0

    ret