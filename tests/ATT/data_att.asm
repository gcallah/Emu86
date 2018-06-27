; First comes the data section, where we declare some names.
.data
    x: .byte 8
    y: .short 16
    z:. long 32

; Next is the .text section, where we use them:
.text
    mov (x), %eax
    mov (y), %ebx
    mov (z), %ecx
