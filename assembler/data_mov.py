"""
data_mov.py: data movement instructions.
"""

from .errors import check_num_args
from .tokens import Instruction


class Mov(Instruction):
    def f(self, ops, gdata):
        check_num_args(self.get_nm(), ops, 2)
        ops[0].set_val(ops[1].get_val())
        return ''


def Pop(ops, gdata):
    check_num_args("POP", ops, 1)
    # TBD!
    return ''


def Push(ops, gdata):
    check_num_args("PUSH", ops, 1)
    # TBD!
    return ''


def Lea(ops, gdata):
    check_num_args("LEA", ops, 2)
    # TBD!
    return ''
