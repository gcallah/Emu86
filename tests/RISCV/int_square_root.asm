; Declare a number
.data
    number: .word 0x64

; Calculate square root of the number
.text
    0x40000 LW X8, 0(X28)

WHILELE: 0x40004 ADD X10, X0, X9
         0x40008 MUL X10, X10, X9
         0x4000C SUB X11, X10, X8
         0x40010 SLT X12, X0, X11
         0x40014 ADDI X9, X9, 1
         0x40018 BEQ X12, X0, -6
ENDWHILELE: 0x4001C ADDI X9, X9, -2
            0x40020 ADD X8, X0, X9
            