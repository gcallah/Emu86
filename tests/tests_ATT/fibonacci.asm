; A program that calculates the 7th Fibonacci Number
; Uses the silly recursive algorithm
; Stores the argument in ebx (0x7)
; Stores the result in ecx (0xD)
main:      movb $0x7, %eax
           push %eax
           xor %eax, %eax
           call fib
           pop %ebx
           mov %eax, %ecx
           xor %eax, %eax
           int $0x20
fib:       push %ebp
           movl %esp, %ebp
           movl %ebp, %ebx
           add $0x2, %ebx
           movl (%ebx), %ebx
           movb $0x1, %ecx
           cmp %ecx, %ebx
           je basecase1
           xor %ecx, %ecx
           cmp %ecx, %ebx
           jle basecase0
           dec %ebx
           push %ebx
           call fib
           pop %ebx
           dec %ebx
           push %eax
           push %ebx
           call fib
           pop %ebx
           pop %ecx
           add %ecx, %eax
           pop %ebp
           ret
basecase1: movb $0x1, %eax
           pop %ebp
           ret
basecase0: movb $0x0, %eax
           pop %ebp
           ret