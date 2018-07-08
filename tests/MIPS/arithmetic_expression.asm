; Declare x, y, and z variables 
.data
    x: .word 35
    y: .word 47
    z: .word 26

; Calculate -(x + y - 2 * z + 1)
.text
    lw $t0, x
    lw $t1, y
    lw $t2, 0($t0)
    lw $t3, 0($t1)
    add $t2, $t2, $t3
    lw $t1, z
    lw $t3, 0($t1)
    add $t3, $t3, $t3
    sub $t2, $t2, $t3
    addi $t2, $t2, 1
    sub $t2, $zero, $t2