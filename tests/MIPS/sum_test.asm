; Declare number and sum.
.data
    number: .word -0x69
    sum: .word 0

; Store first number to R8
; Add 158 to value in R8
; Store total to sum
.text
    LW R8, number(R28)		
    ADDI R8, R8, 0x9E	
    SW R8, sum(R28)