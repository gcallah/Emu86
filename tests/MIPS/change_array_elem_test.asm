; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray: .word 19, 2F, 0F, 32, 20, 0A, 0A, 0A, 0A, 0A
    nbrElts: .word 0A
    nbrMin: .word 21

; Change any numbers less than min to min:
.text
    40000 ADD R8, R0, R0
    40004 ADD R9, R0, R0
    40008 ADD R10, R0, R0
    4000C ADDI R11, R0, nbrArray
    40010 LW R16, nbrMin(R28)
    40014 LW R17, nbrElts(R28)
FORCOUNT: 40018 BEQ R10, R17, 9
BODY: 4001C LW R12, (R9)
      40020 SLT R13, R16, R12
      40024 BNE R13, R0, 1
      40028 SW R16, (R9)
ENDIFSMALL: 4002C LW R11, (R9)
            40030 ADD R8, R8, R11
            40034 ADDI R9, R9, 4
            40038 ADDI R10, R10, 1
            4003C J 100060
ENDCOUNT: 40040 ADD R13, R0, R8