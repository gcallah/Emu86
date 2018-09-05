; Declare a Celsius temperature

.data
    cTemp: .word 0x23
    fTemp: .word 0x0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    0x40000 LW R8, 0(R28)
    0x40004 ADDI R9, R0, 9
    0x40008 MULT R8, R9
    0x4000C MFLO R8
    0x40010 ADDI R8, R8, 2
    0x40014 ADDI R9, R0, 5
    0x40018 DIV R8, R9
    0x4001C MFLO R8
    0x40020 ADDI R8, R8, 0x20
    0x40024 SW R8, 4(R28)