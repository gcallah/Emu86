; First comes the data section, where we declare some names.
.data
    x: .word 0x8
    y: .word 0x10
    z: .word 0x20

; Next is the .text section, where we use them:
.text
    0x400000 LW R8, 0(R28)
    0x400004 LW R9, 4(R28)
    0x400008 LW R10, 8(R28)