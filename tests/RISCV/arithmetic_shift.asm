0x400000 ADDI X8, X0, 4
0x400004 ADDI X9, X0, 1
0x400008 SW X9, 0(X8)
0x40000C ADD X10, X0, X8
0x400010 ADDI X11, X0, 2
0x400014 ADDI X12, X0, 8
0x400018 ADDI X13, X0, 10
0x40001C ADD X11, X11, X12
0x400020 SUB X13, X13, X12
0x400024 MUL X10, X10, X9
0x400028 SLLI X9, X9, 2
0x40002C SW X9, 0(X8)