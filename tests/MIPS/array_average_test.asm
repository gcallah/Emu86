; Declare an array and declare size of the array
.data
    nbrArray: .word 25, 47, -15, -50, 32, 10, 10, 10, 10, 10
    nbrElts: .word 10

; Calculate the average of the array:
.text
    add $s0, $s0, $zero
    add $s1, $s1, $zero
    lw $t0, nbrElts($gp)
    add $s2, $gp, nbrArray 
forCount1: beq $s1, $t0, 5
body: lw $s4, ($s2)
      add $s0, $s0, $s4
      addi $s1, $s1, 1
      addi $s2, $s2, 1
      j forCount1
endCount: div $s0, $t0
mflo $s3
mfhi $s4
