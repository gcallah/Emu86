; First comes the data section, where we declare some names.
.data
    x: .word 8
    y: .word 10
    z: .word 20

; Next is the .text section, where we use them:
.text
    400000 LW R8, x(R28)
    400004 LW R9, y(R28)
    400008 LW R10, z(R28)