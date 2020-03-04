; Calculate -(x + y - 2 * z + 1)
; x = 35, y = 47, z = 26

    40000 ADDI R8, R0, 23
    40004 ADDI R9, R9, 2F
    40008 ADD R8, R8, R9
    4000C ADDI R10, R0, 1A
    40010 ADD R10, R10, R10
    40014 SUB R8, R8, R10
    40018 ADDI R8, R8, 1
    4001C SUB R8, R0, R8