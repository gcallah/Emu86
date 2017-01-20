"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfs

from .parse import get_one_op, get_two_ops


BITS = 32  # for now we assume 32-bit ints



def one_op_arith(code, gdata, code_pos, instr, f):
    (op, code_pos) = get_one_op(instr, code, gdata, code_pos)
    op.set_val(f(op.get_val()))

def two_op_arith(code, gdata, code_pos, instr, f):
    (op1, op2, code_pos) = get_two_ops(instr, code, gdata, code_pos)
    op1.set_val(f(op1.get_val(), op2.get_val()))

def add(code, gdata, code_pos):
    """
    Implments the ADD instruction.
    """
    two_op_arith(code, gdata, code_pos, "ADD", opfs.add)
    return ''

def sub(code, gdata, code_pos):
    """
    Implments the SUB instruction.
    """
    two_op_arith(code, gdata, code_pos, "SUB", opfs.sub)
    return ''

def imul(code, gdata, code_pos):
    """
    Implments the IMUL instruction.
    """
    two_op_arith(code, gdata, code_pos, "IMUL", opfs.mul)
    return ''

def andf(code, gdata, code_pos):
    """
    Implments the AND instruction.
    """
    two_op_arith(code, gdata, code_pos, "AND", opfs.and_)
    return ''

def orf(code, gdata, code_pos):
    """
    Implments the OR instruction.
    """
    two_op_arith(code, gdata, code_pos, "OR", opfs.or_)
    return ''

def xor(code, gdata, code_pos):
    """
    Implments the XOR instruction.
    """
    two_op_arith(code, gdata, code_pos, "XOR", opfs.xor)
    return ''

def shl(code, gdata, code_pos):
    """
    Implments the XOR instruction.
    """
    two_op_arith(code, gdata, code_pos, "SHL", opfs.lshift)
    return ''

def shr(code, gdata, code_pos):
    """
    Implments the XOR instruction.
    """
    two_op_arith(code, gdata, code_pos, "SHR", opfs.rshift)
    return ''

def notf(code, gdata, code_pos):
    """
    Implments the NOT instruction.
    """
    one_op_arith(code, gdata, code_pos, "NOT", opfs.inv)
    return ''

def inc(code, gdata, code_pos):
    """
    Implments the INC instruction.
    """
    (op, code_pos) = get_one_op("INC", code, gdata, code_pos)
    op.set_val(op.get_val() + 1)
    return ''

def dec(code, gdata, code_pos):
    """
    Implments the DEC instruction.
    """
    (op, code_pos) = get_one_op("DEC", code, gdata, code_pos)
    op.set_val(op.get_val() - 1)
    return ''

def neg(code, gdata, code_pos):
    """
    Implments the NEG instruction.
    """
    one_op_arith(code, gdata, code_pos, "NEG", opfs.neg)
    return ''

def idiv(code, gdata, code_pos):
    """
    Implments the IDIV instruction.
    """
    (op, code_pos) = get_one_op("IDIV", code, gdata, code_pos)
    hireg = int(gdata.registers['EAX']) << 32
    lowreg = int(gdata.registers['EBX'])
    dividend = hireg + lowreg
    gdata.registers['EAX'] = dividend // op.get_val()
    gdata.registers['EBX'] = dividend % op.get_val()
    return ''
