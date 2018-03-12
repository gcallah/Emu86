    mov eax, 0
    jmp label1
    dec eax
label1: inc eax

    mov eax, 0
    cmp eax, 0
    je label2
    dec eax
label2: inc eax

    mov eax, 1
    cmp eax, 0
    je label3
    dec eax
label3: inc eax

    mov eax, 0
    cmp eax, 0
    jne label4
    dec eax
label4: inc eax
