function sqrt(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare a number\n.data\n    number DW 100\n\n; Calculate square root of the number\n.text\n    mov eax, [number]\n    push ebx\n    push ecx\n    mov ebx, 0\nWhileLE: mov ecx, ebx\n         imul ecx, ebx\n         cmp ecx, eax\n         jnle EndWhileLE\n         inc ebx\n         jmp WhileLE\nEndWhileLE: dec ebx\n            mov eax, ebx\n            pop ecx\n            pop ebx';
	}
	else if (flavor == 'att'){
		code_string += '; Declare a number\n.data\n    number: .short 100\n\n; Calculate square root of the number\n.text\n    mov (number), %eax\n    push %ebx\n    push %ecx\n    mov $0, %ebx\nWhileLE: mov %ebx, %ecx\n         imul %ebx, %ecx\n         cmp %eax, %ecx\n         jnle EndWhileLE\n         inc %ebx\n         jmp WhileLE\nEndWhileLE: dec %ebx\n            mov %ebx, %eax\n            pop %ecx\n            pop %ebx';
	}
	else{
		code_string += '; Declare a number\n.data\n    number: .word 64\n\n; Calculate square root of the number\n.text\n    40000 LW R8, number(R28)\n\nWHILELE: 40004 ADD R10, R0, R9\n         40008 MULT R10, R9\n         4000C MFLO R10\n         40010 SUB R11, R10, R8\n         40014 SLT R12, R0, R11\n         40018 BNE R12, R0, 2\n         4001C ADDI R9, R9, 1\n         40020 J WHILELE\nENDWHILELE: 40024 ADDI R9, R9, -1\n            40028 ADD R8, R0, R9\n            ';
	}
	document.getElementById('id_code').value = code_string;
}
function power(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; In edx, we put the number to raise to the power we put in ebx.\n      mov edx, 2\n      mov ebx, 16\n      call power\n      mov eax, 0\n      int 32\n\npower: mov ecx, edx\nloop: imul edx, ecx\n      dec ebx\n      cmp ebx, 1\n      jne loop\n      ret\n';
	}
	else if (flavor == 'att'){
		code_string += '; In edx, we put the number to raise to the power we put in ebx.\n      mov $2, %edx\n      mov $16, %ebx\n      call power\n      mov $0, %eax\n      int $32\n\npower: mov %edx, %ecx\nloop: imul %ecx, %edx\n      dec %ebx\n      cmp %ebx, $1\n      jne loop\n      ret\n';
	}
	else{
		code_string += '; In R8, we put the number to raise to the power we put in R9.\n      400000 ADDI R8, R0, 2\n      400004 ADDI R9, R9, 10\n      400008 JAL 1000040\n      40000C SYSCALL\n\npower: 400010 ADD R16, R0, R8\nloop: 400014 MULT R8, R16\n      400018 MFLO R8\n      40001C ADDI R9, R9, -1\n      400020 ADDI R10, R0, 1\n      400024 BNE R9, R10, -5\n      400028 JR R31';
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
		code_string += '; Declare an array and declare size of the array\n.data\n    nbrArray: .word 19, 2F, -0F, -32, 20, 0A, 0A, 0A, 0A, 0A\n    nbrElts: .word 0A\n\n; Calculate the average of the array:\n.text\n    40000 ADD R8, R0, R0\n    40004 ADD R9, R0, R0\n    40008 LW R16, nbrElts(R28)\n    4000C ADDI R10, R28, nbrArray \nFORCOUNT: 40010 BEQ R9, R16, 5\nBODY: 40014 LW R11, (R10)\n      40018 ADD R8, R8, R11\n      4001C ADDI R9, R9, 1\n      40020 ADDI R10, R10, 4\n      40024 J 100040\nENDCOUNT: 40028 DIV R8, R16\n4002C MFLO R12\n40030 MFHI R13\n';
	}
	document.getElementById('id_code').value = code_string;
}
function celFah(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp DW 35\n    fTemp DW ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov eax, [cTemp]\n    imul eax, 9\n    add eax, 2\n    mov ebx, 5\n    idiv ebx \n    add eax, 32\n    mov [fTemp], eax';
	}
	else if (flavor == 'att'){
		code_string += '; Declare a Celsius temperature\n; Uninitialized fTemp \n.data\n    cTemp: .short 35\n    fTemp: .short ?\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    mov (cTemp), %eax\n    imul $9, %eax\n    add $2, %eax\n    mov $5, %ebx\n    idiv %ebx \n    add $32, %eax\n    mov %eax, (fTemp)';
	}
	else{
		code_string += '; Declare a Celsius temperature\n\n.data\n    cTemp: .word 23\n    fTemp: .word 0\n\n; Convert from Celsius to Fahrenheit\n; Store result in fTemp\n.text\n    40000 LW R8, cTemp(R28)\n    40004 ADDI R9, R0, 9\n    40008 MULT R8, R9\n    4000C MFLO R8\n    40010 ADDI R8, R8, 2\n    40014 ADDI R9, R0, 5\n    40018 DIV R8, R9\n    4001C MFLO R8\n    40020 ADDI R8, R8, 20\n    40024 SW R8, fTemp(R28)';
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
		code_string += '; Compare R8 and R9 and loop until equal\n; When done, store R9 to R11\n    40000 ADDI R8, R0, 10\n    40004 ADD R9, R0, R0\n    40008 ADDI R9, R9, 1\n    4000C ADDI R10, R10, -1\n    40010 BNE R8, R9, -3\n    40014 ADD R11, R11, R9';
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
		code_string += '; Declare x, y, and z variables \n.data\n    x: .word 23\n    y: .word 2F\n    z: .word 1A\n\n; Calculate -(x + y - 2 * z + 1)\n.text\n    40000 LW R8, x(R28)\n    40004 LW R9, y(R28)\n    40008 ADD R8, R8, R9\n    4000C LW R10, z(R28)\n    40010 ADD R10, R10, R10\n    40014 SUB R8, R8, R10\n    40018 ADDI R8, R8, 1\n    4001C SUB R8, R0, R8';
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
		code_string += '; Declare length and width\n.data\n    long: .word 23\n    wide: .word 1B\n\n; Calculate area of rectangle\n.text\n    40000 LW R8, long(R28)\n    40004 LW R9, wide(R28)\n    40008 MULT R8, R9\n    4000C MFLO R10';
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
		code_string += '; Declare a number\n.data\n    number: .word 2F7\n\n; Calculating log (base 2) of a number\n.text\n    40000 ADD R8, R8, R0\n    40004 ADDI R9, R9, 1\n    40008 LW R10, number(R28)\n\nWHILELE: 4000C SUB R11, R9, R10\n         40010 SLT R12, R0, R11\n         40014 BNE R12, R0, 3\nBODY: 40018 ADD R9, R9, R9\n      4001C ADDI R8, R8, 1\n      40020 J WHILELE\n\nENDWHILELE: 40024 ADDI R8, R8, -1';
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
		code_string += '; Declare number and sum.\n.data\n    number: .word -69\n    sum: .word 0\n\n; Store first number to R8\n; Add 158 to value in R8\n; Store total to sum\n.text\n    40000 LW R8, number(R28)\t\t\n    40004 ADDI R8, R8, 9E\t\n    40008 SW R8, sum(R28)';
	}
	document.getElementById('id_code').value = code_string;
}
function data(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; First comes the data section, where we declare some names.\n.data\n    x DB 8\n    y DW 16\n    z DD 32\n\n; Next is the .text section, where we use them:\n.text\n    mov eax, [x]\n    mov ebx, [y]\n    mov ecx, [z]\n';
	}
	else if (flavor == 'att'){
		code_string += '; First comes the data section, where we declare some names.\n.data\n    x: .byte 8\n    y: .short 16\n    z: .long 32\n\n; Next is the .text section, where we use them:\n.text\n    mov (x), %eax\n    mov (y), %ebx\n    mov (z), %ecx\n';
	}
	else{
		code_string += '; First comes the data section, where we declare some names.\n.data\n    x: .word 8\n    y: .word 10\n    z: .word 20\n\n; Next is the .text section, where we use them:\n.text\n    400000 LW R8, x(R28)\n    400004 LW R9, y(R28)\n    400008 LW R10, z(R28)';
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
		code_string += '; Declare an array and declare size of the array\n; Declare the minimum of the array\n.data\n    nbrArray: .word 19, 2F, 0F, 32, 20, 0A, 0A, 0A, 0A, 0A\n    nbrElts: .word 0A\n    nbrMin: .word 21\n\n; Change any numbers less than min to min:\n.text\n    40000 ADD R8, R0, R0\n    40004 ADD R9, R0, R0\n    40008 ADD R10, R0, R0\n    4000C ADDI R11, R0, nbrArray\n    40010 LW R16, nbrMin(R28)\n    40014 LW R17, nbrElts(R28)\nFORCOUNT: 40018 BEQ R10, R17, 9\nBODY: 4001C LW R12, (R9)\n      40020 SLT R13, R16, R12\n      40024 BNE R13, R0, 1\n      40028 SW R16, (R9)\nENDIFSMALL: 4002C LW R11, (R9)\n            40030 ADD R8, R8, R11\n            40034 ADDI R9, R9, 4\n            40038 ADDI R10, R10, 1\n            4003C J 100060\nENDCOUNT: 40040 ADD R13, R0, R8';
	}
	document.getElementById('id_code').value = code_string;
}
function arithShift(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += 'mov [4], 1\nmov eax, 4\nmov ebx, 2\nmov ecx, 8\nmov edx, 16\nadd ebx, ecx\nsub edx, ecx\nimul eax, [4]\nshl [4], 2\n';
	}
	else if (flavor == 'att'){
		code_string += 'mov $1, (4)\nmov $4, %eax\nmov $2, %ebx\nmov $8, %ecx\nmov $16, %edx\nadd %ecx, %ebx\nsub %ecx, %edx\nimul (4), %eax\nshl $2, (4)\n';
	}
	document.getElementById('id_code').value = code_string;
}
function keyInterrupt(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += 'INT 22\nMOV EBX, EAX\nMOV ECX, 0\nMOV ESI, 0\n\nL1: MOV [ESI], EAX\nMOV EAX, 0\nINT 22\nINC ECX\nCMP EBX,EAX\nINC ESI\nJNE L1\n\nL2: MOV EAX, 0\nINT 22\nDEC ECX\nCMP ECX, 1\nJNE L2\n\nMOV EAX, 0\nINT 22\nMOV EBX, EAX\n\nL3: MOV [ESI], EAX\nINC ESI\nMOV EAX, 0\nINT 22\nCMP EBX, EAX\nJNE L3\n';
	}
	else if (flavor == 'att'){
		code_string += 'INT $22\nMOV %EAX, %EBX\nMOV $0, %ECX\nMOV $0, %ESI\n\nL1: MOV %EAX, (%ESI)\nMOV $0, %EAX\nINT $22\nINC %ECX\nCMP %EAX, %EBX\nINC %ESI\nJNE L1\n\nL2: MOV $0, %EAX\nINT $22\nDEC %ECX\nCMP $1, %ECX\nJNE L2\n\nMOV $0, %EAX\nINT $22\nMOV %EAX, %EBX\n\nL3: MOV %EAX, (%ESI)\nINC %ESI\nMOV $0, %EAX\nINT $22\nCMP %EAX, %EBX\nJNE L3\n';
	}
	document.getElementById('id_code').value = code_string;
}
function array(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x DB 3, 8, 5, 2\n    y DW 13 DUP (-50)\n    z DD 'hello', 0\n\n; Store array values\n.text\n    mov eax, [x] \n    mov ebx, [y+4]\n    mov ecx, [z+3]\n    mov edx, [x+2]";
	}
	else if (flavor == 'att'){
		code_string += "; Declare arrays x, y, z\n; y is an array of size 13, holding element 50\n; z is an array of the ASCII values of 'hello', ends in 0 \n.data\n    x: .byte 3, 8, 5, 2\n    y: .short 13 DUP (-50)\n    z: .long 'hello', 0\n\n; Store array values\n.text\n    mov (x), %eax \n    mov 4(y), %ebx\n    mov 3(z), %ecx\n    mov 2(x), %edx";
	}
	document.getElementById('id_code').value = code_string;
}
