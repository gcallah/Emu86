; Declare number and sum.
.data
    number: .word -105
    sum: .word 0

; Store first number to EAX
; Add 158 to value in EAX
; Store total to sum
.text
    lw $s0, number($gp)		
    addi $s0, $s0, 158	
    sw $s0, sum($gp)