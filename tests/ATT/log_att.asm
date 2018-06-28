; Declare a number
.data
    number: .short 759

; Calculating log (base 2) of a number
.text
    mov $0, %ecx
    mov $1, %eax
whileLE: cmp (number), %eax
         jnle endWhileLE
body: add %eax, %eax
      inc %ecx
      jmp whileLE

endWhileLE: dec %ecx 