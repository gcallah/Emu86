; Declare a number
.data
    number: .short 100

; Calculate square root of the number
.text
    mov (number), %eax
    push %ebx
    push %ecx
    mov 0, %ebx
WhileLE: mov %ebx, %ecx
         imul %ebx, %ecx
         cmp %eax, %ecx
         jnle EndWhileLE
         inc %ebx
         jmp WhileLE
EndWhileLE: dec %ebx
            mov %ebx, %eax
            pop %ecx
            pop %ebx