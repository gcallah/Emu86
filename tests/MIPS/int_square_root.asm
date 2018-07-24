; Declare a number
.data
    number: .word 64

; Calculate square root of the number
.text
    40000 LW R8, number(R28)

WHILELE: 40004 ADD R10, R0, R9
         40008 MULT R10, R9
         4000C MFLO R10
         40010 SUB R11, R10, R8
         40014 SLT R12, R0, R11
         40018 BNE R12, R0, 2
         4001C ADDI R9, R9, 1
         40020 J WHILELE
ENDWHILELE: 40024 ADDI R9, R9, -1
            40028 ADD R8, R0, R9
            