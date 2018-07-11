; Declare a number
.data
    number: .word 759

; Calculating log (base 2) of a number
.text
    add $s0, $s0, $zero
    addi $s1, $s1, 1
    lw $s2, number($gp)

whileLE: sub $s3, $s1, $s2
         slt $s4, $zero, $s3  
         bne $s4, $zero, 3
body: add $s1, $s1, $s1
      addi $s0, $s0, 1
      j whileLE

endWhileLE: addi $s0, $s0, -1