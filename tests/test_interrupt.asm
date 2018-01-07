         int 22
         mov [0], eax
         mov ebx, 1
loop: int 22
         mov [ebx], eax
         cmp [0], eax
         je done
         inc ebx
         jmp loop
done: mov ecx, 1
