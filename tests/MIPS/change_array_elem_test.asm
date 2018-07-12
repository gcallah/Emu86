; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray: .word 25, 47, 15, 50, 32, 10, 10, 10, 10, 10
    nbrElts: .word 10
    nbrMin: .word 33

; Change any numbers less than min to min:
.text
    add $s0, $zero, $zero
    add $s1, $zero, $zero
    addi $s2, $zero, nbrArray
    lw $t0, nbrMin($gp)
    lw $t1, nbrElts($gp)
forCount1: beq $s1, $t1, 8
body: lw $s3, ($s1)
      slt $s4, $t0, $s3
      bne $s4, $zero, 1
      sw $t0, ($s1)
endIfSmall: lw $s3, ($s1)
            add $s0, $s0, $s3
            addi $s1, $s1, 1
            j forCount1
endCount: add $s5, $zero, $s0