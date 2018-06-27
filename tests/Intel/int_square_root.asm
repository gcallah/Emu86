; Declare a number
.data
    number DW 100

; Calculate square root of the number
.text
    mov eax, [number]
    push ebx
    push ecx
    mov ebx, 0
WhileLE: mov ecx, ebx
         imul ecx, ebx
         cmp ecx, eax
         jnle EndWhileLE
         inc ebx
         jmp WhileLE
EndWhileLE: dec ebx
            mov eax, ebx
            pop ecx
            pop ebx