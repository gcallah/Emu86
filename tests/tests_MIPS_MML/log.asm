; Calculating log (base 2) of 759
    40000 ADD R8, R8, R0
    40004 ADDI R9, R9, 1
    40008 ADDI R10, R0, 2F7

    4000C SUB R11, R9, R10
    40010 SLT R12, R0, R11
    40014 BNE R12, R0, 3
    40018 ADD R9, R9, R9
    4001C ADDI R8, R8, 1
    40020 J 100030

    40024 ADDI R8, R8, -1