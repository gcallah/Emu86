; Declare length and width
.data
    long: .word 0x23
    wide: .word 0x1B

; Calculate area of rectangle
.text
    0x40000 LW R8, 0(R28)
    0x40004 LW R9, 4(R28)
    0x40008 MULT R8, R9
    0x4000C MFLO R10