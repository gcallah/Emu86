; A simple function call
; Calls a function to do a simple calculation 
; Stores the argument in ebx (0x29A)
; Stores the result in ecx (0x6C4A4)
main:     movl $0x299, %eax
          inc %eax
          push %eax
          xor %eax, %eax
          call someFunc
          mov %eax, %ecx
          pop %ebx
          xor %eax, %eax
          int $0x20
someFunc: push %ebp
          movl %esp, %ebp
          movl %ebp, %ebx
          add $0x2, %ebx
          movl (%ebx), %ebx
          imul %ebx, %ebx
          movl %ebx, %eax
          pop %ebp
          ret