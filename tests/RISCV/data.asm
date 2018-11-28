; First comes the data section, where we declare some names.
.data
    x: .word 0x8
    y: .word 0x10
    z: .word 0x20

; Next is the .text section, where we use them:
.text
    0x400000 LW X8, 0(X28)
    0x400004 LW X9, 4(X28)
    0x400008 LW X10, 8(X28)