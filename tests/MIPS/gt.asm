         ADD R8, R8, R0
         ADDI R9, R9, 10

; compare R8 and R9 and loop until R8 greater than R9
LOOP: SUB R10, R8, R9
      SLT R11, R0, R10
      ADDI R12, R0, 1
      BEQ R11, R12, 2
      ADDI R8, R8, 1
      J LOOP

; when done, store R9 in R13
DONE: ADD R13, R9, R0
      ADDI R14, R0, 1B
      ANDI R14, R14, 17



