; Declare a Celsius temperature

.data
    cTemp: .word 23
    fTemp: .word 0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    40000 LW R8, cTemp(R28)
    40004 ADDI R9, R0, 9
    40008 MULT R8, R9
    4000C MFLO R8
    40010 ADDI R8, R8, 2
    40014 ADDI R9, R0, 5
    40018 DIV R8, R9
    4001C MFLO R8
    40020 ADDI R8, R8, 20
    40024 SW R8, fTemp(R28)