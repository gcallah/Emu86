; Declare number and sum.
.data
    number DW 0x40600000
    sum DW ?

; Store first number to F7
; Add 0x9E to value in F7
; Store total to sum
.text
    mov F7, [number]
    add F7, 0x9E
    mov [sum], F7
