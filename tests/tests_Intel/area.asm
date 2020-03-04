; Declare length and width
.data
    long DW 35
    wide DW 27

; Calculate area of rectangle
.text
    mov eax, [long]
    imul eax, [wide]
