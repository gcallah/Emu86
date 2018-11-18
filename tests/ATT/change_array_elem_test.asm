; Declare an array and declare size of the array
; Declare the minimum of the array
.data
    nbrArray: .short 25, 47, 15, 50, 32, 95 DUP (10)
    nbrElts: .short 100
    nbrMin: .short 33

; Change any numbers less than min to min:
.text
    mov $0, %eax
    mov $0, %ebx
    mov $0, %edx
    mov (nbrElts), %ecx
forCount1: cmp %ecx, %ebx
           je endCount
body: cmp (nbrMin), (%ebx)
      jge endIfSmall
      mov (nbrMin), (%ebx)
endIfSmall: add (%ebx), %eax
            inc %ebx
            jmp forCount1
endCount: mov %eax, %edx
