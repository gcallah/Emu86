; Declare an array and declare size of the array
.data
    nbrArray: .short 25, 47, -15, -50, 32, 95 DUP (10)
    nbrElts: .short 100

; Calculate the average of the array:
.text
    mov 0, %eax
    mov 0, %ebx
    mov 0, %edx
    mov (nbrElts), %ecx
forCount1: cmp %ebx, %ecx
           je endCount
body: add (%ebx), %eax
      inc %ebx
      jmp forCount1
endCount: idiv %ecx 


