; Compare R8 and R9 and loop until equal
; When done, store R9 to R11
    40000 ADDI R8, R0, 10
    40004 ADD R9, R0, R0
    40008 ADDI R9, R9, 1
    4000C ADDI R10, R10, -1
    40010 BNE R8, R9, -3
    40014 ADD R11, R11, R9