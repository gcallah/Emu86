from .arithmetic import Add, Sub, Addi, Subi, Andf
from .arithmetic import Andi, Orf, Ori, Nor, Sll, Srl
from .data_mov import Load, Store
from .control_flow import Slt, Slti
from assembler.tokens import DataType

key_words = {
	# data types
	'.BYTE': DataType('DB'),
    '.SHORT': DataType('DW'),
    '.LONG': DataType('DD'),

    # data movement:
	'LOAD': Load('LOAD'),
	'STORE': Store('STORE'),

	# arithmetic and logic
	'ADD': Add('ADD'),
	'ADDI': Addi('ADDI'),
	'SUB': Sub('SUB'),
	'SUBI': Subi('SUBI'),
	'AND': Andf('AND'),
	'ANDI': Andi('ANDI'),
	'OR': Orf('OR'),
	'ORI': Ori('ORI'),
	'NOR': Nor('NOR'),
	'SLL': Sll('SLL'),
	'SRL': Srl('SRL'),

	#control 
	'SLT': Slt('SLT'),
	'SLTI': Slti('SLTI')
}
