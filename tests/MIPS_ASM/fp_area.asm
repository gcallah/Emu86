; Declare length and width
.data
	long: .float 12.2
	wide: .float 12.5

; Calc area of rect
.text
	0x40000 LWC F8, 0(F28)
    0x40004 LWC F10, 4(F28)
    0x40008 MULT.S F12, F8, F10