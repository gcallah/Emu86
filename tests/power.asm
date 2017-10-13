      mov eax, 2
      mov ecx, 2
      mov ebx, 16
loop: call power
      cmp ebx, 1 
      je done
      jmp loop 

power: imul eax, ecx
      dec ebx
      ret

done: int 33, 0
