; Declare number and sum.
.data
    number DW -105
    sum DW ?

; Store first number to EAX
; Add 158 to value in EAX
; Store total to sum
.text
    mov eax, [number]
    add eax, 158
    mov [sum], eax

