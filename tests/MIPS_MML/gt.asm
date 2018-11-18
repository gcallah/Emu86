    40000 ADD R8, R8, R0
    40004 ADDI R9, R9, 10

; compare R8 and R9 and loop until R8 greater than R9
    40008 SUB R10, R8, R9
    4000C SLT R11, R0, R10
    40010 ADDI R12, R0, 1
    40014 BEQ R11, R12, 2
    40018 ADDI R8, R8, 1
    4001C J 100020

; when done, store R9 in R13
    40020 ADD R13, R9, R0
    40024 ADDI R14, R0, 1B
    40028 ANDI R14, R14, 17
