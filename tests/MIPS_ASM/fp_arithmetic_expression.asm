; Declare x, y, and z variables 
.data
    x: .double 15.5
    y: .double 10.813
    z: .double 27.25

; Calculate -(x + y - 2 * z)
.text
    0x40000 LDC F8, 0(R28)
    0x40004 LDC F10, 4(R28)
    0x40008 ADD.D F8, F8, F10
    0x4000C LDC F12, 8(R28)
    0x40010 ADD.D F12, F12, F12
    0x40014 SUB.D F8, F8, F12
    0x40018 SUB.D F8, F0, F8