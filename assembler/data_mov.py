"""
data_mov.py: data movement instructions.
"""

from .errors import check_num_args
from .tokens import Instruction


class Mov(Instruction):
    def __init__(self, name):
        super().__init__(name)

    def f(self, ops, gdata):
        check_num_args(self.name, ops, 2)
        ops[0].set_val(ops[1].get_val())
        return ''


def pop(ops, gdata):
    check_num_args("POP", ops, 1)
    # TBD!
    return ''


def push(ops, gdata):
    check_num_args("PUSH", ops, 1)
    # TBD!
    return ''


def lea(ops, gdata):
    check_num_args("LEA", ops, 2)
    # TBD!
    return ''
