; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray: .word 19, 2F, 0F, 32, 20, 0A, 0A, 0A, 0A, 0A
    nbrElts: .word 0A
    nbrMin: .word 21

; Change any numbers less than min to min:
.text
    ADD R8, R0, R0
    ADD R9, R0, R0
    ADDI R10, R0, nbrArray
    LW R16, nbrMin(R28)
    LW R17, nbrElts(R28)
FORCOUNT: BEQ R9, R17, 8
BODY: LW R11, (R9)
      SLT R12, R16, R11
      BNE R12, R0, 1
      SW R16, (R9)
ENDIFSMALL: LW R11, (R9)
            ADD R8, R8, R11
            ADDI R9, R9, 1
            J FORCOUNT
ENDCOUNT: ADD R13, R0, R8