from .arithmetic import Add, Sub, Addi, Subi, Mult, Div
from .arithmetic import Andf, Andi, Orf, Ori, Xor, Nor, Sll, Srl
from .arithmetic import Mflo, Mfhi
from .data_mov import Load, Store
from .control_flow import Slt, Slti, Beq, Bne
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
	'SUBI': Subi('SUBI'),
	'MULT': Mult('MULT'),
	'DIV': Div('DIV'),
	'MFLO': Mflo('MFLO'),
	'MFHI': Mfhi('MFHI'),
	'AND': Andf('AND'),
	'ANDI': Andi('ANDI'),
	'OR': Orf('OR'),
	'ORI': Ori('ORI'),
	'XOR': Xor('XOR'),
	'NOR': Nor('NOR'),
	'SLL': Sll('SLL'),
	'SRL': Srl('SRL'),

	#control 
	'SLT': Slt('SLT'),
	'SLTI': Slti('SLTI'),
	'BEQ': Beq('BEQ'),
	'BNE': Bne('BNE')
}
