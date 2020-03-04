; Declare length and width
.data
    long: .short 35
    wide: .short 27

; Calculate area of rectangle
.text
    mov (long), %eax
    imul (wide), %eax