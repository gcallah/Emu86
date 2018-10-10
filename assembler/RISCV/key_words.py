from .data_mov import Load, Store
from .arithmetic import Add, Addi, Sub, Mul, And
from assembler.tokens import DataType

key_words = {
	# data types
	'.BYTE': DataType('DB'),
    '.WORD': DataType('DW'),

    # data movement:
	'LW': Load('LW'),
	'SW': Store('SW'),

	# arithmetic and logic
    'ADD': Add('ADD'),
	'ADDI': Addi('ADDI'),
	'SUB': Sub('SUB'),
	'AND': And('AND'),
	'MUL': Mul('MUL')
	# control 

	# interrupts

}

op_func_codes = {
	# R-format
	'ADD': '0110011',
	'SUB': '0110011',
	'MUL': '0110011',
	'AND': '0110011',
    # I-format
	'LW': '0000011',
	'ADDI': '0010011',
	# S-Format
	'SW': '0100011'

	#J-format

}
