; Declare an array and declare size of the array
.data
    nbrArray DW 25, 47, -15, -50, 32, 95 DUP (10)
    nbrElts DW 100

; Calculate the average of the array:
.text
    mov eax, 0
    mov ebx, 0
    mov edx, 0
    mov ecx, [nbrElts]
forCount1: cmp ebx, ecx
           je endCount
body: add eax, [ebx]
      inc ebx
      jmp forCount1
endCount: idiv ecx 


