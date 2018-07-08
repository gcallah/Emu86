      mov $16, %eax
      mov $0, %ebx

; Compare eax and ebx and loop until equal
loop: cmp %eax, %ebx
      jz done
      inc %ebx
      dec %edx
      jnz loop

done: mov %ebx, %ecx  ; when done, store ebx in ecx
