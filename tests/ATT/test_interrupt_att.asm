         mov $0, %eax
         int $22
         mov %eax, (0)
         mov $1, %ebx

loop:    mov %eax, %edx
         mov $0, %eax
         int $22
         mov %eax, (%ebx)
         cmp %eax, (0)
         je done
         inc %ebx
         jmp loop
done: mov $1, %ecx
