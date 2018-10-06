; x is the base, y is the power
.data
    x: .float 5.5
    y: .word 0x3

; In F8, we put the number to raise to the power we put in R9.
.text
      0x400000 LWC F8, 0(F28)
      0x400004 LW R9, 4(R28)
      0x400008 JAL 0x1000040
      0x40000C SYSCALL

power: 0x400010 ADD.S F16, F0, F8
loop: 0x400014 MULT.S F8, F16
      0x400018 MFHI F8
      0x40001C ADDI R9, R9, -1
      0x400020 ADDI R10, R0, 1
      0x400024 BNE R9, R10, -5
      0x400028 JR R31