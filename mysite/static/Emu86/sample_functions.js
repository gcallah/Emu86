function addTwo(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare number and sum.\n.data\n    number DW -105\n    sum DW ?\n\n; Store first number to EAX\n; Add 158 to value in EAX\n; Store total to sum\n.text\n    mov eax, [number]\n    add eax, 158\n    mov [sum], eax\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare number and sum.\n.data\n    number: .short -105\n    sum: .short ?\n\n; Store first number to EAX\n; Add 158 to value in EAX\n; Store total to sum\n.text\n    mov (number), %eax\t\t\n    add $158, %eax\t\n    mov %eax, (sum)';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare number and sum.\n.data\n    number: .word -105\n    sum: .word 0\n\n; Store first number to R8\n; Add 158 to value in R8\n; Store total to sum\n.text\n    262144 LW R8, 0(R28)\t\t\n    262148 ADDI R8, R8, 158\t\n    262152 SW R8, 4(R28)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Store first addend\n    40000 ADDI R7, R0, 69\n    40004 SW R7, 20(R28)\n\n; Load first number to R8\n; Add 158 to value in R8\n; Store sum to next location\n    40008 LW R8, 20(R28)\t\t\n    4000C ADDI R8, R8, 9E\t\n    40010 SW R8, 24(R28)';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare number and sum.\n.data\n    number: .word -105\n    sum: .word 0\n\n; Store first number to X8\n; Add 158 to value in X8\n; Store total to sum\n.text\n    262144 LW X8, 0(X28)\t\t\n    262148 ADDI X8, X8, 158\t\n    262152 SW X8, 4(X28)\n';
	}
	else{
		codeString += 'i32.const -105\nglobal number\nglobal.set number\ni32.const 158\nglobal.get number\ni32.add';
	}
	document.getElementById('id_code').value = codeString;
}
function arithExpr(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare x, y, and z variables \n.data\n    x DW 35\n    y DW 47\n    z DW 26\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    mov eax, [x]\t\t\n    add eax, [y]\t\n    mov ebx, [z]\n    add ebx, ebx\n    sub eax, ebx\n    inc eax \n    neg eax';
	}
	else if (flavor === 'att'){
		codeString += '; Declare x, y, and z variables \n.data\n    x: .short 35\n    y: .short 47\n    z: .short 26\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    mov (x), %eax\t\t\n    add (y), %eax\t\n    mov (z), %ebx\n    add %ebx, %ebx\n    sub %ebx, %eax\n    inc %eax \n    neg %eax';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare x, y, and z variables \n.data\n    x: .word 35\n    y: .word 47\n    z: .word 26\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    262144 LW R8, 0(R28)\n    262148 LW R9, 4(R28)\n    262152 ADD R8, R8, R9\n    262156 LW R10, 8(R28)\n    262160 ADD R10, R10, R10\n    262164 SUB R8, R8, R10\n    262168 ADDI R8, R8, 1\n    262172 SUB R8, R0, R8';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Calculate -(x + y - 2 * z + 1)\n; x = 35, y = 47, z = 26\n\n    40000 ADDI R8, R0, 23\n    40004 ADDI R9, R9, 2F\n    40008 ADD R8, R8, R9\n    4000C ADDI R10, R0, 1A\n    40010 ADD R10, R10, R10\n    40014 SUB R8, R8, R10\n    40018 ADDI R8, R8, 1\n    4001C SUB R8, R0, R8';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare x, y, and z variables \n.data\n    x: .word 35\n    y: .word 47\n    z: .word 26\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    262144 LW X8, 0(X28)\n    262148 LW X9, 4(X28)\n    262152 ADD X8, X8, X9\n    262156 LW X10, 8(X28)\n    262160 ADD X10, X10, X10\n    262164 SUB X8, X8, X10\n    262168 ADDI X8, X8, 1\n    262172 SUB X8, X0, X8\n';
	}
	document.getElementById('id_code').value = codeString;
}
function area(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare length and width\n.data\n    long DW 35\n    wide DW 27\n\n; Calculate area of rectangle\n.text\n    mov eax, [long]\n    imul eax, [wide]\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare length and width\n.data\n    long: .short 35\n    wide: .short 27\n\n; Calculate area of rectangle\n.text\n    mov (long), %eax\n    imul (wide), %eax';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare length and width\n.data\n    long: .word 35\n    wide: .word 27\n\n; Calculate area of rectangle\n.text\n    262144 LW R8, 0(R28)\n    262148 LW R9, 4(R28)\n    262152 MULT R8, R9\n    262156 MFLO R10';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Calculate area of rectangle\n    40000 ADDI R8, R0, 23\n    40004 ADDI R9, R0, 1B\n    40008 MULT R8, R9\n    4000C MFLO R10\n    40010 SW R10, 1000(R0)';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare length and width\n.data\n    long: .word 35\n    wide: .word 27\n\n; Calculate area of rectangle\n.text\n    262144 LW X8, 0(X28)\n    262148 LW X9, 4(X28)\n    262152 MUL X10, X8, X9\n';
	}
	document.getElementById('id_code').value = codeString;
}
function power(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; In edx, we put the number to raise to the power we put in ebx.\n      mov edx, 2\n      mov ebx, 16\n      call power\n      mov eax, 0\n      int 32\n\npower: mov ecx, edx\nloop: imul edx, ecx\n      dec ebx\n      cmp ebx, 1\n      jne loop\n      ret\n';
	}
	else if (flavor === 'att'){
		codeString += '; In edx, we put the number to raise to the power we put in ebx.\n      mov $2, %edx\n      mov $16, %ebx\n      call power\n      mov $0, %eax\n      int $32\n\npower: mov %edx, %ecx\nloop: imul %ecx, %edx\n      dec %ebx\n      cmp %ebx, $1\n      jne loop\n      ret\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; In R8, we put the number to raise to the power we put in R9.\n      4194304 ADDI R8, R0, 2\n      4194308 ADDI R9, R9, 16\n      4194312 JAL 16777280\n      4194316 SYSCALL\n\npower: 4194320 ADD R16, R0, R8\nloop: 4194324 MULT R8, R16\n      4194328 MFLO R8\n      4194332 ADDI R9, R9, -1\n      4194336 ADDI R10, R0, 1\n      4194340 BNE R9, R10, -5\n      4194344 JR R31';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; In R8, we put the number to raise to the power we put in R9.\n    400000 ADDI R8, R0, 2\n    400004 ADDI R9, R9, 10\n    400008 JAL 1000040\n    40000C SYSCALL\n\n    400010 ADD R16, R0, R8\n    400014 MULT R8, R16\n    400018 MFLO R8\n    40001C ADDI R9, R9, -1\n    400020 ADDI R10, R0, 1\n    400024 BNE R9, R10, -5\n    400028 JR R31';
	}
	else if (flavor === 'riscv'){
		codeString += '; In X8, we put the number to raise to the power we put in X9.\n     4194304 ADDI X8, X0, 2\n     4194308 ADDI X9, X9, 16\n      4194312 ADD X16, X0, X8\nloop: 4194316 MUL X8, X8, X16\n      4194320 ADDI X9, X9, -1\n      4194324 ADDI X10, X0, 1\n      4194328 BNE X9, X10, -4\n      4194332 SYSCALL\n\n';
	}
	document.getElementById('id_code').value = codeString;
}
function data(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x DB 8\n    y DW 16\n    z DD 32\n\n; Next is the .text section, where we use them:\n.text\n    mov eax, [x]\n    mov ebx, [y]\n    mov ecx, [z]\n';
	}
	else if (flavor === 'att'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .byte 8\n    y: .short 16\n    z: .long 32\n\n; Next is the .text section, where we use them:\n.text\n    mov (x), %eax\n    mov (y), %ebx\n    mov (z), %ecx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .word 8\n    y: .word 16\n    z: .word 32\n\n; Next is the .text section, where we use them:\n.text\n    4194304 LW R8, 0(R28)\n    4194308 LW R9, 4(R28)\n    4194312 LW R10, 8(R28)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Storing and fetching data\n    400000 ADDI R7, R0, 8\n    400004 SW R7, 0(R28)\n    400008 ADDI R7, R7, 8\n    40000C SW R7, 4(R28)\n    400010 ADDI R7, R7, 10\n    400014 SW R7, 8(R28)\n\n    400018 LW R8, 0(R28)\n    40001C LW R9, 4(R28)\n    400020 LW R10, 8(R28)';
	}
	else if (flavor === 'riscv'){
		codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .word 8\n    y: .word 16\n    z: .word 32\n\n; Next is the .text section, where we use them:\n.text\n    4194304 LW X8, 0(X28)\n    4194308 LW X9, 4(X28)\n    4194312 LW X10, 8(X28)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function loop(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '      mov eax, 16\n      mov ebx, 0\n\n; Compare eax and ebx and loop until equal\nloop: cmp eax, ebx\n      jz done\n      inc ebx\n      dec edx\n      jnz loop\n\ndone: mov ecx, ebx  ; when done, store ebx in ecx\n';
	}
	else if (flavor === 'att'){
		codeString += '      mov $16, %eax\n      mov $0, %ebx\n\n; Compare eax and ebx and loop until equal\nloop: cmp %eax, %ebx\n      jz done\n      inc %ebx\n      dec %edx\n      jnz loop\n\ndone: mov %ebx, %ecx  ; when done, store ebx in ecx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Compare R8 and R9 and loop until equal\n; When done, store R9 to R11\n    262144 ADDI R8, R0, 10\n    262148 ADD R9, R0, R0\n    262152 ADDI R9, R9, 1\n    262156 ADDI R10, R10, -1\n    262160 BNE R8, R9, -3\n    262164 ADD R11, R11, R9';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Compare R8 and R9 and loop until equal\n; When done, store R9 to R11\n    40000 ADDI R8, R0, 10\n    40004 ADD R9, R0, R0\n    40008 ADDI R9, R9, 1\n    4000C ADDI R10, R10, -1\n    40010 BNE R8, R9, -3\n    40014 ADD R11, R11, R9';
	}
	else if (flavor === 'riscv'){
		codeString += '; Compare X8 and X9 and loop until equal\n; When done, store X9 to X11\n    262144 ADDI X8, X0, 10\n    262148 ADD X9, X0, X0\n    262152 ADDI X9, X9, 1\n    262156 ADDI X10, X10, -1\n    262160 BNE X8, X9, -3\n    262164 ADD X11, X11, X9\n';
	}
	document.getElementById('id_code').value = codeString;
}
function log(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare a number\n.data\n    number DW 759\n\n; Calculating log (base 2) of a number\n.text\n    mov ecx, 0\n    mov eax, 1\nwhileLE: cmp eax, [number]\n         jnle endWhileLE\nbody: add eax, eax\n      inc ecx\n      jmp whileLE\n\nendWhileLE: dec ecx ';
	}
	else if (flavor === 'att'){
		codeString += '; Declare a number\n.data\n    number: .short 759\n\n; Calculating log (base 2) of a number\n.text\n    mov $0, %ecx\n    mov $1, %eax\nwhileLE: cmp (number), %eax\n         jnle endWhileLE\nbody: add %eax, %eax\n      inc %ecx\n      jmp whileLE\n\nendWhileLE: dec %ecx ';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare a number\n.data\n    number: .word 477\n\n; Calculating log (base 2) of a number\n.text\n    262144 ADD R8, R8, R0\n    262148 ADDI R9, R9, 1\n    262152 LW R10, 0(R28)\n\nWHILELE: 262156 SUB R11, R9, R10\n         262160 SLT R12, R0, R11\n         262164 BNE R12, R0, 3\nBODY: 262168 ADD R9, R9, R9\n      262172 ADDI R8, R8, 1\n      262176 J 1048624\n\nENDWHILELE: 262180 ADDI R8, R8, -1';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Calculating log (base 2) of 759\n    40000 ADD R8, R8, R0\n    40004 ADDI R9, R9, 1\n    40008 ADDI R10, R0, 2F7\n\n    4000C SUB R11, R9, R10\n    40010 SLT R12, R0, R11\n    40014 BNE R12, R0, 3\n    40018 ADD R9, R9, R9\n    4001C ADDI R8, R8, 1\n    40020 J 100030\n\n    40024 ADDI R8, R8, -1';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare a number\n.data\n    number: .word 477\n\n; Calculating log (base 2) of a number\n.text\n    262144 ADD X8, X8, X0\n    262148 ADDI X9, X9, 1\n    262152 LW X10, 0(X28)\n\nWHILELE: 262156 SUB X11, X9, X10\n         262160 SLT X12, X0, X11\n         262164 BNE X12, X0, 3\nBODY: 262168 ADD X9, X9, X9\n      262172 ADDI X8, X8, 1\n      262176 BEQ X0, X0, -6\n\nENDWHILELE: 262180 ADDI X8, X8, -1\n';
	}
	document.getElementById('id_code').value = codeString;
}
function avg(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray DW 25, 47, -15, -50, 32, 95 DUP (10)\n    nbrElts DW 100\n\n; Calculate the average of the array:\n.text\n    mov eax, 0\n    mov ebx, 0\n    mov edx, 0\n    mov ecx, [nbrElts]\nforCount1: cmp ebx, ecx\n           je endCount\nbody: add eax, [ebx]\n      inc ebx\n      jmp forCount1\nendCount: idiv ecx\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray: .short 25, 47, -15, -50, 32, 95 DUP (10)\n    nbrElts: .short 100\n\n; Calculate the average of the array:\n.text\n    mov $0, %eax\n    mov $0, %ebx\n    mov $0, %edx\n    mov (nbrElts), %ecx\nforCount1: cmp %ebx, %ecx\n           je endCount\nbody: add (%ebx), %eax\n      inc %ebx\n      jmp forCount1\nendCount: idiv %ecx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray: .word 25, 47, -15, -50, 32, 10, 10, 10, 10, 10\n    nbrElts: .word 10\n\n; Calculate the average of the array:\n.text\n    262144 ADD R8, R0, R0\n    262148 ADD R9, R0, R0\n    262152 LW R16, 28(R28)\n    262156 ADD R10, R0, R0\nFORCOUNT: 262160 BEQ R9, R16, 5\nBODY: 262164 LW R11, (R10)\n      262168 ADD R8, R8, R11\n      262172 ADDI R9, R9, 1\n      262176 ADDI R10, R10, 4\n      262180 J 1048640\nENDCOUNT: 262184 DIV R8, R16\n262188 MFLO R12\n262192 MFHI R13\n';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Create an array\n    3FFF4 ADDI R7, R0, A\n    3FFF8 SW R7, 104(R0)\n    3FFFC ADDI R6, R0, 0\n    40000 ADDI R7, R0, 19\n    40004 SW R7, R6(R0)\n    40008 ADDI R6, R6, 4\n    4000C ADDI R7, R0, 2F\n    40010 SW R7, R6(R0)\n    40014 ADDI R6, R6, 4\n    40018 ADDI R7, R0, -F\n    4001C SW R7, R6(R0)\n    40020 ADDI R6, R6, 4\n    40024 ADDI R7, R0, -32\n    40028 SW R7, R6(R0)\n    4002C ADDI R6, R6, 4\n    40030 ADDI R7, R0, 20\n    40034 SW R7, R6(R0)\n    40038 ADDI R6, R6, 4\n    4003C ADDI R7, R0, A\n    40040 ADDI R14, R14, 5\n    40044 BEQ R14, R0, 4\n    40048 SW R7, R6(R0)\n    4004C ADDI R6, R6, 4\n    40050 ADDI R14, R14, -1\n    40054 J 100110\n\n; Calculate the average of the array:\n    40058 ADD R8, R0, R0\n    4005C ADD R9, R0, R0\n    40060 LW R16, 104(R28)\n    40064 ADD R10, R0, R0\n    40068 BEQ R9, R16, 5\n    4006C LW R11, (R10)\n    40070 ADD R8, R8, R11\n    40074 ADDI R9, R9, 1\n    40078 ADDI R10, R10, 4\n    4007C J 1001A0\n    40080 DIV R8, R16\n    40084 MFLO R12\n    40088 MFHI R13\n';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare an array and declare size of the array\n.data\n    nbrArray: .word 25, 47, -15, -50, 32, 10, 10, 10, 10, 10\n    nbrElts: .word 10\n\n; Calculate the average of the array:\n.text\n    262144 ADD X8, X0, X0\n    262148 ADD X9, X0, X0\n    262152 LW X16, 28(X28)\n    262156 ADD X10, X0, X0\nBODY: 262160 LW X11, 0(X10)\n      262164 ADD X8, X8, X11\n      262168 ADDI X9, X9, 1\n      262172 ADDI X10, X10, 4\n      262176 BNE X9, X16, -5\nENDCOUNT: 262180 DIV X17, X8, X16\n';
	}
	document.getElementById('id_code').value = codeString;
}
function celFah(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp DW 35\n    fTemp DW ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov eax, [cTemp]\n    imul eax, 9\n    add eax, 2\n    mov ebx, 5\n    idiv ebx \n    add eax, 32\n    mov [fTemp], eax';
	}
	else if (flavor === 'att'){
		codeString += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp: .short 35\n    fTemp: .short ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov (cTemp), %eax\n    imul $9, %eax\n    add $2, %eax\n    mov $5, %ebx\n    idiv %ebx \n    add $32, %eax\n    mov %eax, (fTemp)';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare a Celsius temperature\n\n.data\n    cTemp: .word 35\n    fTemp: .word 0\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    262144 LW R8, 0(R28)\n    262148 ADDI R9, R0, 9\n    262152 MULT R8, R9\n    262156 MFLO R8\n    262160 ADDI R8, R8, 2\n    262164 ADDI R9, R0, 5\n    262168 DIV R8, R9\n    262172 MFLO R8\n    262176 ADDI R8, R8, 32\n    262180 SW R8, 4(R28)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Convert from Celsius to Fahrenheit\n; Store result in memory location 100\n    40000 ADDI R8, R0, 23\n    40004 ADDI R9, R0, 9\n    40008 MULT R8, R9\n    4000C MFLO R8\n    40010 ADDI R8, R8, 2\n    40014 ADDI R9, R0, 5\n    40018 DIV R8, R9\n    4001C MFLO R8\n    40020 ADDI R8, R8, 20\n    40024 SW R8, 100(R28)';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare a Celsius temperature\n\n.data\n    cTemp: .word 35\n    fTemp: .word 0\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    262144 LW X8, 0(X28)\n    262148 ADDI X9, X0, 9\n    262152 MUL X8, X8, X9\n    262156 ADDI X8, X8, 2\n    262160 ADDI X9, X0, 5\n    262164 DIV X8, X8, X9\n    262168 ADDI X8, X8, 32\n    262172 SW X8, 4(X28)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function modify(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray DW 25, 47, 15, 50, 32, 95 DUP (10)\n    nbrElts DW 100\n    nbrMin DW 33\n\n; Change any numbers less than min to min:\n.text\n    mov eax, 0\n    mov ebx, 0\n    mov edx, 0\n    mov ecx, [nbrElts]\nforCount1: cmp ebx, ecx\n           je endCount\nbody: cmp [ebx], [nbrMin]\n      jge endIfSmall\n      mov [ebx], [nbrMin]\nendIfSmall: add eax, [ebx]\n            inc ebx\n            jmp forCount1\nendCount: mov edx, eax\n';
	}
	else if (flavor === 'att'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .short 25, 47, 15, 50, 32, 95 DUP (10)\n    nbrElts: .short 100\n    nbrMin: .short 33\n\n; Change any numbers less than min to min:\n.text\n    mov $0, %eax\n    mov $0, %ebx\n    mov $0, %edx\n    mov (nbrElts), %ecx\nforCount1: cmp %ecx, %ebx\n           je endCount\nbody: cmp (nbrMin), (%ebx)\n      jge endIfSmall\n      mov (nbrMin), (%ebx)\nendIfSmall: add (%ebx), %eax\n            inc %ebx\n            jmp forCount1\nendCount: mov %eax, %edx\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .word 25, 47, 15, 50, 32, 10, 10, 10, 10, 10\n    nbrElts: .word 10\n    nbrMin: .word 33\n\n; Change any numbers less than min to min:\n.text\n    262144 ADD R8, R0, R0\n    262148 ADD R9, R0, R0\n    262152 ADD R10, R0, R0\n    262156 ADD R11, R0, R0\n    262160 LW R16, 44(R28)\n    262164 LW R17, 40(R28)\nFORCOUNT: 262168 BEQ R10, R17, 9\nBODY: 262172 LW R12, (R9)\n      262176 SLT R13, R16, R12\n      262180 BNE R13, R0, 1\n      262184 SW R16, (R9)\nENDIFSMALL: 262188 LW R11, (R9)\n            262192 ADD R8, R8, R11\n            262196 ADDI R9, R9, 4\n            262200 ADDI R10, R10, 1\n            262204 J 1048672\nENDCOUNT: 262208 ADD R13, R0, R8';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Create an array\n    3FFEC ADDI R7, R0, A\n    3FFF0 SW R7, 100(R0)\n    3FFF4 ADDI R7, R0, 21\n    3FFF8 SW R7, 104(R0)\n    3FFFC ADDI R6, R0, 0\n    40000 ADDI R7, R0, 19\n    40004 SW R7, R6(R0)\n    40008 ADDI R6, R6, 4\n    4000C ADDI R7, R0, 2F\n    40010 SW R7, R6(R0)\n    40014 ADDI R6, R6, 4\n    40018 ADDI R7, R0, F\n    4001C SW R7, R6(R0)\n    40020 ADDI R6, R6, 4\n    40024 ADDI R7, R0, 32\n    40028 SW R7, R6(R0)\n    4002C ADDI R6, R6, 4\n    40030 ADDI R7, R0, 20\n    40034 SW R7, R6(R0)\n    40038 ADDI R6, R6, 4\n    4003C ADDI R7, R0, A\n    40040 ADDI R14, R14, 5\n    40044 BEQ R14, R0, 4\n    40048 SW R7, R6(R0)\n    4004C ADDI R6, R6, 4\n    40050 ADDI R14, R14, -1\n    40054 J 100110\n\n; Change any numbers in array less than 33 to 33:\n    40058 ADD R8, R0, R0\n    4005C ADD R9, R0, R0\n    40060 ADD R10, R0, R0\n    40064 ADD R11, R0, R0\n    40068 LW R16, 104(R28)\n    4006C LW R17, 100(R28)\n    40070 BEQ R10, R17, 9\n    40074 LW R12, (R9)\n    40078 SLT R13, R16, R12\n    4007C BNE R13, R0, 1\n    40080 SW R16, (R9)\n    40084 LW R11, (R9)\n    40088 ADD R8, R8, R11\n    4008C ADDI R9, R9, 4\n    40090 ADDI R10, R10, 1\n    40094 J 1001A0\n    40098 ADD R13, R0, R8';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .word 25, 47, 15, 50, 32, 10, 10, 10, 10, 10\n    nbrElts: .word 10\n    nbrMin: .word 33\n\n; Change any numbers less than min to min:\n.text\n    262144 ADD X8, X0, X0\n    262148 ADD X9, X0, X0\n    262152 ADD X10, X0, X0\n    262156 ADD X11, X0, X0\n    262160 LW X16, 44(X28)\n    262164 LW X17, 40(X28)\n\nFORCOUNT: 262168 BEQ X10, X17, 9\n\nBODY: 262172 LW X12, 0(X9)\n      262176 SLT X13, X16, X12\n      262180 BNE X13, X0, 1\n      262184 SW X16, 0(X9)\n\nENDIFSMALL: 262188 LW X11, 0(X9)\n            262192 ADD X8, X8, X11\n            262196 ADDI X9, X9, 4\n            262200 ADDI X10, X10, 1\n            262204 JR 1048672\n\nENDCOUNT: 262208 ADD X13, X0, X8\n';
	}
	document.getElementById('id_code').value = codeString;
}
function sqrt(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare a number\n.data\n    number DW 100\n\n; Calculate square root of the number\n.text\n    mov eax, [number]\n    push ebx\n    push ecx\n    mov ebx, 0\nWhileLE: mov ecx, ebx\n         imul ecx, ebx\n         cmp ecx, eax\n         jnle EndWhileLE\n         inc ebx\n         jmp WhileLE\nEndWhileLE: dec ebx\n            mov eax, ebx\n            pop ecx\n            pop ebx';
	}
	else if (flavor === 'att'){
		codeString += '; Declare a number\n.data\n    number: .short 100\n\n; Calculate square root of the number\n.text\n    mov (number), %eax\n    push %ebx\n    push %ecx\n    mov $0, %ebx\nWhileLE: mov %ebx, %ecx\n         imul %ebx, %ecx\n         cmp %eax, %ecx\n         jnle EndWhileLE\n         inc %ebx\n         jmp WhileLE\nEndWhileLE: dec %ebx\n            mov %ebx, %eax\n            pop %ecx\n            pop %ebx';
	}
	else if (flavor === 'mips_asm'){
		codeString += '; Declare a number\n.data\n    number: .word 100\n\n; Calculate square root of the number\n.text\n    262144 LW R8, 0(R28)\n\nWHILELE: 262148 ADD R10, R0, R9\n         262152 MULT R10, R9\n         262156 MFLO R10\n         262160 SUB R11, R10, R8\n         262164 SLT R12, R0, R11\n         262168 BNE R12, R0, 2\n         262172 ADDI R9, R9, 1\n         262176 J 1048592\nENDWHILELE: 262180 ADDI R9, R9, -1\n            262184 ADD R8, R0, R9\n            ';
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Store a number\n    40000 ADDI R7, R0, 64\n    40004 SW R7, 100(R28)\n\n; Calculate square root of the number\n    40008 LW R8, 100(R28)\n    4000C ADD R10, R0, R9\n    40010 MULT R10, R9\n    40014 MFLO R10\n    40018 SUB R11, R10, R8\n    4001C SLT R12, R0, R11\n    40020 BNE R12, R0, 2\n    40024 ADDI R9, R9, 1\n    40028 J 100010\n    4002C ADDI R9, R9, -1\n    40030 ADD R8, R0, R9\n            ';
	}
	else if (flavor === 'riscv'){
		codeString += '; Declare a number\n.data\n    number: .word 100\n\n; Calculate square root of the number\n.text\n    262144 LW X8, 0(X28)\n\nWHILELE: 262148 ADD X10, X0, X9\n         262152 MUL X10, X10, X9\n         262156 SUB X11, X10, X8\n         262160 SLT X12, X0, X11\n         262164 ADDI X9, X9, 1\n         262168 BEQ X12, X0, -6\nENDWHILELE: 262172 ADDI X9, X9, -2\n            262176 ADD X8, X0, X9\n';
	}
	document.getElementById('id_code').value = codeString;
}
function arithShift(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += 'mov [4], 1\nmov eax, 4\nmov ebx, 2\nmov ecx, 8\nmov edx, 16\nadd ebx, ecx\nsub edx, ecx\nimul eax, [4]\nshl [4], 2\n';
	}
	else if (flavor === 'att'){
		codeString += 'movb $1, (4)\nmov $4, %eax\nmov $2, %ebx\nmov $8, %ecx\nmov $16, %edx\nadd %ecx, %ebx\nsub %ecx, %edx\nimul (4), %eax\nshl $2, (4)\n';
	}
	else if (flavor === 'mips_asm'){
		codeString += '4194304 ADDI R8, R0, 4\n4194308 ADDI R9, R0, 1\n4194312 SW R9, 0(R8)\n4194316 ADD R10, R0, R8\n4194320 ADDI R11, R0, 2\n4194324 ADDI R12, R0, 8\n4194328 ADDI R13, R0, 16\n4194332 ADD R11, R11, R12\n4194336 SUB R13, R13, R12\n4194340 MULT R10, R9\n4194344 MFLO R10 \n4194348 SLL R9, R9, 2\n4194352 SW R9, 0(R8)';
	}
	else if (flavor === 'mips_mml'){
		codeString += '400000 ADDI R8, R0, 4\n400004 ADDI R9, R0, 1\n400008 SW R9, 0(R8)\n40000C ADD R10, R0, R8\n400010 ADDI R11, R0, 2\n400014 ADDI R12, R0, 8\n400018 ADDI R13, R0, 10\n40001C ADD R11, R11, R12\n400020 SUB R13, R13, R12\n400024 MULT R10, R9\n400028 MFLO R10 \n40002C SLL R9, R9, 2\n400030 SW R9, 0(R8)';
	}
	else if (flavor === 'riscv'){
		codeString += '4194304 ADDI X8, X0, 4\n4194308 ADDI X9, X0, 1\n4194312 SW X9, 0(X8)\n4194316 ADD X10, X0, X8\n4194320 ADDI X11, X0, 2\n4194324 ADDI X12, X0, 8\n4194328 ADDI X13, X0, 0X10\n4194332 ADD X11, X11, X12\n4194336 SUB X13, X13, X12\n4194340 MUL X10, X10, X9\n4194344 SLLI X9, X9, 2\n4194348 SW X9, 0(X8)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function array(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element -50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x DB 3, 8, 5, 2\n    y DW 13 DUP (-50)\n    z DD 'hello', 0\n\n; Store array values\n.text\n    mov eax, [x] \n    mov ebx, [y+4]\n    mov ecx, [z+3]\n    mov edx, [x+2]";
	}
	else if (flavor === 'att'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .byte 3, 8, 5, 2\n    y: .short 13 DUP (-50)\n    z: .long 'hello', 0\n\n; Store array values\n.text\n    mov (x), %eax \n    mov 4(y), %ebx\n    mov 3(z), %ecx\n    mov 2(x), %edx";
	}
	else if (flavor === 'mips_asm'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .word 3, 8, 5, 2\n    y: .word 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50\n    z: .word 'hello', 0\n\n; Store array values\n.text\n    4194304 LW R8, 0(R28) \n    4194308 LW R9, 32(R28)\n    4194312 LW R10, 80(R28)\n    4194316 LW R11, 8(R28)";
	}
	else if (flavor === 'mips_mml'){
		codeString += '; Declare array 3, 8, 5, 2, 32, 32, etc.\n\n\t400000 ADDI R12, R12, 3\n\t400004 SW R12, 0(R0)\n\t400008 ADDI R12, R12, 5\n\t40000C SW R12, 4(R0)\n\t400010 ADDI R12, R12, -3\n\t400014 SW R12, 8(R0)\n\t400018 ADDI R12, R12, -3\n\t40001C SW R12, C(R0)\n\t400020 ADDI R12, R0, 32\n\t400024 ADDI R13, R0, 10\n\t400028 ADDI R14, R0, 38\n\t40002C BEQ R13, R14, 3\n\t400030 SW R12, R13(R0)\n\t400034 ADDI R13, R13, 4\n\t400038 J 10000B0\n\n    40003C LW R8, 0(R28) \n    400040 LW R9, 20(R28)';
	}
	else if (flavor === 'riscv'){
		codeString += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .word 3, 8, 5, 2\n    y: .word 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50\n    z: .word 'hello', 0\n\n; Store array values\n.text\n    4194304 LW X8, 0(X28) \n    4194308 LW X9, 32(X28)\n    4194312 LW X10, 80(X28)\n    4194316 LW X11, 8(X28)\n";
	}
	document.getElementById('id_code').value = codeString;
}
function keyInterrupt(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Asking for key input\nINT 22\nMOV EBX, EAX\nMOV ECX, 0\nMOV ESI, 0\n\n; Move input to memory location esi\n; Ask for key input again\nL1: MOV [ESI], EAX\nMOV EAX, 0\nINT 22\nINC ECX\nCMP EBX,EAX\nINC ESI\nJNE L1\n\n; Ask for key input \nL2: MOV EAX, 0\nINT 22\nDEC ECX\nCMP ECX, 1\nJNE L2\n\nMOV EAX, 0\nINT 22\nMOV EBX, EAX\n\n; Move input to memory location esi\n; Ask for key input again\nL3: MOV [ESI], EAX\nINC ESI\nMOV EAX, 0\nINT 22\nCMP EBX, EAX\nJNE L3\n';
	}
	else if (flavor === 'att'){
		codeString += '; Asking for key input\nINT $22\nMOV %EAX, %EBX\nMOV $0, %ECX\nMOV $0, %ESI\n\n; Move input to memory location esi\n; Ask for key input again\nL1: MOV %EAX, (%ESI)\nMOV $0, %EAX\nINT $22\nINC %ECX\nCMP %EAX, %EBX\nINC %ESI\nJNE L1\n\n; Asking for key input\nL2: MOV $0, %EAX\nINT $22\nDEC %ECX\nCMP $1, %ECX\nJNE L2\n\nMOV $0, %EAX\nINT $22\nMOV %EAX, %EBX\n\n; Move input to memory location esi\n; Ask for key input again\nL3: MOV %EAX, (%ESI)\nINC %ESI\nMOV $0, %EAX\nINT $22\nCMP %EAX, %EBX\nJNE L3\n';
	}
	document.getElementById('id_code').value = codeString;
}
function dataAccess(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare arrays\n.data\n    x DB 1, 2, 3, 4, 5\n    y DW 2, 54, 32, 8\n    z DD 10 DUP (50)\n\n; Storing values into memory using register arithmetic\n.text\n    mov eax, 6\n    mov [eax], [x+2]\n    mov [eax+2], [y+3]\n    mov [ebx], [z]\n    mov [eax-5], [y+2]\n    mov [-5+eax], [y+2]';
	}
	else if (flavor === 'att'){
		codeString += '; Declare arrays\n.data\n    x: .byte 1, 2, 3, 4, 5\n    y: .short 2, 54, 32, 8\n    z: .long 10 DUP (50)\n\n; Storing values into memory using register arithmetic\n.text\n\tmov $6, %eax\n\tmov 2(x), (%eax)\n\tmov 3(y), 2(%eax)\n\tmov (z), (%ebx)\n\tmov 3, %ecx\n\tmov 2(y), -5(%eax, 3)\n\tmov 4(x), (%eax, 2, %ecx)\n\tmov 4(x), 12(%eax, 2, %ecx)\n\tmov 4(x), 12(%eax, 2, %ecx, 4)';
	}
	document.getElementById('id_code').value = codeString;
}
