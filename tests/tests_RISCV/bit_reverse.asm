; reverses the order of bits
; in a word

; Declare a string
.data
    string: .word 0xABCD

.text
    0x400000 LW X5, 0(X0)
    0x400004 ADD X11, X0, X0

loop: 0x400008 SLLI X11, X11, 1
      0x40000C ANDI X13, X10, 1
      0x400010 OR X11, X13, X11
      0x400014 SRLI X10, X10, 1
      0x400018 ADDI X5, X5, -1
      0x40001C BNE X5, X0, -6
