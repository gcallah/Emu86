; Store a number
    40000 ADDI R7, R0, 64
    40004 SW R7, 100(R28)

; Calculate square root of the number
    40008 LW R8, 100(R28)
    4000C ADD R10, R0, R9
    40010 MULT R10, R9
    40014 MFLO R10
    40018 SUB R11, R10, R8
    4001C SLT R12, R0, R11
    40020 BNE R12, R0, 2
    40024 ADDI R9, R9, 1
    40028 J 10001
    4002C ADDI R9, R9, -1
    40030 ADD R8, R0, R9
            