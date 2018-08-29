; Declare arrays x, y, z
; y is an array of size 13, holding element 50
; z is an array of the ASCII values of 'hello', ends in 0 
.data
    x: .word 3, 8, 5, 2
    y: .word 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32
    z: .word 'hello', 0

; Store array values
.text
    400000 LW R8, 0(R28) 
    400004 LW R9, 20(R28)
    400008 LW R10, 50(R28)
    40000C LW R11, 8(R28)