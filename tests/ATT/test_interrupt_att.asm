         mov 0, %eax
         int 22
         mov %eax, (0)
         mov 1, %ebx

loop:    mov %eax, %edx
         mov 0, %eax
         int 22
         mov %eax, (%ebx)
         cmp [0], %eax
         je done
         inc %ebx
         jmp loop
done: mov 1, %ecx
