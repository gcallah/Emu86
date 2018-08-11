; Declare length and width
.data
    long: .word 23
    wide: .word 1B

; Calculate area of rectangle
.text
    40000 LW R8, 0(R28)
    40004 LW R9, 4(R28)
    40008 MULT R8, R9
    4000C MFLO R10