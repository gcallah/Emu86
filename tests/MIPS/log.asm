; Declare a number
.data
    number: .word 759

; Calculating log (base 2) of a number
.text
    ADD R8, R8, R0
    ADDI R9, R9, 1
    LW R10, number(R28)

WHILELE: SUB R11, R9, R10
         SLT R12, R0, R11
         BNE R12, R0, 3
BODY: ADD R9, R9, R9
      ADDI R8, R8, 1
      J WHILELE

ENDWHILELE: ADDI R8, R8, -1