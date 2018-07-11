; Declare length and width
.data
    long: .word 35
    wide: .word 27

; Calculate area of rectangle
.text
    lw $t0, long($gp)
    lw $t1, wide($gp)
    mult $t0, $t1
    mflo $t2