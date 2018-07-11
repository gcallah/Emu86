; Declare a Celsius temperature

.data
    cTemp: .word 35
    fTemp: .word 0

; Convert from Celsius to Fahrenheit
; Store result in fTemp
.text
    lw $t0, cTemp($gp)
    addi $s0, $zero, 9
    mult $t0, $s0
    mflo $t0
    addi $t0, $t0, 2
    addi $s0, $zero, 5
    div $t0, $s0
    mflo $t0
    addi $t0, $t0, 32
    sw $t0, fTemp($gp)