"""
assemble.py
Executes assembly code typed in.
"""

from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .arithmetic import add, sub, imult, idiv, inc, dec, shl, 
from .arithmetic import shr, notf, andf, orf, xor
from .parse import get_token, get_op, get_one_op, get_two_ops


debug = ""


def add_debug(s):
    global debug
    debug += (s + "\n")

def move(code, registers, memory, code_pos):
    """
    Implments the MOV instruction.
    """
    (op1, op2, code_pos) = get_two_ops("MOV", code, registers, memory, code_pos)
    op1.set_val(op2.get_val())
    return ('', code_pos)

instructions = {
        # data movement:
        'MOV': move,
        # arithmetic and logic:
        'ADD': add,
        'IMUL': imul,
        'IDIV': idiv,
        'SUB': sub,
        'AND': andf,
        'OR': orf,
        'XOR': xor,
        'SHL': shl,
        'SHR': shr,
        'NOT': notf,
        'INC': inc,
        'DEC': dec,
        }


def assemble(code, registers, memory):
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            registers: current register values.
        Returns:
            Output, if any.
            Error, if any.
    """
    global debug
    debug = ''

    code_pos = 0
    output = ''
    error = ''
    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    while code_pos < len(code):
        try:
            (outp, code_pos) = get_instruction(code, registers, memory, code_pos)
            output += outp
        except Error as err:
            return (output, err.msg, debug)
    return (output, '', debug)

def get_instruction(code, registers, memory, code_pos):
    """
    We expect an instruction next.
        Args:
            code
        Returns:
            None
    """
    (instr, code_pos) = get_token(code, code_pos)
    if instr == '':
        return ''
    elif instr not in instructions:
        raise InvalidInstruction(instr)
    else:
        add_debug("Calling " + instr)
        return instructions[instr](code, registers, memory, code_pos)

