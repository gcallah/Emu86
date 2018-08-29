; Declare an array and declare size of the array
.data
    nbrArray: .word 19, 2F, -0F, -32, 20, 0A, 0A, 0A, 0A, 0A
    nbrElts: .word 0A

; Calculate the average of the array:
.text
    40000 ADD R8, R0, R0
    40004 ADD R9, R0, R0
    40008 LW R16, 28(R28)
    4000C ADD R10, R0, R0
FORCOUNT: 40010 BEQ R9, R16, 5
BODY: 40014 LW R11, (R10)
      40018 ADD R8, R8, R11
      4001C ADDI R9, R9, 1
      40020 ADDI R10, R10, 4
      40024 J 100040
ENDCOUNT: 40028 DIV R8, R16
4002C MFLO R12
40030 MFHI R13
