; In edx, we put the number to raise to the power we put in ebx.
      mov edx, 2
      mov ebx, 16
      call power
      mov eax, 0
      int 32

power: mov ecx, edx
loop: imul edx, ecx
      dec ebx
      cmp ebx, 1
      jne loop
      ret
