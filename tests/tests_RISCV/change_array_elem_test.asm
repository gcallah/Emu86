; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray: .word 0x19, 0x2F, 0xF, 0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA
    nbrElts: .word 0xA
    nbrMin: .word 0x21

; Change any numbers less than min to min:
.text
    0x40000 ADD X8, X0, X0
    0x40004 ADD X9, X0, X0
    0x40008 ADD X10, X0, X0
    0x4000C ADD X11, X0, X0
    0x40010 LW X16, 0x2C(X28)
    0x40014 LW X17, 0x28(X28)

FORCOUNT: 0x40018 BEQ X10, X17, 9

BODY: 0x4001C LW X12, 0(X9)
      0x40020 SLT X13, X16, X12
      0x40024 BNE X13, X0, 1
      0x40028 SW X16, 0(X9)

ENDIFSMALL: 0x4002C LW X11, 0(X9)
            0x40030 ADD X8, X8, X11
            0x40034 ADDI X9, X9, 4
            0x40038 ADDI X10, X10, 1
            0x4003C JR 0x10006

ENDCOUNT: 0x40040 ADD X13, X0, X8
