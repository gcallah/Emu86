; Declare a Celsius temperature

.data
    cTemp: .word 23
    fTemp: .word 0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    LW R8, cTemp(R28)
    ADDI R9, R0, 9
    MULT R8, R9
    MFLO R8
    ADDI R8, R8, 2
    ADDI R9, R0, 5
    DIV R8, R9
    MFLO R8
    ADDI R8, R8, 20
    SW R8, fTemp(R28)