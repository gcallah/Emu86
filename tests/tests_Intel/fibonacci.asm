; A program that calculates the 7th Fibonacci Number
; Uses the silly recursive algorithm
; Stores the argument in ebx (0x7)
; Stores the result in ecx (0xD)
main:      mov eax, 0x7
           push eax
           xor eax, eax
           call fib
           pop ebx
           mov ecx, eax
           xor eax, eax
           int 0x20
fib:       push ebp
           mov ebp, esp
           mov ebx, [ebp + 2]
           mov ecx, 0x1
           cmp ebx, ecx
           je basecase1
           xor ecx, ecx
           cmp ebx, ecx
           jle basecase0
           dec ebx
           push ebx
           call fib
           pop ebx
           dec ebx
           push eax
           push ebx
           call fib
           pop ebx
           pop ecx
           add eax, ecx
           pop ebp
           ret
basecase1: mov eax, 0x1
           pop ebp
           ret
basecase0: mov eax, 0x0
           pop ebp
           ret