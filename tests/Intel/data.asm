; First comes the data section, where we declare some names.
.data
    x DB 8
    y DW 16
    z DD 32

; Next is the .text section, where we use them:
.text
    mov eax, [x]
    mov ebx, [y]
    mov ecx, [z]
