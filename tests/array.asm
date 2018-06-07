; Declare arrays x, y, z
; y is an array of size 13, holding element 50
; z is an array of the ASCII values of 'hello', ends in 0 
.data
    x DB 3, 8, 5, 2
    y DW 13 DUP (50)
    z DD 'hello', 0

; Store first element of x into EAX 
; Store fifth element of y into EBX
; Store fourth element of z into ECX 
; Store third element of x into EDX
.text
    mov eax, x 
    mov ebx, y[4]
    mov ecx, z[3]
    mov edx, x[2]