         mov 0, %eax
         mov 16, %ebx

; compare eax and ebx and loop until eax greater than ebx
loop: cmp %eax, %ebx
         jg done
         inc %eax
         jmp loop

; when done, store ebx in ecx
done: mov %ebx, %ecx
         mov 27, %edx
         and 23, %edx
