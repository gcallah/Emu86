"""
parse.py: creates parse tree.
"""

import re

from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName
from .tokens import Location, Address, Register, IntOp, Symbol, Instruction
from .tokens import RegAddress
from .arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .arithmetic import Shr, Notf, Andf, Orf, Xor, Neg
from .control_flow import Cmpf, Je, Jne, Jmp, FlowBreak, Call, Ret
from .control_flow import Jg, Jge, Jl, Jle
from .data_mov import Mov, Pop, Push, Lea
from .interrupts import Interrupt


LABEL_RE = "^([A-Za-z_][A-Za-z0-9_]*):"
label_match = re.compile(LABEL_RE)
SYM_RE = "([A-Za-z_][A-Za-z0-9_]*)"
sym_match = re.compile(SYM_RE)

DELIMITERS = set([' ', ',', '\n', '\r', '\t',])

je = Je('JE')
jne = Jne('JNE')
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
        'JG': Jg('JG'),
        'JGE': Jge('JGE'),
        'JL': Jl('JL'),
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


def add_debug(s, vm):
    vm.debug += (s + "\n")


def get_token(code, code_pos):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    token = ''
    if code_pos <= len(code):
        count = 0
        for char in code[code_pos:]:  # eat leading delimiters
            if char in DELIMITERS:
                count += 1
            else:
                break
        code_pos += count

        if code_pos <= len(code):
            count = 0
            for char in code[code_pos:]:
                count += 1
                if char not in DELIMITERS:
                    token = token + char
                else:
                    break
            code_pos += count
    return (token, code_pos)


def get_op(token, vm, symbols):
    """
    Args:
        token: string to evaluate
        vm: our virtual machine
        symbols: the symbol table
    Returns:
        The object representing this operand.
    """

    global sym_match
    int_val = 0

    if not token:
        return None
    elif token.upper() in vm.registers:  # reg can be e.g. EAX or eax
        return Register(token.upper(), vm.registers)
    elif token[0] == '[' and token[len(token) - 1] == ']':
        address = token[1:len(token) - 1]
        if address in vm.memory:
            return Address(address, vm.memory)
        elif address.upper() in vm.registers:
            return RegAddress(address.upper(), vm.registers, vm.memory)
        else:
            raise InvalidMemLoc(address)
    elif re.search(sym_match, token) is not None:
        return Symbol(token)
    else:
        try:
            int_val = int(token)
        except Exception:
            raise InvalidOperand(token)
        return IntOp(int_val)

def get_instr(code, code_pos):
    """
    Get an instruction from the code text.
    Args:
        code: the code!
        code_pos: where we are in reading the code.
    Returns:
        a tuple of the instruction found and the new code_pos.
        (Throws an exception if the token is not an instruction.)
    """
    (token, code_pos) = get_token(code, code_pos)
    uptok = token.upper()  # allow instructions in upper or lower
    if uptok in instructions:
        instr = instructions[uptok]
    else:
        raise InvalidInstruction(token)
    return (instr, code_pos)

def get_ops(code, code_pos, vm, symbols):
    """
    Collect our operands.
    """
    ops = []
    while code_pos < len(code):
        (token, code_pos) = get_token(code, code_pos)
        op = get_op(token, vm, symbols)
        ops.append(op)

    return (ops, code_pos)

def lex(code, vm):
    """
    Lexical phase: tokenizes the code.
    Args:
        code: The code to lexically analyze.

    Returns:
        tok_lines: the tokenized version
    """
    global label_match
    code_pos = 0
    symbols = {}
    lines = code.split("\n")
    tok_lines = []  # this will hold the tokenized version of the code
    i = 0
    for line in lines:
        code_pos = 0   # reset each line!

        # comments:
        comm_start = line.find(";")
        if comm_start > 0:  # -1 means not found
            line = line[0:comm_start]
        elif comm_start == 0:  # the whole line is a comment
            continue

        # strip AFTER comments to handle blanks between code and ;
        line = line.strip()
        if len(line) == 0:  # blank lines ok; just skip 'em
            continue

        # labels:
        label_present = re.search(label_match, line)
        if label_present is not None:
            label = label_present.group(1)
            vm.labels[label] = i
            # now strip off the label:
            line = line.split(":", 1)[-1]
        # we've stripped extra whitespace, comments, and labels: now store
        # line:
        lines[i] = line
        # now tokenize!
        this_line = []
        (instr, code_pos) = get_instr(line, code_pos)
        this_line.append(instr)
        (ops, code_pos) = get_ops(line, code_pos, vm, symbols)
        this_line.append(ops)
        tok_lines.append(this_line)
        i += 1
    return (tok_lines)
