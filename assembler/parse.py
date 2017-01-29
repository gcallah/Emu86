"""
parse.py: creates parse tree.
"""

import re

from errors import *  # import * OK here:
                       # these are *our* errors, after all!
from tokens import Location, Address, Register, IntOp, Symbol


SYMBOL_RE = "^([A-Za-z]+)"
sym_match = re.compile(SYMBOL_RE)

DELIMITERS = set([' ', ',', '\n', '\r', '\t',])


def get_one_op(instr, code, gdata, code_pos):
    """
    For instructions that expect one integer operand.
    """
    (tok, code_pos) = get_token(code, code_pos)
    op = get_op(tok, gdata)

    if not op:
        raise InvalidNumArgs(instr, 1)

    return (op, code_pos)

def get_two_ops(instr, code, gdata, code_pos):
    """
    For instructions that expect two integer operands.
    """
    (tok1, code_pos) = get_token(code, code_pos)
    (tok2, code_pos) = get_token(code, code_pos)
    op1 = get_op(tok1, gdata)
    op2 = get_op(tok2, gdata)

    if not op1 or not op2:
        raise InvalidNumArgs(instr, 2)
    if not isinstance(op1, Location):
        raise InvalidOperand(op1)

    return (op1, op2, code_pos)

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

    token = token.upper()  # for now, a simple-minded way to allow input in
                           # either case!
    return (token, code_pos)

def get_op(token, gdata):
    """
    Returns int value of operand: direct int or reg val
    Args:
        op: operand to evaluate
    Returns:
        int value
    """

    int_val = 0

    if not token:
        return None
    elif token in gdata.registers:
        return Register(token, gdata.registers)
    elif token[0] == '[' and token[len(token) - 1] == ']':
        address = token[1:len(token) - 1]
        if address in gdata.memory:
            return Address(token[1:len(token) - 1], gdata.memory)
        else:
            raise InvalidAddress(address)
    elif token.isalpha():
        return Symbol(token)
    else:
        try:
            int_val = int(token)
        except Exception:
            raise InvalidOperand(token)
        return IntOp(int_val)
