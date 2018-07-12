; Declare a number
.data
    number: .word 100

; Calculate square root of the number
.text
    LW R8, number(R28)

WHILELE: ADD R10, R0, R9
         MULT R10, R9
         MFLO R10
         SUB R11, R10, R8
         SLT R12, R0, R11
         BNE R12, R0, 2
         ADDI R9, R9, 1
         J WHILELE
ENDWHILELE: SUBI R9, R9, 1
            ADD R8, R0, R9
            