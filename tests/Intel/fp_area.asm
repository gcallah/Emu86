; Declare length and width
.data
    long DW 0x40600000
    wide DW 0x1B

; Calculate area of rectangle
.text
    FLD F7, [long]
    FMUL F6, [wide]
