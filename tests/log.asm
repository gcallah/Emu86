; Declare a number
.data
    number DW 759

; Calculating log (base 2) of a number
.text
    mov ecx, 0
    mov eax, 1

; Loop until EAX is greater than number
whileLE: cmp eax, number
         jnle endWhileLE
body: add eax, eax
      inc ecx
      jmp whileLE

endWhileLE:	dec ecx 