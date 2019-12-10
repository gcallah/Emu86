from .arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .arithmetic import Shr, Notf, Andf, Orf, Xor, Neg, BTR, BTS, BSF, BSR
from .arithmetic import BT, BTC
from .fp_arithmetic import FAdd, FSub, FDiv, FMul
from .fp_arithmetic import FAbs, FChs, FaddP, FSubP, FMulP, FDivP, FSqrt
from .control_flow import Cmpf, Je, Jne, Jmp, Call, Ret
from .control_flow import Jg, Jge, Jl, Jle


from .data_mov import Mov, Pop, Push, Lea, Fld, Fst
from .data_mov_att import Movb, Movw, Movl
from .interrupts import Interrupt
from assembler.tokens import DataType, ConstantSign, DupTok

je = Je('JE')
jne = Jne('JNE')
jg = Jg('JG')
jl = Jl('JL')

instructions = {
        # interrupts:
        'INT': Interrupt('INT'),
        # control flow:
        'CMP': Cmpf('CMP'),
        'JMP': Jmp('JMP'),
        je.get_nm(): je,
        jne.get_nm(): jne,
        # the next two instructions are just synonyms for the previous two.
        'JZ': je,
        'JNZ': jne,
        jg.get_nm(): jg,
        jl.get_nm(): jl,
        # JNLE synonymous to JG, JNGE synonymous to JL
        'JNLE': jg,
        'JNGE': jl,
        'JGE': Jge('JGE'),
        'JLE': Jle('JLE'),
        'CALL': Call('CALL'),
        'RET': Ret('RET'),
        # data movement:
        'MOV': Mov('MOV'),
        'PUSH': Push('PUSH'),
        'POP': Pop('POP'),
        'LEA': Lea('LEA'),
        'FLD': Fld('FLD'),
        'FST': Fst('FST'),
        # arithmetic and logic:
        'ADD': Add('ADD'),
        'SUB': Sub('SUB'),
        'IMUL': Imul('IMUL'),
        'IDIV': Idiv('IDIV'),
        'AND': Andf('AND'),
        'OR': Orf('OR'),
        'XOR': Xor('XOR'),
        'SHL': Shl('SHL'),
        'SHR': Shr('SHR'),
        'NOT': Notf('NOT'),
        'INC': Inc('INC'),
        'DEC': Dec('DEC'),
        'NEG': Neg('NEG'),
        'BTR': BTR('BTR'),
        'BTS': BTS('BTS'),
        'BSF': BSF('BSF'),
        'BSR': BSR('BSR'),
        'BT': BT('BT'),
        'BTC': BTC('BTC'),
        # floating point
        'FADD': FAdd('FADD'),
        'FSUB': FSub('FSUB'),
        'FDIV': FDiv('FDIV'),
        'FMUL': FMul('FMUL'),
        'FABS': FAbs('FABS'),
        'FCHS': FChs('FCHS'),
        'FADDP': FaddP('FADDP'),
        'FSUBP': FSubP('FSUBP'),
        'FMULP': FMulP('FMULP'),
        'FDIVP': FDivP('FDIVP'),
        'FSQRT': FSqrt('FSQRT')

        # Other
        }

intel_key_words = {
        # data-types
        'DB': DataType('DB'),
        'DW': DataType('DW'),
        'DD': DataType('DD'),
        # floating point
        "REAL4": DataType('REAL4'),
        "REAL8": DataType('REAL8'),
        "REAL16": DataType('REAL16'),
        "COMPLEX": DataType('COMPLEX'),
        "DUP": DupTok()
}

att_key_words = {
        # other mov instructions
        'MOVB': Movb('MOVB'),
        'MOVW': Movw('MOVW'),
        'MOVL': Movl('MOVL'),

        # data-types
        '.BYTE': DataType('DB'),
        '.SHORT': DataType('DW'),
        '.LONG': DataType('DD'),
        '.FLOAT': DataType('FL'),
        '.DOUBLE': DataType('DBL'),

        # other tokens
        '$': ConstantSign(),
        "DUP": DupTok()
}
