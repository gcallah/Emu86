"""
assemble.py
Executes assembly code typed in.
"""

from .errors import *  # OK here: there are *our* errors, after all!


def move(code):
    op1 = get_token(code)
    op2 = get_token(code)
    return 'MOV' + op1 + ", " + op2

def add(code):
    return 'ADD'

def sub(code):
    return 'SUB'


instructions = {
        'ADD': add,
        'MOV': move,
        'SUB': sub,
        }

delimiters = set([' ', ',' '\n', '\t'])

registers = None

code_pos = 0


def assemble(code, regs):  # memory to come!
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            registers: current register values.
        Returns:
            Output, if any.
            Error, if any.
    """
    global code_pos
    code_pos = 0
    global registers
    registers = regs

    output = ''
    error = ''
    while code_pos < len(code):
        try:
            output = get_instruction(code)
            return (output, '')
        except Error as err:
            return (output, err.msg)

def get_instruction(code):
    """
    We expect an instruction next.
        Args:
            code
        Returns:
            None
    """
    token = get_token(code)
    if token not in instructions:
        raise InvalidInstruction(token)
    else:
        return instructions[token](code)

def get_operand(code):
    token = get_token(code)
    if token not in registers:
        pass

def get_token(code):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    global code_pos

    count = 0
    for char in code[code_pos:]:  # eat leading delimiters
        if char in delimiters:
            count += 1
    code_pos += count

    token = ''
    for char in code[code_pos:]:
        if char not in delimiters:
            token = token + char
        else:
            break
    code_pos += len(token) + 1  # because we read 1 delim char
    return token
