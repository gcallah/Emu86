; Declare x, y, and z variables 
.data
    x: .word 23
    y: .word 2F
    z: .word 1A

; Calculate -(x + y - 2 * z + 1)
.text
    40000 LW R8, 0(R28)
    40004 LW R9, 4(R28)
    40008 ADD R8, R8, R9
    4000C LW R10, 8(R28)
    40010 ADD R10, R10, R10
    40014 SUB R8, R8, R10
    40018 ADDI R8, R8, 1
    4001C SUB R8, R0, R8