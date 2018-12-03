; Declare a number
.data
    number: .word 0x2F7

; Calculating log (base 2) of a number
.text
    0x40000 ADD X8, X8, X0
    0x40004 ADDI X9, X9, 1
    0x40008 LW X10, 0(X28)

WHILELE: 0x4000C SUB X11, X9, X10


BODY:    0x40010 ADD X9, X9, X9
         0x40014 ADDI X8, X8, 1
         0x40018 SLT X12, X0, X11
         0x4001C BNE X12, X0, -5


ENDWHILELE: 0x40020 ADDI X8, X8, -1