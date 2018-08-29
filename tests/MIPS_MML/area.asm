; Calculate area of rectangle
    40000 ADDI R8, R0, 23
    40004 ADDI R9, R0, 1B
    40008 MULT R8, R9
    4000C MFLO R10
    40010 SW R10, 1000(R0)