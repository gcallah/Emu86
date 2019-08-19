; Declare length and width
.data
    long REAL4 16.6
    wide REAL4 128.4

; Calculate area of rectangle
.text
    FLD [long]
    FLD [wide]
    FMUL ST0, ST1
