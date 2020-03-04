; Declare number and sum.
.data
    number: .word -0x69
    sum: .word 0

; Store first number to X8
; Add 158 to value in X8
; Store total to sum
.text
    0x40000 LW X8, 0(X28)		
    0x40004 ADDI X8, X8, 0x9E	
    0x40008 SW X8, 4(X28)
