; Storing and fetching data
    400000 ADDI R7, R0, 8
    400004 SW R7, 0(R28)
    400008 ADDI R7, R7, 8
    40000C SW R7, 4(R28)
    400010 ADDI R7, R7, 10
    400014 SW R7, 8(R28)

    400018 LW R8, 0(R28)
    40001C LW R9, 4(R28)
    400020 LW R10, 8(R28)