    mov 0, %eax
    jmp label1
    dec %eax
label1: inc %eax

    mov 0, %ebx
    cmp %ebx, 0
    je label2
    dec %eax
label2: inc %eax

    mov 1, %ebx
    cmp %ebx, 0
    je label3
    dec %eax
label3: inc %eax

    mov 1, %ebx
    cmp %ebx, 0
    jne label4
    dec %eax
label4: inc %eax

