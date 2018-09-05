; Compare R8 and R9 and loop until equal
; When done, store R9 to R11
    0x40000 ADDI R8, R0, 10
    0x40004 ADD R9, R0, R0
    0x40008 ADDI R9, R9, 1
    0x4000C ADDI R10, R10, -1
    0x40010 BNE R8, R9, -3
    0x40014 ADD R11, R11, R9