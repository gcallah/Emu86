; Declare length and width
.data
    long: .word 0x23
    wide: .word 0x1B

; Calculate area of rectangle
.text
    0x40000 LW X8, 0(X28)
    0x40004 LW X9, 4(X28)
    0x40008 MUL X10, X8, X9
