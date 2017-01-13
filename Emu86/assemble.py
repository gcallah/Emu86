"""
assemble.py
Executes assembly code typed in.
"""

from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .arithmetic import add, sub, imul, idiv, inc, dec, shl
from .arithmetic import shr, notf, andf, orf, xor, neg
from .data_mov import mov
from .parse import get_token, get_op, get_one_op, get_two_ops
from .tokens import Instruction


debug = ""


def add_debug(s):
    global debug
    debug += (s + "\n")

instructions = {
        # data movement:
        'MOV': mov,
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
        'NEG': neg,
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
    (token, code_pos) = get_token(code, code_pos)
    if token == '':
        return ''
    else:
        instr = Instruction(token, instructions)
        add_debug("Calling " + token)
        return instr.exec(code, registers, memory, code_pos)

