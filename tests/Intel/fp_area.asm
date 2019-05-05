; Declare length and width
.data
    long DW 0x40600000
    wide DW 0x1B

; Calculate area of rectangle
.text
    mov F7, [long]
    imul F6, [wide]
