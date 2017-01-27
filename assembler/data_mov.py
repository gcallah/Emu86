"""
data_mov.py: data movement instructions.
"""

from .parse import get_two_ops


def mov(code, gdata, code_pos):
    """
    Implments the MOV instruction.
    """
    (op1, op2, code_pos) = get_two_ops("MOV", code, gdata, code_pos)
    op1.set_val(op2.get_val())
    return ''
