; Declare length and width
.data
    long: .word 23
    wide: .word 1B

; Calculate area of rectangle
.text
    LW R8, long(R28)
    LW R9, wide(R28)
    MULT R8, R9
    MFLO R10