"""
interrupts.py: data movement instructions.
"""

from .parse import get_two_ops

int_vectors = {
    22: [],
}


def interrupt(code, gdata, code_pos):
    """
    Implments the INT instruction.
    """
    (op1, op2, code_pos) = get_two_ops("INT", code, gdata, code_pos)
    return ''
