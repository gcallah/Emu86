; In R8, we put the number to raise to the power we put in R9.
      0x400000 ADDI X8, X0, 2
      0x400004 ADDI X9, X9, 0x10
      0x400008 JAL X31, 0x8
      0x40000C SYSCALL

power: 0x400010 ADD X16, X0, X8
loop: 0x400014 MUL X8, X8, X16
      0x40001C ADDI X9, X9, -1
      0x400020 ADDI X10, X0, 1
      0x400024 BNE X9, X10, -4
      0x400028 JR X31