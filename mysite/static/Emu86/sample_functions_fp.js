function area_fp(flavor) {
	code_string = '';
	code_string += '; Declare length and width\n.data\n\tlong: .float 12.2\n\twide: .float 12.5\n\n; Calc area of rect\n.text\n\t0x40000 LWC F8, 0(F28)\n    0x40004 LWC F10, 4(F28)\n    0x40008 MULT.S F12, F8, F10';
	
	document.getElementById('id_code').value = code_string;
}
function data_fp(flavor) {
	code_string = '';
	code_string += '; First comes the data section, where we declare some names.\n.data\n    x: .float 8.0\n    y: .float 10.5\n    z: .double 20.555\n\n; Next is the .text section, where we use them:\n.text\n    0x400000 LWC F8, 0(F28)\n    0x400004 LWC F10, 4(F28)\n    0x400008 LDC F12, 8(F28)\n';
	
	document.getElementById('id_code').value = code_string;
}
function power_fp(flavor) {
	code_string = '';
	code_string += '; x is the base, y is the power\n.data\n    x: .float 5.5\n    y: .word 0x3\n\n; In F8, we put the number to raise to the power we put in R9.\n.text\n      0x400000 LWC F8, 0(F28)\n      0x400004 LW R9, 4(R28)\n      0x400008 JAL 0x1000040\n      0x40000C SYSCALL\n\npower: 0x400010 ADD.S F16, F0, F8\nloop: 0x400014 MULT.S F8, F8, F16\n      0x400018 ADDI R9, R9, -1\n      0x40001C ADDI R10, R0, 1\n      0x400020 BNE R9, R10, -4\n      0x400024 JR R31';
	
	document.getElementById('id_code').value = code_string;
}
