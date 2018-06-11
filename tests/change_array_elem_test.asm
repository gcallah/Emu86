; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray DW 25, 47, 15, 50, 32, 95 DUP (10)
    nbrElts DW 100
    nbrMin DW 33

; Change any numbers less than min to min:
.text
    mov eax, 0
    mov ebx, 0
    mov edx, 0
    mov ecx, nbrElts
forCount1: cmp ebx, ecx
           je endCount
body: cmp nbrArray[ebx], nbrMin
      jge endIfSmall
      mov nbrArray[ebx], nbrMin
endIfSmall: add eax, nbrArray[ebx]
            inc ebx
            jmp forCount1
endCount: mov edx, eax


