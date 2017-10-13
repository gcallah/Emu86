      mov eax, 2
      mov ebx, 16
      call power
      jmp done 

power: mov ecx, eax
loop: imul eax, ecx
      dec ebx
      cmp ebx, 1
      jne loop
      ret

done: int 33, 0
