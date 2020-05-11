; A simple function call
; Calls a function to do a simple calculation 
; Stores the argument in ebx (420)
; Stores the result in ecx (176400)
main:     movl $419, %eax
          inc %eax
          push %eax
          xor %eax, %eax
          call someFunc
          mov %eax, %ecx
          pop %ebx
          xor %eax, %eax
          int $32
someFunc: push %ebp
          movl %esp, %ebp
          movl %ebp, %ebx
          add $2, %ebx
          movl (%ebx), %ebx
          imul %ebx, %ebx
          movl %ebx, %eax
          pop %ebp
          ret