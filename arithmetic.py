"""
arithmetic.py: arithmetic and logic instructions.
"""

from .parse import get_two_ops


def add(code, registers, memory, code_pos):
    """
    Implments the ADD instruction.
    """
    (op1, op2, code_pos) = get_two_ops("ADD", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() + op2.get_val())
    return ('', code_pos)

def sub(code, registers, memory, code_pos):
    """
    Implments the SUB instruction.
    """
    (op1, op2, code_pos) = get_two_ops("ADD", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() - op2.get_val())
    return ('', code_pos)

def imul(code, registers, memory, code_pos):
    """
    Implments the IMUL instruction.
    """
    (op1, op2, code_pos) = get_two_ops("IMUL", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() * op2.get_val())
    return ('', code_pos)

def andf(code, registers, memory, code_pos):
    """
    Implments the AND instruction.
    """
    (op1, op2, code_pos) = get_two_ops("AND", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() & op2.get_val())
    return ('', code_pos)

def orf(code, registers, memory, code_pos):
    """
    Implments the OR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("OR", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() | op2.get_val())
    return ('', code_pos)

def xor(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("OR", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() ^ op2.get_val())
    return ('', code_pos)

def shl(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("SHL", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() << op2.get_val())
    return ('', code_pos)

def shr(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("SHR", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() >> op2.get_val())
    return ('', code_pos)

def notf(code, registers, memory, code_pos):
    """
    Implments the NOT instruction.
    """
    (op, code_pos) = get_one_op("NOT", code, registers, memory, code_pos)
    op.set_val(~(op.get_val()))
    return ('', code_pos)

def inc(code, registers, memory, code_pos):
    """
    Implments the INC instruction.
    """
    (op, code_pos) = get_one_op("INC", code, registers, memory, code_pos)
    op.set_val(op.get_val() + 1)
    return ('', code_pos)

def dec(code, registers, memory, code_pos):
    """
    Implments the DEC instruction.
    """
    (op, code_pos) = get_one_op("DEC", code, registers, memory, code_pos)
    op.set_val(op.get_val() - 1)
    return ('', code_pos)

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
    return ('', code_pos)
