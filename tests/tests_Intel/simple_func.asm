; A simple function call
; Calls a function to do a simple calculation
; Stores the argument in ebx (420)
; Stores the result in ecx (176400)
main:     mov eax, 419
          inc eax
          push eax
          xor eax, eax
          call someFunc
          pop ebx
          mov ecx, eax
          xor eax, eax
          int 32
someFunc: push ebp
          mov ebp, esp
          mov ebx, [ebp + 2]
          imul ebx, ebx
          mov eax, ebx
          pop ebp
          ret