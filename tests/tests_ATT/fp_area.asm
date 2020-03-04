; Declare length and width
.data
    long .float 16.6
    wide .float 128.4

; Calculate area of rectangle
.text
    FLD (long)
    FLD (wide)
    FMUL %ST1, %ST0
