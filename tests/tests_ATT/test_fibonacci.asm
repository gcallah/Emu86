main: movb $0x10, %eax
push %eax
xor %eax, %eax
call fib
pop %ebx
mov %eax, %ecx
xor %eax, %eax
int $0x20
fib: push %ebp
movl %esp, %ebp
movl %ebp, %ecx
add $0x2, %ecx
movl (%ecx), %ebx
movl %ebx, %edx
movb $0x1, %ecx
sub %ecx, %edx
jz basecase
xor %ecx, %ecx
movl %ebx, %edx
sub %ecx, %edx
jz basecase
dec %ebx
push %ebx
call fib
pop %ebx
add %ebx, %eax
pop %ebp
ret
basecase: movb $0x1, %eax
pop %ebp
ret