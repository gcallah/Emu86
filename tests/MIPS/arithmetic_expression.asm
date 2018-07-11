; Declare x, y, and z variables 
.data
    x: .word 35
    y: .word 47
    z: .word 26

; Calculate -(x + y - 2 * z + 1)
.text
    lw $t0, x($gp)
    lw $t1, y($gp)
    add $t0, $t0, $t1
    lw $t1, z($gp)
    add $t1, $t1, $t1
    sub $t0, $t0, $t1
    addi $t0, $t0, 1
    sub $t0, $zero, $t0