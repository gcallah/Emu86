; Declare arrays x, y, z
; y is an array of size 13, holding element 50
; z is an array of the ASCII values of 'hello', ends in 0 
.data
    x: .byte 3, 8, 5, 2
    y: .short 13 DUP (-50)
    z: .long 'hello', 0

; Store array values
.text
    mov (x), %eax 
    mov 4(y), %ebx
    mov 3(z), %ecx
    mov 2(x), %edx