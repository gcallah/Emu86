; Compare R8 and R9 and loop until equal
; When done, store R9 to R11
    ADDI R8, R0, 10
    ADD R9, R0, R0
    ADDI R9, R9, 1
    ADDI R10, R10, -1
    BNE R8, R9, -3
    ADD R11, R11, R9