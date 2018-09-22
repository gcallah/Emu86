from .data_mov import Load, Store
from assembler.tokens import DataType

key_words = {
	# data types
	'.BYTE': DataType('DB'),
    '.WORD': DataType('DW'),

    # data movement:
	'LW': Load('LW'),
	'SW': Store('SW'),

	# arithmetic and logic

	# control 

	# interrupts

}

op_func_codes = {
	# R-format

    # I-format
	'LW': '0000011',

	# S-Format
	'SW': '0100011',

	#J-format

}
