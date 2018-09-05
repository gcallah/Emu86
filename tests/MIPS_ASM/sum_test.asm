; Declare number and sum.
.data
    number: .word -0x69
    sum: .word 0

; Store first number to R8
; Add 158 to value in R8
; Store total to sum
.text
    0x40000 LW R8, 0(R28)		
    0x40004 ADDI R8, R8, 0x9E	
    0x40008 SW R8, 4(R28)