; Declare a Celsius temperature
; Uninitialized fTemp 
.data
    cTemp DW 35
    fTemp DW ?

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    mov eax, cTemp
    imul eax, 9
    add eax, 2
    mov ebx, 5
    idiv ebx 
    add eax, 32
    mov fTemp, eax