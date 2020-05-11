; A program that calculates the 7th Fibonacci Number
; Uses the silly recursive algorithm
; Stores the argument in ebx (7)
; Stores the result in ecx (13)
main:      movb $7, %eax
           push %eax
           xor %eax, %eax
           call fib
           pop %ebx
           mov %eax, %ecx
           xor %eax, %eax
           int $32
fib:       push %ebp
           movl %esp, %ebp
           movl %ebp, %ebx
           add $2, %ebx
           movl (%ebx), %ebx
           movb $1, %ecx
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
basecase1: movb $1, %eax
           pop %ebp
           ret
basecase0: movb $0, %eax
           pop %ebp
           ret