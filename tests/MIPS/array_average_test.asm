; Declare an array and declare size of the array
.data
    nbrArray: .word 19, 2F, -0xF, -32, 20, 0A, 0A, 0A, 0A, 0A
    nbrElts: .word 0A

; Calculate the average of the array:
.text
    ADD R8, R0, R0
    ADD R9, R0, R0
    LW R16, nbrElts(R28)
    ADDI R10, R28, nbrArray 
FORCOUNT: BEQ R9, R16, 5
BODY: LW R11, (R10)
      ADD R8, R8, R11
      ADDI R9, R9, 1
      ADDI R10, R10, 4
      J FORCOUNT
ENDCOUNT: DIV R8, R16
MFLO R12
MFHI R13
