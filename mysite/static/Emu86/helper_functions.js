function celFah(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp DW 35\n    fTemp DW ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov eax, [cTemp]\n    imul eax, 9\n    add eax, 2\n    mov ebx, 5\n    idiv ebx \n    add eax, 32\n    mov [fTemp], eax';
	}
	else if (flavor == 'att'){
		code_string += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp: .short 35\n    fTemp: .short ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov (cTemp), %eax\n    imul $9, %eax\n    add $2, %eax\n    mov $5, %ebx\n    idiv %ebx \n    add $32, %eax\n    mov %eax, (fTemp)';
	}
	else{
		code_string += '; Declare a Celsius temperature\n\n.data\n    cTemp: .word 23\n    fTemp: .word 0\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    LW R8, cTemp(R28)\n    ADDI R9, R0, 9\n    MULT R8, R9\n    MFLO R8\n    ADDI R8, R8, 2\n    ADDI R9, R0, 5\n    DIV R8, R9\n    MFLO R8\n    ADDI R8, R8, 20\n    SW R8, fTemp(R28)';
	}
	document.getElementById('id_code').value = code_string;
}
function avg(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare an array and declare size of the array\n.data\n    nbrArray DW 25, 47, -15, -50, 32, 95 DUP (10)\n    nbrElts DW 100\n\n; Calculate the average of the array:\n.text\n    mov eax, 0\n    mov ebx, 0\n    mov edx, 0\n    mov ecx, [nbrElts]\nforCount1: cmp ebx, ecx\n           je endCount\nbody: add eax, [ebx]\n      inc ebx\n      jmp forCount1\nendCount: idiv ecx \n\n\n';
	}
	else if (flavor == 'att'){
		code_string += '; Declare an array and declare size of the array\n.data\n    nbrArray: .short 25, 47, -15, -50, 32, 95 DUP (10)\n    nbrElts: .short 100\n\n; Calculate the average of the array:\n.text\n    mov 0, %eax\n    mov 0, %ebx\n    mov 0, %edx\n    mov (nbrElts), %ecx\nforCount1: cmp %ebx, %ecx\n           je endCount\nbody: add (%ebx), %eax\n      inc %ebx\n      jmp forCount1\nendCount: idiv %ecx \n\n\n';
	}
	else{
		code_string += '; Declare an array and declare size of the array\n.data\n    nbrArray: .word 19, 2F, -0xF, -32, 20, 0A, 0A, 0A, 0A, 0A\n    nbrElts: .word 0A\n\n; Calculate the average of the array:\n.text\n    ADD R8, R0, R0\n    ADD R9, R0, R0\n    LW R16, nbrElts(R28)\n    ADDI R10, R28, nbrArray \nFORCOUNT: BEQ R9, R16, 5\nBODY: LW R11, (R10)\n      ADD R8, R8, R11\n      ADDI R9, R9, 1\n      ADDI R10, R10, 1\n      J FORCOUNT\nENDCOUNT: DIV R8, R16\nMFLO R12\nMFHI R13\n';
	}
	document.getElementById('id_code').value = code_string;
}
function loop(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '      mov eax, 16\n      mov ebx, 0\n\n; Compare eax and ebx and loop until equal\nloop: cmp eax, ebx\n      jz done\n      inc ebx\n      dec edx\n      jnz loop\n\ndone: mov ecx, ebx  ; when done, store ebx in ecx\n';
	}
	else if (flavor == 'att'){
		code_string += '      mov $16, %eax\n      mov $0, %ebx\n\n; Compare eax and ebx and loop until equal\nloop: cmp %eax, %ebx\n      jz done\n      inc %ebx\n      dec %edx\n      jnz loop\n\ndone: mov %ebx, %ecx  ; when done, store ebx in ecx\n';
	}
	else{
		code_string += '; Compare R8 and R9 and loop until equal\n; When done, store R9 to R11\n    ADDI R8, R0, 10\n    ADD R9, R0, R0\n    ADDI R9, R9, 1\n    ADDI R10, R10, -1\n    BNE R8, R9, -3\n    ADD R11, R11, R9';
	}
	document.getElementById('id_code').value = code_string;
}
function sqrt(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare a number\n.data\n    number DW 100\n\n; Calculate square root of the number\n.text\n    mov eax, [number]\n    push ebx\n    push ecx\n    mov ebx, 0\nWhileLE: mov ecx, ebx\n         imul ecx, ebx\n         cmp ecx, eax\n         jnle EndWhileLE\n         inc ebx\n         jmp WhileLE\nEndWhileLE: dec ebx\n            mov eax, ebx\n            pop ecx\n            pop ebx';
	}
	else if (flavor == 'att'){
		code_string += '; Declare a number\n.data\n    number: .short 100\n\n; Calculate square root of the number\n.text\n    mov (number), %eax\n    push %ebx\n    push %ecx\n    mov $0, %ebx\nWhileLE: mov %ebx, %ecx\n         imul %ebx, %ecx\n         cmp %eax, %ecx\n         jnle EndWhileLE\n         inc %ebx\n         jmp WhileLE\nEndWhileLE: dec %ebx\n            mov %ebx, %eax\n            pop %ecx\n            pop %ebx';
	}
	else{
		code_string += '; Declare a number\n.data\n    number: .word 64\n\n; Calculate square root of the number\n.text\n    LW R8, number(R28)\n\nWHILELE: ADD R10, R0, R9\n         MULT R10, R9\n         MFLO R10\n         SUB R11, R10, R8\n         SLT R12, R0, R11\n         BNE R12, R0, 2\n         ADDI R9, R9, 1\n         J WHILELE\nENDWHILELE: SUBI R9, R9, 1\n            ADD R8, R0, R9\n            ';
	}
	document.getElementById('id_code').value = code_string;
}
function area(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare length and width\n.data\n    long DW 35\n    wide DW 27\n\n; Calculate area of rectangle\n.text\n    mov eax, [long]\n    imul eax, [wide]';
	}
	else if (flavor == 'att'){
		code_string += '; Declare length and width\n.data\n    long: .short 35\n    wide: .short 27\n\n; Calculate area of rectangle\n.text\n    mov (long), %eax\n    imul (wide), %eax';
	}
	else{
		code_string += '; Declare length and width\n.data\n    long: .word 23\n    wide: .word 1B\n\n; Calculate area of rectangle\n.text\n    LW R8, long(R28)\n    LW R9, wide(R28)\n    MULT R8, R9\n    MFLO R10';
	}
	document.getElementById('id_code').value = code_string;
}
function arithExpr(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare x, y, and z variables \n.data\n    x DW 35\n    y DW 47\n    z DW 26\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    mov eax, [x]\t\t\n    add eax, [y]\t\n    mov ebx, [z]\n    add ebx, ebx\n    sub eax, ebx\n    inc eax \n    neg eax';
	}
	else if (flavor == 'att'){
		code_string += '; Declare x, y, and z variables \n.data\n    x: .short 35\n    y: .short 47\n    z: .short 26\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    mov (x), %eax\t\t\n    add (y), %eax\t\n    mov (z), %ebx\n    add %ebx, %ebx\n    sub %ebx, %eax\n    inc %eax \n    neg %eax';
	}
	else{
		code_string += '; Declare x, y, and z variables \n.data\n    x: .word 23\n    y: .word 2F\n    z: .word 1A\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    LW R8, x(R28)\n    LW R9, y(R28)\n    ADD R8, R8, R9\n    LW R10, z(R28)\n    ADD R10, R10, R10\n    SUB R8, R8, R10\n    ADDI R8, R8, 1\n    SUB R8, R0, R8';
	}
	document.getElementById('id_code').value = code_string;
}
function modify(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray DW 25, 47, 15, 50, 32, 95 DUP (10)\n    nbrElts DW 100\n    nbrMin DW 33\n\n; Change any numbers less than min to min:\n.text\n    mov eax, 0\n    mov ebx, 0\n    mov edx, 0\n    mov ecx, [nbrElts]\nforCount1: cmp ebx, ecx\n           je endCount\nbody: cmp [ebx], [nbrMin]\n      jge endIfSmall\n      mov [ebx], [nbrMin]\nendIfSmall: add eax, [ebx]\n            inc ebx\n            jmp forCount1\nendCount: mov edx, eax\n\n\n';
	}
	else if (flavor == 'att'){
		code_string += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .short 25, 47, 15, 50, 32, 95 DUP (10)\n    nbrElts: .short 100\n    nbrMin: .short 33\n\n; Change any numbers less than min to min:\n.text\n    mov 0, %eax\n    mov 0, %ebx\n    mov 0, %edx\n    mov (nbrElts), %ecx\nforCount1: cmp %ecx, %ebx\n           je endCount\nbody: cmp (nbrMin), (%ebx)\n      jge endIfSmall\n      mov (nbrMin), (%ebx)\nendIfSmall: add (%ebx), %eax\n            inc %ebx\n            jmp forCount1\nendCount: mov %eax, %edx\n\n\n';
	}
	else{
		code_string += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .word 19, 2F, 0F, 32, 20, 0A, 0A, 0A, 0A, 0A\n    nbrElts: .word 0A\n    nbrMin: .word 21\n\n; Change any numbers less than min to min:\n.text\n    ADD R8, R0, R0\n    ADD R9, R0, R0\n    ADDI R10, R0, nbrArray\n    LW R16, nbrMin(R28)\n    LW R17, nbrElts(R28)\nFORCOUNT: BEQ R9, R17, 8\nBODY: LW R11, (R9)\n      SLT R12, R16, R11\n      BNE R12, R0, 1\n      SW R16, (R9)\nENDIFSMALL: LW R11, (R9)\n            ADD R8, R8, R11\n            ADDI R9, R9, 1\n            J FORCOUNT\nENDCOUNT: ADD R13, R0, R8';
	}
	document.getElementById('id_code').value = code_string;
}
function log(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare a number\n.data\n    number DW 759\n\n; Calculating log (base 2) of a number\n.text\n    mov ecx, 0\n    mov eax, 1\nwhileLE: cmp eax, [number]\n         jnle endWhileLE\nbody: add eax, eax\n      inc ecx\n      jmp whileLE\n\nendWhileLE: dec ecx ';
	}
	else if (flavor == 'att'){
		code_string += '; Declare a number\n.data\n    number: .short 759\n\n; Calculating log (base 2) of a number\n.text\n    mov $0, %ecx\n    mov $1, %eax\nwhileLE: cmp (number), %eax\n         jnle endWhileLE\nbody: add %eax, %eax\n      inc %ecx\n      jmp whileLE\n\nendWhileLE: dec %ecx ';
	}
	else{
		code_string += '; Declare a number\n.data\n    number: .word 2F7\n\n; Calculating log (base 2) of a number\n.text\n    ADD R8, R8, R0\n    ADDI R9, R9, 1\n    LW R10, number(R28)\n\nWHILELE: SUB R11, R9, R10\n         SLT R12, R0, R11\n         BNE R12, R0, 3\nBODY: ADD R9, R9, R9\n      ADDI R8, R8, 1\n      J WHILELE\n\nENDWHILELE: ADDI R8, R8, -1';
	}
	document.getElementById('id_code').value = code_string;
}
function addTwo(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare number and sum.\n.data\n    number DW -105\n    sum DW ?\n\n; Store first number to EAX\n; Add 158 to value in EAX\n; Store total to sum\n.text\n    mov eax, [number]\t\t\n    add eax, 158\t\n    mov [sum], eax';
	}
	else if (flavor == 'att'){
		code_string += '; Declare number and sum.\n.data\n    number: .short -105\n    sum: .short ?\n\n; Store first number to EAX\n; Add 158 to value in EAX\n; Store total to sum\n.text\n    mov (number), %eax\t\t\n    add $158, %eax\t\n    mov %eax, (sum)';
	}
	else{
		code_string += '; Declare number and sum.\n.data\n    number: .word -69\n    sum: .word 0\n\n; Store first number to R8\n; Add 158 to value in R8\n; Store total to sum\n.text\n    LW R8, number(R28)\t\t\n    ADDI R8, R8, 9E\t\n    SW R8, sum(R28)';
	}
	document.getElementById('id_code').value = code_string;
}
