main:      0x00 addi R4, R0, 0x7
           0x04 jal 0x3
           0x08 syscall
fib:       0x0C beq R4, R0, 0x13
           0x10 slti R8, R4, 0x2
           0x14 bne R8, R0, 0x13
           0x18 addi R4, R4, -1
           0x1C sw R4, -4(R29)
           0x20 sw R31, -8(R29)
           0x24 addi R29, R29, -8
           0x28 jal 0x3
           0x2C lw R31, 0(R29)
           0x30 lw R4, 4(R29)
           0x34 addi R4, R4, -1
           0x38 sw R2, 0(R29)
           0x3C sw R31, -4(R29)
           0x40 addi R29, R29, -4
           0x44 jal 0x3
           0x48 lw R31, 0(R29)
           0x4C lw R8, 4(R29)
           0x50 addi R29, R29, 0xC
           0x54 add R2, R2, R8
           0x58 jr R31
basecase0: 0x5C add R2, R0, R0
           0x60 jr R31
basecase1: 0x64 addi R2, R0, 1
           0x68 jr R31