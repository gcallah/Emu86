; A simple function call
; Calls a function to do a simple calculation
; Stores the argument in R4 (29A)
; Stores the result in R2 (6C4A4)
0x00 addi R4, R0, 0x299
0x04 addi R4, R4, 0x1
0x08 jal 0x4
0x0C syscall
0x10 mult R4, R4
0x14 mflo R2
0x18 jr R31