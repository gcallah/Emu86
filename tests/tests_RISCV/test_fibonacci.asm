; A program that calculates the 7th Fibonacci Number
; Uses the silly recursive algorithm
; Stores the result in X10 (0xD)
main:      0x00 addi X12, X0, 0x7
           0x04 jal X1, 0x3
           0x08 syscall
fib:       0x0C beq X12, X0, 0x13
           0x10 slti X6, X12, 0x2
           0x14 bne X6, X0, 0x13
           0x18 addi X12, X12, -1
           0x1C sw X12, -4(X2)
           0x20 sw X1, -8(X2)
           0x24 addi X2, X2, -8
           0x28 jal X1, 0x3
           0x2C lw X1, 0(X2)
           0x30 lw X12, 4(X2)
           0x34 addi X12, X12, -1
           0x38 sw X10, 0(X2)
           0x3C sw X1, -4(X2)
           0x40 addi X2, X2, -4
           0x44 jal X1, 0x3
           0x48 lw X1, 0(X2)
           0x4C lw X6, 4(X2)
           0x50 addi X2, X2, 0xC
           0x54 add X10, X10, X6
           0x58 jr X1
basecase0: 0x5C add X10, X0, X0
           0x60 jr X1
basecase1: 0x64 addi X10, X0, 1
           0x68 jr X1