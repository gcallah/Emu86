; Declare a Celsius temperature

.data
    cTemp: .word 0x23
    fTemp: .word 0x0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    0x40000 LW X8, 0(X28)
    0x40004 ADDI X9, X0, 9
    0x40008 MUL X8, X8, X9
    0x4000C ADDI X8, X8, 2
    0x40010 ADDI X9, X0, 5
    0x40014 DIV X8, X8, X9
    0x40018 ADDI X8, X8, 0x20
    0x4001C SW X8, 4(X28)