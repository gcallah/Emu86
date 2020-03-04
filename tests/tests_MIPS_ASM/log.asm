; Declare a number
.data
    number: .word 0x2F7

; Calculating log (base 2) of a number
.text
    0x40000 ADD R8, R8, R0
    0x40004 ADDI R9, R9, 1
    0x40008 LW R10, 0(R28)

WHILELE: 0x4000C SUB R11, R9, R10
         0x40010 SLT R12, R0, R11
         0x40014 BNE R12, R0, 3
BODY: 0x40018 ADD R9, R9, R9
      0x4001C ADDI R8, R8, 1
      0x40020 J 0x100030

ENDWHILELE: 0x40024 ADDI R8, R8, -1