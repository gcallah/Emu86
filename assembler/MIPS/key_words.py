from .arithmetic import Add, Sub, Addi, Mult, Div
from .arithmetic import Andf, Andi, Orf, Ori, Xor, Nor, Sll, Srl
from .arithmetic import Mflo, Mfhi
from .data_mov import Load, Store
from .control_flow import Slt, Slti, Beq, Bne, Jmp, Jal, Jr
from .interrupts import Syscall
from assembler.tokens import DataType
from .fp_arithmetic import Adds, Subs, Mults, Divs
from .fp_arithmetic import Addd, Subd, Multd, Divd
from .fp_data_mov import Loadc, Storec, LoadDouble, StoreDouble

key_words = {
    # data types
    '.BYTE': DataType('DB'),
    '.WORD': DataType('DW'),
    '.FLOAT': DataType('FL'),
    '.DOUBLE': DataType('DBL'),

    # data movement:
    'LW': Load('LW'),
    'SW': Store('SW'),

    # arithmetic and logic
    'ADD': Add('ADD'),
    'ADDI': Addi('ADDI'),
    'SUB': Sub('SUB'),
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


    # control
    'SLT': Slt('SLT'),
    'SLTI': Slti('SLTI'),
    'BEQ': Beq('BEQ'),
    'BNE': Bne('BNE'),
    'J': Jmp('J'),
    'JAL': Jal('JAL'),
    'JR': Jr('JR'),

    # interrupts
    'SYSCALL': Syscall('SYSCALL'),

    # floating point
    'ADD.S': Adds('ADD.S'),
    'SUB.S': Subs('SUB.S'),
    'MULT.S': Mults('MULT.S'),
    'DIV.S': Divs('DIV.S'),

    'ADD.D': Addd("ADD.D"),
    'SUB.D': Subd('SUB.D'),
    'MULT.D': Multd('MULT.D'),
    'DIV.D': Divd('DIV.D'),

    # floating point data mov
    'LWC': Loadc('LWC'),
    'SWC': Storec('SWC'),
    'LDC': LoadDouble('LDC'),
    'SDC': StoreDouble('SDC')
}

op_func_codes = {
    # R-format
    'ADD': ('000000', '100000'),
    'SUB': ('000000', '100010'),
    'MULT': ('000000', '011000'),
    'DIV': ('000000', '011010'),
    'MFLO': ('000000', '010010'),
    'MFHI': ('000000', '010000'),
    'AND': ('000000', '100100'),
    'OR': ('000000', '100101'),
    'XOR': ('000000', '100110'),
    'NOR': ('000000', '100111'),
    'SLL': ('000000', '000000'),
    'SRL': ('000000', '000010'),
    'SLT': ('000000', '101010'),
    'JR': ('000000', '001000'),
    # I-format
    'LW': '100011',
    'SW': '101011',
    'ADDI': '001000',
    'ANDI': '001100',
    'ORI': '001101',
    'SLTI': '001010',
    'BEQ': '000100',
    'BNE': '000101',
    'SYSCALL': '001100',

    # J-format
    'J': '000010',
    'JAL': '000011',

    # FR
    'ADD.S': ('010001'),
    'SUB.S': ('010001', "000001"),
    'MULT.S': ('010001', '000010'),
    'DIV.S': ('010001', '000010'),
    'LWC': ('110001'),
    'SWC': ('111001'),
    'LDC': ('110101'),
    'SDC': ('111101'),

    'ADD.D': ('010001'),
    'SUB.D': ('010001'),
    'MULT.D': ('010001'),
    'DIV.D': ('010001'),
}
