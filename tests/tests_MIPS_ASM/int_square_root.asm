; Declare a number
.data
    number: .word 0x64

; Calculate square root of the number
.text
    0x40000 LW R8, 0(R28)

WHILELE: 0x40004 ADD R10, R0, R9
         0x40008 MULT R10, R9
         0x4000C MFLO R10
         0x40010 SUB R11, R10, R8
         0x40014 SLT R12, R0, R11
         0x40018 BNE R12, R0, 2
         0x4001C ADDI R9, R9, 1
         0x40020 J 0x10001
ENDWHILELE: 0x40024 ADDI R9, R9, -1
            0x40028 ADD R8, R0, R9
            