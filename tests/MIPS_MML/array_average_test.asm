; Create an array
    3FFF4 ADDI R7, R0, A
    3FFF8 SW R7, 104(R0)
    3FFFC ADDI R6, R0, 0
    40000 ADDI R7, R0, 19
    40004 SW R7, R6(R0)
    40008 ADDI R6, R6, 4
    4000C ADDI R7, R0, 2F
    40010 SW R7, R6(R0)
    40014 ADDI R6, R6, 4
    40018 ADDI R7, R0, -F
    4001C SW R7, R6(R0)
    40020 ADDI R6, R6, 4
    40024 ADDI R7, R0, -32
    40028 SW R7, R6(R0)
    4002C ADDI R6, R6, 4
    40030 ADDI R7, R0, 20
    40034 SW R7, R6(R0)
    40038 ADDI R6, R6, 4
    4003C ADDI R7, R0, A
    40040 ADDI R14, R14, 5
    40044 BEQ R14, R0, 4
    40048 SW R7, R6(R0)
    4004C ADDI R6, R6, 4
    40050 ADDI R14, R14, -1
    40054 J 100110

; Calculate the average of the array:
    40058 ADD R8, R0, R0
    4005C ADD R9, R0, R0
    40060 LW R16, 104(R28)
    40064 ADD R10, R0, R0
    40068 BEQ R9, R16, 5
    4006C LW R11, (R10)
    40070 ADD R8, R8, R11
    40074 ADDI R9, R9, 1
    40078 ADDI R10, R10, 4
    4007C J 1001A0
    40080 DIV R8, R16
    40084 MFLO R12
    40088 MFHI R13
