"""
data_mov.py: data movement instructions.
"""

from .errors import check_num_args


def mov(ops, gdata):
    """
    Implments the MOV instruction.
    """
    check_num_args(instr, ops, 2)
    ops[0].set_val(ops[1].get_val())
    return ''
