from .arithmetic import Add_MIPS, Sub_MIPS, Addi, Subi, Andf_MIPS
from .arithmetic import Andi, Orf_MIPS, Ori
from .data_mov import Load, Store

instructions = {
    # data movement:
	'LOAD': Load('LOAD'),
	'STORE': Store('STORE'),

	# arithmetic and logic
	'ADD': Add_MIPS('ADD'),
	'ADDI': Addi('ADDI'),
	'SUB': Sub_MIPS('SUB'),
	'SUBI': Subi('SUBI'),
	'AND': Andf_MIPS('AND'),
	'ANDI': Andi('ANDI'),
	'OR': Orf_MIPS('OR'),
	'ORI': Ori('ORI'),
}
