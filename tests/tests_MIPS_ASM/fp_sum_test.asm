; Declare x, y, and sum.
.data
    x: .double 56789.1234
    y: .double 12345.6789
    sum: .double 0

; Store first number to F8
; Store second number to F10
; Add numbers together
; Store total to sum
.text
    0x40000 LDC F8, 0(F28)
    0x40004 LDC F10, 4(F28)		
    0x40008 ADD.D F12, F8, F10
    0x4000C SDC F12, 8(F28)