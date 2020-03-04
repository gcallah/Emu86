; Store first addend
    40000 ADDI R7, R0, 69
    40004 SW R7, 20(R28)

; Load first number to R8
; Add 158 to value in R8
; Store sum to next location
    40008 LW R8, 20(R28)		
    4000C ADDI R8, R8, 9E	
    40010 SW R8, 24(R28)