"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfs

from .parse import get_one_op, get_two_ops


BITS = 32  # for now we assume 32-bit ints



def one_op_arith(code, registers, memory, code_pos, instr, f):
    (op, code_pos) = get_one_op(instr, code, registers, memory, code_pos)
    op.set_val(f(op.get_val()))

def two_op_arith(code, registers, memory, code_pos, instr, f):
    (op1, op2, code_pos) = get_two_ops(instr, code, registers, memory, code_pos)
    op1.set_val(f(op1.get_val(), op2.get_val()))

def add(code, registers, memory, code_pos):
    """
    Implments the ADD instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "ADD", opfs.add)
    return ''

def sub(code, registers, memory, code_pos):
    """
    Implments the SUB instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "SUB", opfs.sub)
    return ''

def imul(code, registers, memory, code_pos):
    """
    Implments the IMUL instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "IMUL", opfs.mul)
    return ''

def andf(code, registers, memory, code_pos):
    """
    Implments the AND instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "AND", opfs.and_)
    return ''

def orf(code, registers, memory, code_pos):
    """
    Implments the OR instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "OR", opfs.or_)
    return ''

def xor(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "XOR", opfs.xor)
    return ''

def shl(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "SHL", opfs.lshift)
    return ''

def shr(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    two_op_arith(code, registers, memory, code_pos, "SHR", opfs.rshift)
    return ''

def notf(code, registers, memory, code_pos):
    """
    Implments the NOT instruction.
    """
    one_op_arith(code, registers, memory, code_pos, "NOT", opfs.inv)
    return ''

def inc(code, registers, memory, code_pos):
    """
    Implments the INC instruction.
    """
    (op, code_pos) = get_one_op("INC", code, registers, memory, code_pos)
    op.set_val(op.get_val() + 1)
    return ''

def dec(code, registers, memory, code_pos):
    """
    Implments the DEC instruction.
    """
    (op, code_pos) = get_one_op("DEC", code, registers, memory, code_pos)
    op.set_val(op.get_val() - 1)
    return ''

def neg(code, registers, memory, code_pos):
    """
    Implments the NEG instruction.
    """
    one_op_arith(code, registers, memory, code_pos, "NEG", opfs.neg)
    return ''

def idiv(code, registers, memory, code_pos):
    """
    Implments the IDIV instruction.
    """
    (op, code_pos) = get_one_op("IDIV", code, registers, memory, code_pos)
    hireg = int(registers['EAX']) << 32
    lowreg = int(registers['EBX'])
    dividend = hireg + lowreg
    registers['EAX'] = dividend // op.get_val()
    registers['EBX'] = dividend % op.get_val()
    return ''
