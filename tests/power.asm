      mov edx, 2
      mov ebx, 16
      call power
      int 33

power: mov ecx, edx
loop: imul edx, ecx
      dec ebx
      cmp ebx, 1
      jne loop
      ret
