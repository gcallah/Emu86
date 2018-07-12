    add $s0, $zero, $zero
    j label1
    subi $s0, $s0, 1
label1: addi $s0, $s0, 1

    add $s1, $zero, $zero
    beq $s1, $zero, 1
    subi $s0, $s0, 1
label2: addi $s0, $s0, 1

    addi $s1, $zero, 1
    beq $s1, $zero, 1
    subi $s0, $s0, 1
label3: addi $s0, $s0, 1

    addi $s1, $zero, 1
    bne $s1, $zero, 1
    subi $s0, $s0, 1
label4: addi $s0, $s0, 1

