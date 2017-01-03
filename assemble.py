"""
assemble.py
Executes assembly code typed in.
"""

from .errors import *  # OK here: there are *our* errors, after all!


def move(code):
    return 'MOV'

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


def assemble(code, registers):  # memory to come!
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            registers: current register values.
        Returns:
            Output, if any.
            Error, if any.
    """
    output = ''
    error = ''
#    while len(code) > 0:
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

def get_token(code):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    token = ''
    for char in code:
        if char not in delimiters:
            token = token + char
        else:
            break
    return token
