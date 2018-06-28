; In edx, we put the number to raise to the power we put in ebx.
      mov 2, %edx
      mov 16, %ebx
      call power
      mov 0, %eax
      int 32

power: mov %edx, %ecx
loop: imul %ecx, %edx
      dec %ebx
      cmp %ebx, 1
      jne loop
      ret
