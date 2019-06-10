function area_fp(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare length and width\n.data\n    long DW 0x40600000\n    wide DW 0x1B\n\n; Calculate area of rectangle\n.text\n    FLD F7, [long]\n    FMUL F6, [wide]\n';
	}
	else if (flavor === 'mips_asm'){
	codeString += '; Declare length and width\n.data\n\tlong: .float 12.2\n\twide: .float 12.5\n\n; Calc area of rect\n.text\n\t0x40000 LWC F8, 0(F28)\n    0x40004 LWC F10, 4(F28)\n    0x40008 MULT.S F12, F8, F10';
	}
	document.getElementById('id_code').value = codeString;
}
function data_fp(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare arrays\n.data\n    x DB 0x3f99999a, 0x2, 0x40600000, 0x4, 0x5\n    y DW 0x2, 0x36, 0x3fb33333, 0x8\n    z DD 0xA DUP (0x32)\n\n; Storing values into memory using register arithmetic\n.text\n    FLD F7, 0x6\n    FLD [F7], [x+0x2]\n    FLD [F7+0x2], [y+0x3]\n    FLD [F6], [z]\n    FLD [F7-0x5], [y+0x2]\n    FLD [-0x5+F7], [y+0x2]';
	}
	else if (flavor === 'mips_asm'){
	codeString += '; First comes the data section, where we declare some names.\n.data\n    x: .float 8.0\n    y: .float 10.5\n    z: .double 20.555\n\n; Next is the .text section, where we use them:\n.text\n    0x400000 LWC F8, 0(F28)\n    0x400004 LWC F10, 4(F28)\n    0x400008 LDC F12, 8(F28)\n';
	}
	document.getElementById('id_code').value = codeString;
}
function power_fp(flavor) {
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; In F7, we put the number to raise to the power we put in F5.\n      mov F7, 0x40600000\n      mov F5, 0x3fb33333\n      call power\n      mov F4, 0x0\n      int 0x20\n\npower: mov F6, F7\nloop: imul F7, F6\n      dec F5\n      cmp F5, 0x1\n      jne loop\n      ret\n';
	}
	else if (flavor === 'mips_asm'){
	codeString += '; x is the base, y is the power\n.data\n    x: .float 5.5\n    y: .word 0x3\n\n; In F8, we put the number to raise to the power we put in R9.\n.text\n      0x400000 LWC F8, 0(F28)\n      0x400004 LW R9, 4(R28)\n      0x400008 JAL 0x1000040\n      0x40000C SYSCALL\n\npower: 0x400010 ADD.S F16, F0, F8\nloop: 0x400014 MULT.S F8, F8, F16\n      0x400018 ADDI R9, R9, -1\n      0x40001C ADDI R10, R0, 1\n      0x400020 BNE R9, R10, -4\n      0x400024 JR R31';
	}
	document.getElementById('id_code').value = codeString;
}

function addTwo_fp(flavor)
{
	let codeString = '';
	if (flavor === 'intel'){
		codeString += '; Declare number and sum.\n.data\n    long DW 0x40600000\n    sum DW ?\n\n; Store first number to R7\n; Add 0x40000 to value in R7\n; Store total to sum\n.text\n    mov R7, [number]\n    add R7, 0x9E\n    mov [sum], R7\n';
	}
	document.getElementById('id_code').value = codeString;
}
