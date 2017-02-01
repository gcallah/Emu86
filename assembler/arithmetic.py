"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfs

from errors import *


BITS = 32  # for now we assume 32-bit ints


def one_op_arith(ops, gdata, instr, f):
    if len(ops) != 1:
        raise(InvalidNumArgs(instr))

    ops[0].set_val(f(ops[0].get_val()))

def two_op_arith(ops, gdata, instr, f):
    if len(ops) != 2:
        raise(InvalidNumArgs(instr))
    ops[0].set_val(f(ops[0].get_val(), ops[1].get_val()))

def add(ops, gdata):
    """
    Implments the ADD instruction.
    """
    two_op_arith(ops, gdata, "ADD", opfs.add)
    return ''

def sub(ops, gdata):
    """
    Implments the SUB instruction.
    """
    two_op_arith(ops, gdata, "SUB", opfs.sub)
    return ''

def imul(ops, gdata):
    """
    Implments the IMUL instruction.
    """
    two_op_arith(ops, gdata, "IMUL", opfs.mul)
    return ''

def andf(ops, gdata):
    """
    Implments the AND instruction.
    """
    two_op_arith(ops, gdata, "AND", opfs.and_)
    return ''

def orf(ops, gdata):
    """
    Implments the OR instruction.
    """
    two_op_arith(ops, gdata, "OR", opfs.or_)
    return ''

def xor(ops, gdata):
    """
    Implments the XOR instruction.
    """
    two_op_arith(ops, gdata, "XOR", opfs.xor)
    return ''

def shl(ops, gdata):
    """
    Implments the XOR instruction.
    """
    two_op_arith(ops, gdata, "SHL", opfs.lshift)
    return ''

def shr(ops, gdata):
    """
    Implments the XOR instruction.
    """
    two_op_arith(ops, gdata, "SHR", opfs.rshift)
    return ''

def notf(ops, gdata):
    """
    Implments the NOT instruction.
    """
    one_op_arith(ops, gdata, "NOT", opfs.inv)
    return ''

def inc(ops, gdata):
    """
    Implments the INC instruction.
    """
    (op, code_pos) = get_one_op("INC", ops, gdata)
    op.set_val(op.get_val() + 1)
    return ''

def dec(ops, gdata):
    """
    Implments the DEC instruction.
    """
    (op, code_pos) = get_one_op("DEC", ops, gdata)
    op.set_val(op.get_val() - 1)
    return ''

def neg(ops, gdata):
    """
    Implments the NEG instruction.
    """
    one_op_arith(ops, gdata, "NEG", opfs.neg)
    return ''

def idiv(ops, gdata):
    """
    Implments the IDIV instruction.
    """
    if len(ops) != 1:
        raise(InvalidNumArgs(instr))

    hireg = int(gdata.registers['EDX']) << 32
    lowreg = int(gdata.registers['EAX'])
    dividend = hireg + lowreg
    gdata.registers['EAX'] = dividend // ops[0].get_val()
    gdata.registers['EBX'] = dividend % ops[0].get_val()
    return ''
