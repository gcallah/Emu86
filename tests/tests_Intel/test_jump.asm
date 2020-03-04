    mov eax, 0
    jmp label1
    dec eax
label1: inc eax

    mov ebx, 0
    cmp ebx, 0
    je label2
    dec eax
label2: inc eax

    mov ebx, 1
    cmp ebx, 0
    je label3
    dec eax
label3: inc eax

    mov ebx, 1
    cmp ebx, 0
    jne label4
    dec eax
label4: inc eax
