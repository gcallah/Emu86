; First comes the data section, where we declare some array names.
.data
    x DB 3, 8, 5, 2
    y DW 13 DUP (50)
    z DD 'hello', 0

; Next is the .text section, where we use them:
.text
    mov eax, x 
    mov ebx, y[4]
    mov ecx, z[3]
    mov edx, x[2]