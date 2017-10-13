      mov eax, 2
      mov ebx, 16
      call power
      int 33, 0

power: mov ecx, eax
loop: imul eax, ecx
      dec ebx
      cmp ebx, 1
      jne loop
      ret
