"""
arithmetic.py: arithmetic and logic instructions.
"""

from .parse import get_one_op, get_two_ops


BITS = 32  # for now we assume 32-bit ints


def add(code, registers, memory, code_pos):
    """
    Implments the ADD instruction.
    """
    (op1, op2, code_pos) = get_two_ops("ADD", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() + op2.get_val())
    return ''

def sub(code, registers, memory, code_pos):
    """
    Implments the SUB instruction.
    """
    (op1, op2, code_pos) = get_two_ops("ADD", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() - op2.get_val())
    return ''

def imul(code, registers, memory, code_pos):
    """
    Implments the IMUL instruction.
    """
    (op1, op2, code_pos) = get_two_ops("IMUL", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() * op2.get_val())
    return ''

def andf(code, registers, memory, code_pos):
    """
    Implments the AND instruction.
    """
    (op1, op2, code_pos) = get_two_ops("AND", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() & op2.get_val())
    return ''

def orf(code, registers, memory, code_pos):
    """
    Implments the OR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("OR", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() | op2.get_val())
    return ''

def xor(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("OR", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() ^ op2.get_val())
    return ''

def shl(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("SHL", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() << op2.get_val())
    return ''

def shr(code, registers, memory, code_pos):
    """
    Implments the XOR instruction.
    """
    (op1, op2, code_pos) = get_two_ops("SHR", code, registers, memory, code_pos)
    op1.set_val(op1.get_val() >> op2.get_val())
    return ''

def notf(code, registers, memory, code_pos):
    """
    Implments the NOT instruction.
    """
    (op, code_pos) = get_one_op("NOT", code, registers, memory, code_pos)
    op.set_val(~(op.get_val()))
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
    (op, code_pos) = get_one_op("NEG", code, registers, memory, code_pos)
    val = op.get_val()
    if (val & (1 << (BITS - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << BITS)        # compute negative value
    op.set_val(val)
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
