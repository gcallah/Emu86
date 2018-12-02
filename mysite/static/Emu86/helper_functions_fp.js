function fp_area_fp(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare length and width\n.data\n\tlong: .float 12.2\n\twide: .float 12.5\n\n; Calc area of rect\n.text\n\t0x40000 LWC F8, 0(F28)\n    0x40004 LWC F10, 4(F28)\n    0x40008 MULT.S F12, F8, F10';
	}
	document.getElementById('id_code').value = code_string;
}
function fp_data_fp(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; First comes the data section, where we declare some names.\n.data\n    x: .float 8.0\n    y: .float 10.5\n    z: .double 20.555\n\n; Next is the .text section, where we use them:\n.text\n    0x400000 LWC F8, 0(F28)\n    0x400004 LWC F10, 4(F28)\n    0x400008 LDC F12, 8(F28)\n';
	}
	document.getElementById('id_code').value = code_string;
}
function fp_power_fp(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; x is the base, y is the power\n.data\n    x: .float 5.5\n    y: .word 0x3\n\n; In F8, we put the number to raise to the power we put in R9.\n.text\n      0x400000 LWC F8, 0(F28)\n      0x400004 LW R9, 4(R28)\n      0x400008 JAL 0x1000040\n      0x40000C SYSCALL\n\npower: 0x400010 ADD.S F16, F0, F8\nloop: 0x400014 MULT.S F8, F8, F16\n      0x400018 ADDI R9, R9, -1\n      0x40001C ADDI R10, R0, 1\n      0x400020 BNE R9, R10, -4\n      0x400024 JR R31';
	}
	document.getElementById('id_code').value = code_string;
}
function keyInterrupt_fp(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Asking for key input\nINT 22\nMOV EBX, EAX\nMOV ECX, 0\nMOV ESI, 0\n\n; Move input to memory location esi\n; Ask for key input again\nL1: MOV [ESI], EAX\nMOV EAX, 0\nINT 22\nINC ECX\nCMP EBX,EAX\nINC ESI\nJNE L1\n\n; Ask for key input \nL2: MOV EAX, 0\nINT 22\nDEC ECX\nCMP ECX, 1\nJNE L2\n\nMOV EAX, 0\nINT 22\nMOV EBX, EAX\n\n; Move input to memory location esi\n; Ask for key input again\nL3: MOV [ESI], EAX\nINC ESI\nMOV EAX, 0\nINT 22\nCMP EBX, EAX\nJNE L3\n';
	}
	else if (flavor == 'mips_asm'){
		code_string += '; Asking for key input\nINT $22\nMOV %EAX, %EBX\nMOV $0, %ECX\nMOV $0, %ESI\n\n; Move input to memory location esi\n; Ask for key input again\nL1: MOV %EAX, (%ESI)\nMOV $0, %EAX\nINT $22\nINC %ECX\nCMP %EAX, %EBX\nINC %ESI\nJNE L1\n\n; Asking for key input\nL2: MOV $0, %EAX\nINT $22\nDEC %ECX\nCMP $1, %ECX\nJNE L2\n\nMOV $0, %EAX\nINT $22\nMOV %EAX, %EBX\n\n; Move input to memory location esi\n; Ask for key input again\nL3: MOV %EAX, (%ESI)\nINC %ESI\nMOV $0, %EAX\nINT $22\nCMP %EAX, %EBX\nJNE L3\n';
	}
	document.getElementById('id_code').value = code_string;
}
function dataAccess_fp(flavor) {
	code_string = '';
	if (flavor == 'intel'){
		code_string += '; Declare arrays\n.data\n    x DB 1, 2, 3, 4, 5\n    y DW 2, 54, 32, 8\n    z DD 10 DUP (50)\n\n; Storing values into memory using register arithmetic\n.text\n    mov eax, 6\n    mov [eax], [x+2]\n    mov [eax+2], [y+3]\n    mov [ebx], [z]\n    mov [eax-5], [y+2]\n    mov [-5+eax], [y+2]';
	}
	else if (flavor == 'mips_asm'){
		code_string += '; Declare arrays\n.data\n    x: .byte 1, 2, 3, 4, 5\n    y: .short 2, 54, 32, 8\n    z: .long 10 DUP (50)\n\n; Storing values into memory using register arithmetic\n.text\n\tmov $6, %eax\n\tmov 2(x), (%eax)\n\tmov 3(y), 2(%eax)\n\tmov (z), (%ebx)\n\tmov 3, %ecx\n\tmov 2(y), -5(%eax, 3)\n\tmov 4(x), (%eax, 2, %ecx)\n\tmov 4(x), 12(%eax, 2, %ecx)\n\tmov 4(x), 12(%eax, 2, %ecx, 4)';
	}
	document.getElementById('id_code').value = code_string;
}
