; Declare an array and declare size of the array
.data
    nbrArray: .word 0x19, 0x2F, -0xF, -0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA
    nbrElts: .word 0xA

; Calculate the average of the array:
.text
    0x40000 ADD X8, X0, X0
    0x40004 ADD X9, X0, X0
    0x40008 LW X16, 28(X28)
    0x4000C ADD X10, X0, X0
BODY: 0x40010 LW X11, 0(X10)
      0x40014 ADD X8, X8, X11
      0x40018 ADDI X9, X9, 1
      0x4001C ADDI X10, X10, 4
      0x40020 BNE X9, X16, -5
ENDCOUNT: 0x40024 DIV X17, X8, X16
