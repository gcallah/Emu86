         mov eax, 0
         mov ebx, 16

; compare eax and ebx and loop until eax > ebx
loop: cmp eax, ebx
         jg done
         inc eax
         jmp loop

done: mov ecx, ebx  ; when done, store ebx in ecx

         mov edx, 27
         and edx, 23