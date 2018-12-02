    mov $0, %eax
    jmp label1
    dec %eax
label1: inc %eax

    mov $0, %ebx
    cmp $0, %ebx
    je label2
    dec %eax
label2: inc %eax

    mov $1, %ebx
    cmp $0, %ebx
    je label3
    dec %eax
label3: inc %eax

    mov $1, %ebx
    cmp $0, %ebx
    jne label4
    dec %eax
label4: inc %eax
