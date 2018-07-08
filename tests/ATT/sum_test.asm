; Declare number and sum.
.data
    number: .short -105
    sum: .short ?

; Store first number to EAX
; Add 158 to value in EAX
; Store total to sum
.text
    mov (number), %eax		
    add $158, %eax	
    mov %eax, (sum)