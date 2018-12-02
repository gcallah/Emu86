         0x40000 ADD X8, X8, X0
         0x40004 ADDI X9, X9, 10

; compare X8 and X9 and loop until X8 greater than X9
LOOP: 0x40008 SUB X10, X8, X9
      0x4000C SLT X11, X0, X10
      0x40010 ADDI X12, X0, 1
      0x40014 BEQ X11, X12, 2
      0x40018 ADDI X8, X8, 1
      0x4001C Jr LOOP

; when done, store X9 in X13
DONE: 0x40020 ADD X13, X9, X0
      0x40024 ADDI X14, X0, 1B
      0x40028 ANDI X14, X14, 17
