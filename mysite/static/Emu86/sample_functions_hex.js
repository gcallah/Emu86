function addTwo_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare number and sum.\n.data\n    number DW -0x69\n    sum DW ?\n\n; Store first number to EAX\n; Add 158 to value in EAX\n; Store total to sum\n.text\n    mov eax, [number]\n    add eax, 0x9E\n    mov [sum], eax\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare number and sum.\n.data\n    number: .short -0x69\n    sum: .short ?\n\n; Store first number to EAX\n; Add 158 to value in EAX\n; Store total to sum\n.text\n    mov (number), %eax\t\t\n    add $0x9E, %eax\t\n    mov %eax, (sum)';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare number and sum.\n.data\n    number: .word -0x69\n    sum: .word 0\n\n; Store first number to R8\n; Add 158 to value in R8\n; Store total to sum\n.text\n    0x40000 LW R8, 0(R28)\t\t\n    0x40004 ADDI R8, R8, 0x9E\t\n    0x40008 SW R8, 4(R28)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Store first addend\n    40000 ADDI R7, R0, 69\n    40004 SW R7, 20(R28)\n\n; Load first number to R8\n; Add 158 to value in R8\n; Store sum to next location\n    40008 LW R8, 20(R28)\t\t\n    4000C ADDI R8, R8, 9E\t\n    40010 SW R8, 24(R28)';
	}
	else{
		codeString += '; Declare number and sum.\n.data\n    number: .word -0x69\n    sum: .word 0\n\n; Store first number to X8\n; Add 158 to value in X8\n; Store total to sum\n.text\n    0x40000 LW X8, 0(X28)\t\t\n    0x40004 ADDI X8, X8, 0x9E\t\n    0x40008 SW X8, 4(X28)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function arithExpr_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare x, y, and z variables \n.data\n    x DW 0x23\n    y DW 0x2F\n    z DW 0x1A\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    mov eax, [x]\t\t\n    add eax, [y]\t\n    mov ebx, [z]\n    add ebx, ebx\n    sub eax, ebx\n    inc eax \n    neg eax';
	}
	else if (flavor === 'att'){
		codeString += '; Declare x, y, and z variables \n.data\n    x: .short 0x23\n    y: .short 0x2F\n    z: .short 0x1A\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    mov (x), %eax\t\t\n    add (y), %eax\t\n    mov (z), %ebx\n    add %ebx, %ebx\n    sub %ebx, %eax\n    inc %eax \n    neg %eax';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare x, y, and z variables \n.data\n    x: .word 0x23\n    y: .word 0x2F\n    z: .word 0x1A\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    0x40000 LW R8, 0(R28)\n    0x40004 LW R9, 4(R28)\n    0x40008 ADD R8, R8, R9\n    0x4000C LW R10, 8(R28)\n    0x40010 ADD R10, R10, R10\n    0x40014 SUB R8, R8, R10\n    0x40018 ADDI R8, R8, 1\n    0x4001C SUB R8, R0, R8';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Calculate -(x + y - 2 * z + 1)\n; x = 35, y = 47, z = 26\n\n    40000 ADDI R8, R0, 23\n    40004 ADDI R9, R9, 2F\n    40008 ADD R8, R8, R9\n    4000C ADDI R10, R0, 1A\n    40010 ADD R10, R10, R10\n    40014 SUB R8, R8, R10\n    40018 ADDI R8, R8, 1\n    4001C SUB R8, R0, R8';
	}
	else{
		codeString += '; Declare x, y, and z variables \n.data\n    x: .word 0x23\n    y: .word 0x2F\n    z: .word 0x1A\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    0x40000 LW X8, 0(X28)\n    0x40004 LW X9, 4(X28)\n    0x40008 ADD X8, X8, X9\n    0x4000C LW X10, 8(X28)\n    0x40010 ADD X10, X10, X10\n    0x40014 SUB X8, X8, X10\n    0x40018 ADDI X8, X8, 1\n    0x4001C SUB X8, X0, X8\n';
	}
	document.getElementById('id_code').value = codeString;
}
function area_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare length and width\n.data\n    long DW 0x23\n    wide DW 0x1B\n\n; Calculate area of rectangle\n.text\n    mov eax, [long]\n    imul eax, [wide]\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare length and width\n.data\n    long: .short 0x23\n    wide: .short 0x1B\n\n; Calculate area of rectangle\n.text\n    mov (long), %eax\n    imul (wide), %eax';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare length and width\n.data\n    long: .word 0x23\n    wide: .word 0x1B\n\n; Calculate area of rectangle\n.text\n    0x40000 LW R8, 0(R28)\n    0x40004 LW R9, 4(R28)\n    0x40008 MULT R8, R9\n    0x4000C MFLO R10';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Calculate area of rectangle\n    40000 ADDI R8, R0, 23\n    40004 ADDI R9, R0, 1B\n    40008 MULT R8, R9\n    4000C MFLO R10\n    40010 SW R10, 1000(R0)';
	}
	else{
		codeString += '; Declare length and width\n.data\n    long: .word 0x23\n    wide: .word 0x1B\n\n; Calculate area of rectangle\n.text\n    0x40000 LW X8, 0(X28)\n    0x40004 LW X9, 4(X28)\n    0x40008 MUL X10, X8, X9\n';
	}
	document.getElementById('id_code').value = codeString;
}
function power_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; In edx, we put the number to raise to the power we put in ebx.\n      mov edx, 0x2\n      mov ebx, 0x10\n      call power\n      mov eax, 0x0\n      int 0x20\n\npower: mov ecx, edx\nloop: imul edx, ecx\n      dec ebx\n      cmp ebx, 0x1\n      jne loop\n      ret\n';
	}
	else if (flavor === 'att'){
		codeString += '; In edx, we put the number to raise to the power we put in ebx.\n      mov $0x2, %edx\n      mov $0x10, %ebx\n      call power\n      mov $0x0, %eax\n      int $0x20\n\npower: mov %edx, %ecx\nloop: imul %ecx, %edx\n      dec %ebx\n      cmp %ebx, $0x1\n      jne loop\n      ret\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; In R8, we put the number to raise to the power we put in R9.\n      0x400000 ADDI R8, R0, 2\n      0x400004 ADDI R9, R9, 0x10\n      0x400008 JAL 0x1000040\n      0x40000C SYSCALL\n\npower: 0x400010 ADD R16, R0, R8\nloop: 0x400014 MULT R8, R16\n      0x400018 MFLO R8\n      0x40001C ADDI R9, R9, -1\n      0x400020 ADDI R10, R0, 1\n      0x400024 BNE R9, R10, -5\n      0x400028 JR R31';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; In R8, we put the number to raise to the power we put in R9.\n    400000 ADDI R8, R0, 2\n    400004 ADDI R9, R9, 10\n    400008 JAL 1000040\n    40000C SYSCALL\n\n    400010 ADD R16, R0, R8\n    400014 MULT R8, R16\n    400018 MFLO R8\n    40001C ADDI R9, R9, -1\n    400020 ADDI R10, R0, 1\n    400024 BNE R9, R10, -5\n    400028 JR R31';
	}
	else{
		codeString += '; In X8, we put the number to raise to the power we put in X9.\n     0x400000 ADDI X8, X0, 2\n     0x400004 ADDI X9, X9, 0x10\n      0x400008 ADD X16, X0, X8\nloop: 0x40000C MUL X8, X8, X16\n      0x400010 ADDI X9, X9, -1\n      0x400014 ADDI X10, X0, 1\n      0x400018 BNE X9, X10, -4\n      0x40001C SYSCALL\n\n';
	}
	document.getElementById('id_code').value = codeString;
}
function data_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x DB 0x8\n    y DW 0x10\n    z DD 0x20\n\n; Next is the .text section, where we use them:\n.text\n    mov eax, [x]\n    mov ebx, [y]\n    mov ecx, [z]\n';
	}
	else if (flavor === 'att'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .byte 0x8\n    y: .short 0x10\n    z: .long 0x20\n\n; Next is the .text section, where we use them:\n.text\n    mov (x), %eax\n    mov (y), %ebx\n    mov (z), %ecx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .word 0x8\n    y: .word 0x10\n    z: .word 0x20\n\n; Next is the .text section, where we use them:\n.text\n    0x400000 LW R8, 0(R28)\n    0x400004 LW R9, 4(R28)\n    0x400008 LW R10, 8(R28)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Storing and fetching data\n    400000 ADDI R7, R0, 8\n    400004 SW R7, 0(R28)\n    400008 ADDI R7, R7, 8\n    40000C SW R7, 4(R28)\n    400010 ADDI R7, R7, 10\n    400014 SW R7, 8(R28)\n\n    400018 LW R8, 0(R28)\n    40001C LW R9, 4(R28)\n    400020 LW R10, 8(R28)';
	}
	else{
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .word 0x8\n    y: .word 0x10\n    z: .word 0x20\n\n; Next is the .text section, where we use them:\n.text\n    0x400000 LW X8, 0(X28)\n    0x400004 LW X9, 4(X28)\n    0x400008 LW X10, 8(X28)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function loop_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '      mov eax, 0x10\n      mov ebx, 0x0\n\n; Compare eax and ebx and loop until equal\nloop: cmp eax, ebx\n      jz done\n      inc ebx\n      dec edx\n      jnz loop\n\ndone: mov ecx, ebx  ; when done, store ebx in ecx\n';
	}
	else if (flavor === 'att'){
		codeString += '      mov $0x10, %eax\n      mov $0x0, %ebx\n\n; Compare eax and ebx and loop until equal\nloop: cmp %eax, %ebx\n      jz done\n      inc %ebx\n      dec %edx\n      jnz loop\n\ndone: mov %ebx, %ecx  ; when done, store ebx in ecx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Compare R8 and R9 and loop until equal\n; When done, store R9 to R11\n    0x40000 ADDI R8, R0, 10\n    0x40004 ADD R9, R0, R0\n    0x40008 ADDI R9, R9, 1\n    0x4000C ADDI R10, R10, -1\n    0x40010 BNE R8, R9, -3\n    0x40014 ADD R11, R11, R9';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Compare R8 and R9 and loop until equal\n; When done, store R9 to R11\n    40000 ADDI R8, R0, 10\n    40004 ADD R9, R0, R0\n    40008 ADDI R9, R9, 1\n    4000C ADDI R10, R10, -1\n    40010 BNE R8, R9, -3\n    40014 ADD R11, R11, R9';
	}
	else{
		codeString += '; Compare X8 and X9 and loop until equal\n; When done, store X9 to X11\n    0x40000 ADDI X8, X0, 10\n    0x40004 ADD X9, X0, X0\n    0x40008 ADDI X9, X9, 1\n    0x4000C ADDI X10, X10, -1\n    0x40010 BNE X8, X9, -3\n    0x40014 ADD X11, X11, X9\n';
	}
	document.getElementById('id_code').value = codeString;
}
function log_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare a number\n.data\n    number DW 0x2F7\n\n; Calculating log (base 2) of a number\n.text\n    mov ecx, 0x0\n    mov eax, 0x1\nwhileLE: cmp eax, [number]\n         jnle endWhileLE\nbody: add eax, eax\n      inc ecx\n      jmp whileLE\n\nendWhileLE: dec ecx ';
	}
	else if (flavor === 'att'){
		codeString += '; Declare a number\n.data\n    number: .short 0x2F7\n\n; Calculating log (base 2) of a number\n.text\n    mov $0x0, %ecx\n    mov $0x1, %eax\nwhileLE: cmp (number), %eax\n         jnle endWhileLE\nbody: add %eax, %eax\n      inc %ecx\n      jmp whileLE\n\nendWhileLE: dec %ecx ';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare a number\n.data\n    number: .word 0x2F7\n\n; Calculating log (base 2) of a number\n.text\n    0x40000 ADD R8, R8, R0\n    0x40004 ADDI R9, R9, 1\n    0x40008 LW R10, 0(R28)\n\nWHILELE: 0x4000C SUB R11, R9, R10\n         0x40010 SLT R12, R0, R11\n         0x40014 BNE R12, R0, 3\nBODY: 0x40018 ADD R9, R9, R9\n      0x4001C ADDI R8, R8, 1\n      0x40020 J 0x100030\n\nENDWHILELE: 0x40024 ADDI R8, R8, -1';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Calculating log (base 2) of 759\n    40000 ADD R8, R8, R0\n    40004 ADDI R9, R9, 1\n    40008 ADDI R10, R0, 2F7\n\n    4000C SUB R11, R9, R10\n    40010 SLT R12, R0, R11\n    40014 BNE R12, R0, 3\n    40018 ADD R9, R9, R9\n    4001C ADDI R8, R8, 1\n    40020 J 100030\n\n    40024 ADDI R8, R8, -1';
	}
	else{
		codeString += '; Declare a number\n.data\n    number: .word 0x2F7\n\n; Calculating log (base 2) of a number\n.text\n    0x40000 ADD X8, X8, X0\n    0x40004 ADDI X9, X9, 1\n    0x40008 LW X10, 0(X28)\n\nWHILELE: 0x4000C SUB X11, X9, X10\n         0x40010 SLT X12, X0, X11\n         0x40014 BNE X12, X0, 3\nBODY: 0x40018 ADD X9, X9, X9\n      0x4001C ADDI X8, X8, 1\n      0x40020 BEQ X0, X0, -6\n\nENDWHILELE: 0x40024 ADDI X8, X8, -1\n';
	}
	document.getElementById('id_code').value = codeString;
}
function avg_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray DW 0x19, 0x2F, -0xF, -0x32, 0x20, 0x5F DUP (0xA)\n    nbrElts DW 0x64\n\n; Calculate the average of the array:\n.text\n    mov eax, 0x0\n    mov ebx, 0x0\n    mov edx, 0x0\n    mov ecx, [nbrElts]\nforCount0x1: cmp ebx, ecx\n           je endCount\nbody: add eax, [ebx]\n      inc ebx\n      jmp forCount0x1\nendCount: idiv ecx\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray: .short 0x19, 0x2F, -0xF, -0x32, 0x20, 0x5F DUP (0xA)\n    nbrElts: .short 0x64\n\n; Calculate the average of the array:\n.text\n    mov $0x0, %eax\n    mov $0x0, %ebx\n    mov $0x0, %edx\n    mov (nbrElts), %ecx\nforCount0x1: cmp %ebx, %ecx\n           je endCount\nbody: add (%ebx), %eax\n      inc %ebx\n      jmp forCount0x1\nendCount: idiv %ecx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray: .word 0x19, 0x2F, -0xF, -0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA\n    nbrElts: .word 0xA\n\n; Calculate the average of the array:\n.text\n    0x40000 ADD R8, R0, R0\n    0x40004 ADD R9, R0, R0\n    0x40008 LW R16, 28(R28)\n    0x4000C ADD R10, R0, R0\nFORCOUNT: 0x40010 BEQ R9, R16, 5\nBODY: 0x40014 LW R11, (R10)\n      0x40018 ADD R8, R8, R11\n      0x4001C ADDI R9, R9, 1\n      0x40020 ADDI R10, R10, 4\n      0x40024 J 0x100040\nENDCOUNT: 0x40028 DIV R8, R16\n0x4002C MFLO R12\n0x40030 MFHI R13\n';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Create an array\n    3FFF4 ADDI R7, R0, A\n    3FFF8 SW R7, 104(R0)\n    3FFFC ADDI R6, R0, 0\n    40000 ADDI R7, R0, 19\n    40004 SW R7, R6(R0)\n    40008 ADDI R6, R6, 4\n    4000C ADDI R7, R0, 2F\n    40010 SW R7, R6(R0)\n    40014 ADDI R6, R6, 4\n    40018 ADDI R7, R0, -F\n    4001C SW R7, R6(R0)\n    40020 ADDI R6, R6, 4\n    40024 ADDI R7, R0, -32\n    40028 SW R7, R6(R0)\n    4002C ADDI R6, R6, 4\n    40030 ADDI R7, R0, 20\n    40034 SW R7, R6(R0)\n    40038 ADDI R6, R6, 4\n    4003C ADDI R7, R0, A\n    40040 ADDI R14, R14, 5\n    40044 BEQ R14, R0, 4\n    40048 SW R7, R6(R0)\n    4004C ADDI R6, R6, 4\n    40050 ADDI R14, R14, -1\n    40054 J 100110\n\n; Calculate the average of the array:\n    40058 ADD R8, R0, R0\n    4005C ADD R9, R0, R0\n    40060 LW R16, 104(R28)\n    40064 ADD R10, R0, R0\n    40068 BEQ R9, R16, 5\n    4006C LW R11, (R10)\n    40070 ADD R8, R8, R11\n    40074 ADDI R9, R9, 1\n    40078 ADDI R10, R10, 4\n    4007C J 1001A0\n    40080 DIV R8, R16\n    40084 MFLO R12\n    40088 MFHI R13\n';
	}
	else{
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray: .word 0x19, 0x2F, -0xF, -0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA\n    nbrElts: .word 0xA\n\n; Calculate the average of the array:\n.text\n    0x40000 ADD X8, X0, X0\n    0x40004 ADD X9, X0, X0\n    0x40008 LW X16, 28(X28)\n    0x4000C ADD X10, X0, X0\nBODY: 0x40010 LW X11, 0(X10)\n      0x40014 ADD X8, X8, X11\n      0x40018 ADDI X9, X9, 1\n      0x4001C ADDI X10, X10, 4\n      0x40020 BNE X9, X16, -5\nENDCOUNT: 0x40024 DIV X17, X8, X16\n';
	}
	document.getElementById('id_code').value = codeString;
}
function celFah_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp DW 0x23\n    fTemp DW ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov eax, [cTemp]\n    imul eax, 0x9\n    add eax, 0x2\n    mov ebx, 0x5\n    idiv ebx \n    add eax, 0x20\n    mov [fTemp], eax';
	}
	else if (flavor === 'att'){
		codeString += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp: .short 0x23\n    fTemp: .short ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov (cTemp), %eax\n    imul $0x9, %eax\n    add $0x2, %eax\n    mov $0x5, %ebx\n    idiv %ebx \n    add $0x20, %eax\n    mov %eax, (fTemp)';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare a Celsius temperature\n\n.data\n    cTemp: .word 0x23\n    fTemp: .word 0x0\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    0x40000 LW R8, 0(R28)\n    0x40004 ADDI R9, R0, 9\n    0x40008 MULT R8, R9\n    0x4000C MFLO R8\n    0x40010 ADDI R8, R8, 2\n    0x40014 ADDI R9, R0, 5\n    0x40018 DIV R8, R9\n    0x4001C MFLO R8\n    0x40020 ADDI R8, R8, 0x20\n    0x40024 SW R8, 4(R28)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Convert from Celsius to Fahrenheit\n; Store result in memory location 100\n    40000 ADDI R8, R0, 23\n    40004 ADDI R9, R0, 9\n    40008 MULT R8, R9\n    4000C MFLO R8\n    40010 ADDI R8, R8, 2\n    40014 ADDI R9, R0, 5\n    40018 DIV R8, R9\n    4001C MFLO R8\n    40020 ADDI R8, R8, 20\n    40024 SW R8, 100(R28)';
	}
	else{
		codeString += '; Declare a Celsius temperature\n\n.data\n    cTemp: .word 0x23\n    fTemp: .word 0x0\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    0x40000 LW X8, 0(X28)\n    0x40004 ADDI X9, X0, 9\n    0x40008 MUL X8, X8, X9\n    0x4000C ADDI X8, X8, 2\n    0x40010 ADDI X9, X0, 5\n    0x40014 DIV X8, X8, X9\n    0x40018 ADDI X8, X8, 0x20\n    0x4001C SW X8, 4(X28)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function modify_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray DW 0x19, 0x2F, 0xF, 0x32, 0x20, 0x5F DUP (0xA)\n    nbrElts DW 0x64\n    nbrMin DW 0x21\n\n; Change any numbers less than min to min:\n.text\n    mov eax, 0x0\n    mov ebx, 0x0\n    mov edx, 0x0\n    mov ecx, [nbrElts]\nforCount0x1: cmp ebx, ecx\n           je endCount\nbody: cmp [ebx], [nbrMin]\n      jge endIfSmall\n      mov [ebx], [nbrMin]\nendIfSmall: add eax, [ebx]\n            inc ebx\n            jmp forCount0x1\nendCount: mov edx, eax\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .short 0x19, 0x2F, 0xF, 0x32, 0x20, 0x5F DUP (0xA)\n    nbrElts: .short 0x64\n    nbrMin: .short 0x21\n\n; Change any numbers less than min to min:\n.text\n    mov $0x0, %eax\n    mov $0x0, %ebx\n    mov $0x0, %edx\n    mov (nbrElts), %ecx\nforCount0x1: cmp %ecx, %ebx\n           je endCount\nbody: cmp (nbrMin), (%ebx)\n      jge endIfSmall\n      mov (nbrMin), (%ebx)\nendIfSmall: add (%ebx), %eax\n            inc %ebx\n            jmp forCount0x1\nendCount: mov %eax, %edx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .word 0x19, 0x2F, 0xF, 0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA\n    nbrElts: .word 0xA\n    nbrMin: .word 0x21\n\n; Change any numbers less than min to min:\n.text\n    0x40000 ADD R8, R0, R0\n    0x40004 ADD R9, R0, R0\n    0x40008 ADD R10, R0, R0\n    0x4000C ADD R11, R0, R0\n    0x40010 LW R16, 0x2C(R28)\n    0x40014 LW R17, 0x28(R28)\nFORCOUNT: 0x40018 BEQ R10, R17, 9\nBODY: 0x4001C LW R12, (R9)\n      0x40020 SLT R13, R16, R12\n      0x40024 BNE R13, R0, 1\n      0x40028 SW R16, (R9)\nENDIFSMALL: 0x4002C LW R11, (R9)\n            0x40030 ADD R8, R8, R11\n            0x40034 ADDI R9, R9, 4\n            0x40038 ADDI R10, R10, 1\n            0x4003C J 0x100060\nENDCOUNT: 0x40040 ADD R13, R0, R8';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Create an array\n    3FFEC ADDI R7, R0, A\n    3FFF0 SW R7, 100(R0)\n    3FFF4 ADDI R7, R0, 21\n    3FFF8 SW R7, 104(R0)\n    3FFFC ADDI R6, R0, 0\n    40000 ADDI R7, R0, 19\n    40004 SW R7, R6(R0)\n    40008 ADDI R6, R6, 4\n    4000C ADDI R7, R0, 2F\n    40010 SW R7, R6(R0)\n    40014 ADDI R6, R6, 4\n    40018 ADDI R7, R0, F\n    4001C SW R7, R6(R0)\n    40020 ADDI R6, R6, 4\n    40024 ADDI R7, R0, 32\n    40028 SW R7, R6(R0)\n    4002C ADDI R6, R6, 4\n    40030 ADDI R7, R0, 20\n    40034 SW R7, R6(R0)\n    40038 ADDI R6, R6, 4\n    4003C ADDI R7, R0, A\n    40040 ADDI R14, R14, 5\n    40044 BEQ R14, R0, 4\n    40048 SW R7, R6(R0)\n    4004C ADDI R6, R6, 4\n    40050 ADDI R14, R14, -1\n    40054 J 100110\n\n; Change any numbers in array less than 33 to 33:\n    40058 ADD R8, R0, R0\n    4005C ADD R9, R0, R0\n    40060 ADD R10, R0, R0\n    40064 ADD R11, R0, R0\n    40068 LW R16, 104(R28)\n    4006C LW R17, 100(R28)\n    40070 BEQ R10, R17, 9\n    40074 LW R12, (R9)\n    40078 SLT R13, R16, R12\n    4007C BNE R13, R0, 1\n    40080 SW R16, (R9)\n    40084 LW R11, (R9)\n    40088 ADD R8, R8, R11\n    4008C ADDI R9, R9, 4\n    40090 ADDI R10, R10, 1\n    40094 J 1001A0\n    40098 ADD R13, R0, R8';
	}
	else{
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .word 0x19, 0x2F, 0xF, 0x32, 0x20, 0xA, 0xA, 0xA, 0xA, 0xA\n    nbrElts: .word 0xA\n    nbrMin: .word 0x21\n\n; Change any numbers less than min to min:\n.text\n    0x40000 ADD X8, X0, X0\n    0x40004 ADD X9, X0, X0\n    0x40008 ADD X10, X0, X0\n    0x4000C ADD X11, X0, X0\n    0x40010 LW X16, 0x2C(X28)\n    0x40014 LW X17, 0x28(X28)\n\nFORCOUNT: 0x40018 BEQ X10, X17, 9\n\nBODY: 0x4001C LW X12, 0(X9)\n      0x40020 SLT X13, X16, X12\n      0x40024 BNE X13, X0, 1\n      0x40028 SW X16, 0(X9)\n\nENDIFSMALL: 0x4002C LW X11, 0(X9)\n            0x40030 ADD X8, X8, X11\n            0x40034 ADDI X9, X9, 4\n            0x40038 ADDI X10, X10, 1\n            0x4003C JR 0x100060\n\nENDCOUNT: 0x40040 ADD X13, X0, X8\n';
	}
	document.getElementById('id_code').value = codeString;
}
function sqrt_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare a number\n.data\n    number DW 0x64\n\n; Calculate square root of the number\n.text\n    mov eax, [number]\n    push ebx\n    push ecx\n    mov ebx, 0x0\nWhileLE: mov ecx, ebx\n         imul ecx, ebx\n         cmp ecx, eax\n         jnle EndWhileLE\n         inc ebx\n         jmp WhileLE\nEndWhileLE: dec ebx\n            mov eax, ebx\n            pop ecx\n            pop ebx';
	}
	else if (flavor === 'att'){
		codeString += '; Declare a number\n.data\n    number: .short 0x64\n\n; Calculate square root of the number\n.text\n    mov (number), %eax\n    push %ebx\n    push %ecx\n    mov $0x0, %ebx\nWhileLE: mov %ebx, %ecx\n         imul %ebx, %ecx\n         cmp %eax, %ecx\n         jnle EndWhileLE\n         inc %ebx\n         jmp WhileLE\nEndWhileLE: dec %ebx\n            mov %ebx, %eax\n            pop %ecx\n            pop %ebx';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare a number\n.data\n    number: .word 0x64\n\n; Calculate square root of the number\n.text\n    0x40000 LW R8, 0(R28)\n\nWHILELE: 0x40004 ADD R10, R0, R9\n         0x40008 MULT R10, R9\n         0x4000C MFLO R10\n         0x40010 SUB R11, R10, R8\n         0x40014 SLT R12, R0, R11\n         0x40018 BNE R12, R0, 2\n         0x4001C ADDI R9, R9, 1\n         0x40020 J 0x100010\nENDWHILELE: 0x40024 ADDI R9, R9, -1\n            0x40028 ADD R8, R0, R9\n            ';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Store a number\n    40000 ADDI R7, R0, 64\n    40004 SW R7, 100(R28)\n\n; Calculate square root of the number\n    40008 LW R8, 100(R28)\n    4000C ADD R10, R0, R9\n    40010 MULT R10, R9\n    40014 MFLO R10\n    40018 SUB R11, R10, R8\n    4001C SLT R12, R0, R11\n    40020 BNE R12, R0, 2\n    40024 ADDI R9, R9, 1\n    40028 J 100010\n    4002C ADDI R9, R9, -1\n    40030 ADD R8, R0, R9\n            ';
	}
	else{
		codeString += '; Declare a number\n.data\n    number: .word 0x64\n\n; Calculate square root of the number\n.text\n    0x40000 LW X8, 0(X28)\n\nWHILELE: 0x40004 ADD X10, X0, X9\n         0x40008 MUL X10, X10, X9\n         0x4000C SUB X11, X10, X8\n         0x40010 SLT X12, X0, X11\n         0x40014 ADDI X9, X9, 1\n         0x40018 BEQ X12, X0, -6\nENDWHILELE: 0x4001C ADDI X9, X9, -2\n            0x40020 ADD X8, X0, X9\n';
	}
	document.getElementById('id_code').value = codeString;
}
function arithShift_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += 'mov [0x4], 0x1\nmov eax, 0x4\nmov ebx, 0x2\nmov ecx, 0x8\nmov edx, 0x10\nadd ebx, ecx\nsub edx, ecx\nimul eax, [0x4]\nshl [0x4], 0x2\n';
	}
	else if (flavor === 'att'){
		codeString += 'movb $0x1, (0x4)\nmov $0x4, %eax\nmov $0x2, %ebx\nmov $0x8, %ecx\nmov $0x10, %edx\nadd %ecx, %ebx\nsub %ecx, %edx\nimul (0x4), %eax\nshl $0x2, (0x4)\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '0x400000 ADDI R8, R0, 4\n0x400004 ADDI R9, R0, 1\n0x400008 SW R9, 0(R8)\n0x40000C ADD R10, R0, R8\n0x400010 ADDI R11, R0, 2\n0x400014 ADDI R12, R0, 8\n0x400018 ADDI R13, R0, 0x10\n0x40001C ADD R11, R11, R12\n0x400020 SUB R13, R13, R12\n0x400024 MULT R10, R9\n0x400028 MFLO R10 \n0x40002C SLL R9, R9, 2\n0x400030 SW R9, 0(R8)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '400000 ADDI R8, R0, 4\n400004 ADDI R9, R0, 1\n400008 SW R9, 0(R8)\n40000C ADD R10, R0, R8\n400010 ADDI R11, R0, 2\n400014 ADDI R12, R0, 8\n400018 ADDI R13, R0, 10\n40001C ADD R11, R11, R12\n400020 SUB R13, R13, R12\n400024 MULT R10, R9\n400028 MFLO R10 \n40002C SLL R9, R9, 2\n400030 SW R9, 0(R8)';
	}
	else{
		codeString += '0x400000 ADDI X8, X0, 4\n0x400004 ADDI X9, X0, 1\n0x400008 SW X9, 0(X8)\n0x40000C ADD X10, X0, X8\n0x400010 ADDI X11, X0, 2\n0x400014 ADDI X12, X0, 8\n0x400018 ADDI X13, X0, 0X10\n0x40001C ADD X11, X11, X12\n0x400020 SUB X13, X13, X12\n0x400024 MUL X10, X10, X9\n0x400028 SLLI X9, X9, 2\n0x40002C SW X9, 0(X8)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function array_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element -50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x DB 0x3, 0x8, 0x5, 0x2\n    y DW 0xD DUP (-0x32)\n    z DD 'hello', 0x0\n\n; Store array values\n.text\n    mov eax, [x] \n    mov ebx, [y+0x4]\n    mov ecx, [z+0x3]\n    mov edx, [x+0x2]";
	}
	else if (flavor === 'att'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .byte 0x3, 0x8, 0x5, 0x2\n    y: .short 0xD DUP (-0x32)\n    z: .long 'hello', 0x0\n\n; Store array values\n.text\n    mov (x), %eax \n    mov 0x4(y), %ebx\n    mov 0x3(z), %ecx\n    mov 0x2(x), %edx";
	}
	else if (flavor === 'mips_asm'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .word 0x3, 0x8, 0x5, 0x2\n    y: .word 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32\n    z: .word 'hello', 0\n\n; Store array values\n.text\n    0x400000 LW R8, 0(R28) \n    0x400004 LW R9, 0x20(R28)\n    0x400008 LW R10, 0x50(R28)\n    0x40000C LW R11, 0x8(R28)";
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Declare array 3, 8, 5, 2, 32, 32, etc.\n\n\t400000 ADDI R12, R12, 3\n\t400004 SW R12, 0(R0)\n\t400008 ADDI R12, R12, 5\n\t40000C SW R12, 4(R0)\n\t400010 ADDI R12, R12, -3\n\t400014 SW R12, 8(R0)\n\t400018 ADDI R12, R12, -3\n\t40001C SW R12, C(R0)\n\t400020 ADDI R12, R0, 32\n\t400024 ADDI R13, R0, 10\n\t400028 ADDI R14, R0, 38\n\t40002C BEQ R13, R14, 3\n\t400030 SW R12, R13(R0)\n\t400034 ADDI R13, R13, 4\n\t400038 J 10000B0\n\n    40003C LW R8, 0(R28) \n    400040 LW R9, 20(R28)';
	}
	else{
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .word 0x3, 0x8, 0x5, 0x2\n    y: .word 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32, 0x32\n    z: .word 'hello', 0\n\n; Store array values\n.text\n    0x400000 LW X8, 0(X28) \n    0x400004 LW X9, 0x20(X28)\n    0x400008 LW X10, 0x50(X28)\n    0x40000C LW X11, 0x8(X28)\n";
	}
	document.getElementById('id_code').value = codeString;
}
function keyInterrupt_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Asking for key input\nINT 0x16\nMOV EBX, EAX\nMOV ECX, 0x0\nMOV ESI, 0x0\n\n; Move input to memory location esi\n; Ask for key input again\nL0x1: MOV [ESI], EAX\nMOV EAX, 0x0\nINT 0x16\nINC ECX\nCMP EBX,EAX\nINC ESI\nJNE L0x1\n\n; Ask for key input \nL0x0x2: MOV EAX, 0\nINT 0x16\nDEC ECX\nCMP ECX, 0x1\nJNE L0x2\n\nMOV EAX, 0x0\nINT 0x16\nMOV EBX, EAX\n\n; Move input to memory location esi\n; Ask for key input again\nL0x3: MOV [ESI], EAX\nINC ESI\nMOV EAX, 0x0\nINT 0x16\nCMP EBX, EAX\nJNE L0x3\n';
	}
	else if (flavor === 'att'){
		codeString += '; Asking for key input\nINT $0x16\nMOV %EAX, %EBX\nMOV $0x0, %ECX\nMOV $0x0, %ESI\n\n; Move input to memory location esi\n; Ask for key input again\nL0x1: MOV %EAX, (%ESI)\nMOV $0x0, %EAX\nINT $0x16\nINC %ECX\nCMP %EAX, %EBX\nINC %ESI\nJNE L0x1\n\n; Asking for key input\nL0x0x2: MOV $0, %EAX\nINT $0x16\nDEC %ECX\nCMP $0x1, %ECX\nJNE L0x2\n\nMOV $0x0, %EAX\nINT $0x16\nMOV %EAX, %EBX\n\n; Move input to memory location esi\n; Ask for key input again\nL0x3: MOV %EAX, (%ESI)\nINC %ESI\nMOV $0x0, %EAX\nINT $0x16\nCMP %EAX, %EBX\nJNE L0x3\n';
	}
	document.getElementById('id_code').value = codeString;
}
function dataAccess_hex(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare arrays\n.data\n    x DB 0x1, 0x2, 0x3, 0x4, 0x5\n    y DW 0x2, 0x36, 0x20, 0x8\n    z DD 0xA DUP (0x32)\n\n; Storing values into memory using register arithmetic\n.text\n    mov eax, 0x6\n    mov [eax], [x+0x2]\n    mov [eax+0x2], [y+0x3]\n    mov [ebx], [z]\n    mov [eax-0x5], [y+0x2]\n    mov [-0x5+eax], [y+0x2]';
	}
	else if (flavor === 'att'){
		codeString += '; Declare arrays\n.data\n    x: .byte 0x1, 0x2, 0x3, 0x4, 0x5\n    y: .short 0x2, 0x36, 0x20, 0x8\n    z: .long 0xA DUP (0x32)\n\n; Storing values into memory using register arithmetic\n.text\n\tmov $0x6, %eax\n\tmov 0x2(x), (%eax)\n\tmov 0x3(y), 0x2(%eax)\n\tmov (z), (%ebx)\n\tmov 0x3, %ecx\n\tmov 0x2(y), -0x5(%eax, 0x3)\n\tmov 0x4(x), (%eax, 0x2, %ecx)\n\tmov 0x4(x), 0xC(%eax, 0x2, %ecx)\n\tmov 0x4(x), 0xC(%eax, 0x2, %ecx, 0x4)';
	}
	document.getElementById('id_code').value = codeString;
}
