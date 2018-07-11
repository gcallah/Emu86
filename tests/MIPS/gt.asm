         add $s0, $s0, $zero
         addi $s1, $s1, 16

; compare S0 and S1 and loop until eax greater than ebx
loop: sub $s2, $s0, $s1
      slt $s3, $zero, $s2
      addi $s4, $zero, 1
      beq $s3, $s4, 2
      addi $s0, $s0, 1
      j loop

; when done, store ebx in ecx
done: add $s5, $s1, $zero
      addi $s6, $zero, 27
      andi $s6, $s6, 23



