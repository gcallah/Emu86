      mov eax, 16
      mov ebx, 0

; compare eax and ebx and loop until equal
loop: cmp eax, ebx
      jz done
      inc ebx
      dec edx
      jnz loop

done: mov ecx, ebx  ; when done, store ebx in ecx
