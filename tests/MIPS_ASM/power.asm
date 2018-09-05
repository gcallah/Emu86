; In R8, we put the number to raise to the power we put in R9.
      0x400000 ADDI R8, R0, 2
      0x400004 ADDI R9, R9, 10
      0x400008 JAL 0x1000040
      0x40000C SYSCALL

power: 0x400010 ADD R16, R0, R8
loop: 0x400014 MULT R8, R16
      0x400018 MFLO R8
      0x40001C ADDI R9, R9, -1
      0x400020 ADDI R10, R0, 1
      0x400024 BNE R9, R10, -5
      0x400028 JR R31