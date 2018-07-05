from .Intel.arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .Intel.arithmetic import Shr, Notf, Andf, Orf, Xor, Neg
from .MIPS.arithmetic import Add_MIPS, Sub_MIPS, Addi, Subi, Andf_MIPS
from .MIPS.arithmetic import Andi, Orf_MIPS, Ori
from .Intel.control_flow import Cmpf, Je, Jne, Jmp, FlowBreak, Call, Ret
from .Intel.control_flow import Jg, Jge, Jl, Jle
from .Intel.data_mov import Mov, Pop, Push, Lea
from .MIPS.data_mov import Load, Store
from .interrupts import Interrupt

je = Je('JE')
jne = Jne('JNE')
jg = Jg ('JG')
jl = Jl ('JL')
intel_instructions = {
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
        'RET' : Ret('RET'),
        # data movement:
        'MOV': Mov('MOV'),
        'PUSH': Push('PUSH'),
        'POP': Pop('POP'),
        'LEA': Lea('LEA'),
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
        }

INTEL_SEPARATORS = set([',', '(', ')', '[', ']', '+', '-'])

ATT_SEPARATORS = set([',', '(', ')', '[', ']', '+', '-', '$'])

mips_instructions = {
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

MIPS_SEPARATORS = set([',', '(', ')', '[', ']', '+', '-'])