         0x40000 ADD R8, R8, R0
         0x40004 ADDI R9, R9, 10

; compare R8 and R9 and loop until R8 greater than R9
LOOP: 0x40008 SUB R10, R8, R9
      0x4000C SLT R11, R0, R10
      0x40010 ADDI R12, R0, 1
      0x40014 BEQ R11, R12, 2
      0x40018 ADDI R8, R8, 1
      0x4001C J LOOP

; when done, store R9 in R13
DONE: 0x40020 ADD R13, R9, R0
      0x40024 ADDI R14, R0, 1B
      0x40028 ANDI R14, R14, 17
