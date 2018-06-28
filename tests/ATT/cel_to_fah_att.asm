; Declare a Celsius temperature
; Uninitialized fTemp 
.data
    cTemp: .short 35
    fTemp: .short ?

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    mov (cTemp), %eax
    imul $9, %eax
    add $2, %eax
    mov $5, %ebx
    idiv %ebx 
    add $32, %eax
    mov %eax, (fTemp)