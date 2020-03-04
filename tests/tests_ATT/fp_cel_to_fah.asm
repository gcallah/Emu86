; Declare a Celsius temperature
; Uninitialized fTemp 
.data
    cTemp .FLOAT 35.4
    fTemp .FLOAT 0.0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    fld (cTemp)
    fmul $9
    fdiv $5 
    fadd $32
    fst (fTemp)