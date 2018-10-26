; First comes the data section, where we declare some names.
.data
    x: .float 8.0
    y: .float 10.5
    z: .float 20.555
    a: .double 60.222

; Next is the .text section, where we use them:
.text
    0x400000 LWC F8, 0(F28)
    0x400004 LWC F10, 4(F28)
    0x400008 LWC F12, 8(F28)
    0x40000C LDC F14, C(F28)
