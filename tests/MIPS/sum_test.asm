; Declare number and sum.
.data
    number: .word -69
    sum: .word 0

; Store first number to R8
; Add 158 to value in R8
; Store total to sum
.text
    40000 LW R8, number(R28)		
    40004 ADDI R8, R8, 9E	
    40008 SW R8, sum(R28)