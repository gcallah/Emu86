; First comes the data section, where we declare some names.
.data
    x: .byte 8
    y: .short 16
    z: .long 32

; Next is the .text section, where we use them:
.text
    mov eax, x
    mov ebx, y
    mov ecx, z
