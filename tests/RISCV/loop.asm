; Compare X8 and X9 and loop until equal
; When done, store X9 to X11
    0x40000 ADDI X8, X0, 10
    0x40004 ADD X9, X0, X0
    0x40008 ADDI X9, X9, 1
    0x4000C ADDI X10, X10, -1
    0x40010 BNE X8, X9, -3
    0x40014 ADD X11, X11, X9