; Declare a Celsius temperature floating points
.data
    cTemp: .double 10.0
    scale: .double 1.8
    offsetAdd: .double 32.0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    0x40000 LDC F8, 0(F28)
    0x40004 LDC F10, 4(F28)
    0x40008 MULT.D F8, F8, F10
    0x4000C LDC F12, 8(F28)
    0x40010 ADD.D F12, F8, F12