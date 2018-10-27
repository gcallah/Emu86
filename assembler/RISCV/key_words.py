from .arithmetic import Add, Addi, Sub, Mul, And, Andi 
from .arithmetic import Xor, Xori, Or, Ori, Srl, Sll
from .arithmetic import Srli, Slli, Slt, Sltu, Slti, Sltiu
from .arithmetic import Sra, Srai
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
    'ADD': Add('ADD'),
	'ADDI': Addi('ADDI'),
	'SUB': Sub('SUB'),
	'MUL': Mul('MUL'),
	'AND': And('AND'),
	'ANDI': Andi('ANDI'),
	'OR': Or('OR'),
	'ORI': Ori('ORI'),
	'XOR': Xor('XOR'),
	'XORI': Xori('XORI'), 
	'SRL': Srl('SRL'),
	'SLL': Sll('SLL'),
	'SLLI': Slli('SLLI'),
	'SRLI': Srli('SRLI'),
	'SLT': Slt('SLT'),
	'SLTU': Sltu('SLTU'),
	'SLTI': Slti('SLTI'),
	'SLTIU': Sltiu('SLTIU'),
	'SRA': Sra('SRA'),
	'SRAI': Srai('SRAI')






	# control 

	# interrupts

}

op_func_codes = {
	# R-format
	'ADD': '0110011',
	'SUB': '0110011',
	'MUL': '0110011',
	'AND': '0110011',
	'OR': '0110011',
	'XOR': '0110011',
	'SRL': '0110011',
	'SLL': '0110111',
	'SLT': '0110011',
	'SLTU': '0110011',

    # I-format
	'LW': '0000011',
	'ADDI': '0010011',
	'ANDI': '0010011',
	'ORI': '0010011',
	'XORI': '0010011',
	'SRLI': '0010011',
	'SLLI': '0010011',
	'SLTI': '0010011',
	'SLTIU': '0010011',

	# S-Format
	'SW': '0100011'

	#J-format

}
