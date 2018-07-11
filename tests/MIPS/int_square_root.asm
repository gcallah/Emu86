; Declare a number
.data
    number: .word 100

; Calculate square root of the number
.text
    lw $s0, number($gp)

WhileLE: add $s2, $zero, $s1
         mult $s2, $s1
         mflo $s2
         sub $s3, $s2, $s0
         slt $s4, $zero, $s3
         bne $s4, $zero, 2
         addi $s1, $s1, 1
         j WhileLE
EndWhileLE: subi $s1, $s1, 1
            add $s0, $zero, $s1
            