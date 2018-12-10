; Declare a number
.data
    number: .word 0x2F7

; Calculating log (base 2) of a number
.text
    0x40000 ADD X8, X8, X0
    0x40004 ADDI X9, X9, 1
    0x40008 LW X10, 0(X28)

WHILELE: 0x4000C SUB X11, X9, X10
         0x40010 SLT X12, X0, X11
         0x40014 BNE X12, X0, 3
BODY: 0x40018 ADD X9, X9, X9
      0x4001C ADDI X8, X8, 1
      0x40020 BEQ X0, X0, -6

ENDWHILELE: 0x40024 ADDI X8, X8, -1
