; In R8, we put the number to raise to the power we put in R9.
      0x400000 ADDI X8, X0, 2
      0x400004 ADDI X9, X9, 10
      0x400008 ADD X16, X0, X8
loop: 0x40000C MUL X8, X8, X16
      0x400010 ADDI X9, X9, -1
      0x400014 ADDI X10, X0, 1
      0x400018 BNE X9, X10, -4
      0x40001C SYSCALL