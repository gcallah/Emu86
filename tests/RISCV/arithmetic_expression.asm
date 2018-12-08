; Declare x, y, and z variables 
.data
    x: .word 0x23
    y: .word 0x2F
    z: .word 0x1A

; Calculate -(x + y - 2 * z + 1)
.text
    0x40000 LW X8, 0(X28)
    0x40004 LW X9, 4(X28)
    0x40008 ADD X8, X8, X9
    0x4000C LW X10, 8(X28)
    0x40010 ADD X10, X10, X10
    0x40014 SUB X8, X8, X10
    0x40018 ADDI X8, X8, 1
    0x4001C SUB X8, X0, X8
