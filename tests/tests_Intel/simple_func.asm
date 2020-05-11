; A simple function call
; Calls a function to do a simple calculation
; Stores the argument in ebx (0x29A)
; Stores the result in ecx (0x6C4A4)
main:     mov eax, 0x299
          inc eax
          push eax
          xor eax, eax
          call someFunc
          pop ebx
          mov ecx, eax
          xor eax, eax
          int 0x20
someFunc: push ebp
          mov ebp, esp
          mov ebx, [ebp + 2]
          imul ebx, ebx
          mov eax, ebx
          pop ebp
          ret