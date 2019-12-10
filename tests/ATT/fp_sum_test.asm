; Declare addends
.data
    numOne .float 16.6
    numTwo .float 128.4

; Store addends in ST0 and ST1
; Add and store result in ST0
.text
    FLD (numOne)
    FLD (numTwo)
    FADD %ST1, %ST0
