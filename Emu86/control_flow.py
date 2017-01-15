"""
control_flow.py: control flow instructions.

Contains:
    JMP
"""

from .parse import get_one_op


def jmp(code, registers, memory, code_pos):
    """
    Implments the MOV instruction.
    """
    (label, code_pos) = get_one_op("JMP", code, registers, memory, code_pos)

    return ('', code_pos)
