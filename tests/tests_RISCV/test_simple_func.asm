; A simple function call
; Calls a function to do a simple calculation
; Stores the argument in X12 (29A)
; Stores the result in X10 (6C4A4)
main:     0x00 addi X12, R0, 0x299
          0x04 addi X12, X12, 0x1
          0x08 jal 0x4
          0x0C syscall
someFunc: 0x10 mult X10, X12, X12
          0x18 jr R31