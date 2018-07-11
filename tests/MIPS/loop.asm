; Compare S0 and S1 and loop until equal
; When done, store S1 to S3
    addi $s0, $s0, 16
    add $s1, $s1, $zero
    addi $s1, $s1, 1
    addi $s2, $s2, -1
    bne $s0, $s1, -3
    add $s3, $s3, $s1