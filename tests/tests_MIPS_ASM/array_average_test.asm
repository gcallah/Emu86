; Declare an array and declare size of the array
.data
    nbrArray: .word 0x19, 0x2F, -0xF, -0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA
    nbrElts: .word 0xA

; Calculate the average of the array:
.text
    0x40000 ADD R8, R0, R0
    0x40004 ADD R9, R0, R0
    0x40008 LW R16, 28(R28)
    0x4000C ADD R10, R0, R0
FORCOUNT: 0x40010 BEQ R9, R16, 5
BODY: 0x40014 LW R11, (R10)
      0x40018 ADD R8, R8, R11
      0x4001C ADDI R9, R9, 1
      0x40020 ADDI R10, R10, 4
      0x40024 J 0x10004
ENDCOUNT: 0x40028 DIV R8, R16
0x4002C MFLO R12
0x40030 MFHI R13
