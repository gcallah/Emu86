; Declare a Celsius temperature floating points
.data
    a: .float 5.1
    b: .float 3.78
    c: .float 4.6
    d: .float 1.0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    0x40000 LWC F8, 0(F28)
    0x40004 LWC F10, 4(f28)
    0x40008 ADD.S F8, F8, F10
    0x4000C SUB.S F8, F8, F10
    0x40010 LWC F12, 8(F28)
    0x40014 MULT.S F8, F8, F12
    0x40018 DIV.S F8, F8, F12
    0x4001C SWC F8, 0xC(F28)