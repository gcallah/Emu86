; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray: .word 0x19, 0x2F, 0xF, 0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA
    nbrElts: .word 0xA
    nbrMin: .word 0x21

; Change any numbers less than min to min:
.text
    0x40000 ADD R8, R0, R0
    0x40004 ADD R9, R0, R0
    0x40008 ADD R10, R0, R0
    0x4000C ADD R11, R0, R0
    0x40010 LW R16, 0x2C(R28)
    0x40014 LW R17, 0x28(R28)
FORCOUNT: 0x40018 BEQ R10, R17, 9
BODY: 0x4001C LW R12, (R9)
      0x40020 SLT R13, R16, R12
      0x40024 BNE R13, R0, 1
      0x40028 SW R16, (R9)
ENDIFSMALL: 0x4002C LW R11, (R9)
            0x40030 ADD R8, R8, R11
            0x40034 ADDI R9, R9, 4
            0x40038 ADDI R10, R10, 1
            0x4003C J 0x10006
ENDCOUNT: 0x40040 ADD R13, R0, R8