; Declare an array and declare size of the array
.data
    nbrArray: .word 25, 47, -15, -50, 32, 10, 10, 10, 10, 10
    nbrElts: .word 10

; Calculate the average of the array:
.text
    add $s0, $s0, $zero
    add $s1, $s1, $zero
    lw $t0, nbrElts
forCount1: beq $s1, $t0, 4
body: add $s0, $s0, $s1
      addi $s1, $s1, 1
      j forCount1
endCount: div $s0, $t0
mflo $s2
mfhi $s3
