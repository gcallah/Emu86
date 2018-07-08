; Declare length and width
.data
    long: .word 35
    wide: .word 27

; Calculate area of rectangle
.text
    lw $t0, long
    lw $t1, wide
    lw $t2, 0($t0)
    lw $t3, 0($t1)
    mult $t3, $t2
    mflo $t4