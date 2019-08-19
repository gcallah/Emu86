; Declare addends
.data
    numOne REAL4 16.6
    numTwo REAL4 128.4

; Store addends in ST0 and ST1
; Add and store result in ST0
.text
    FLD [numOne]
    FLD [numTwo]
    FADD ST0, ST1
