         mov eax, 0
         mov ebx, 16

; compare eax and ebx and loop until eax greater than ebx
loop: cmp eax, ebx
         jg done
         inc eax
         jmp loop

; when done, store ebx in ecx
done: mov ecx, ebx
         mov edx, 27
         and edx, 23
