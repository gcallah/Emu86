"""
data_mov.py: data movement instructions.
"""

from .errors import check_num_args
from .tokens import Instruction


class Mov(Instruction):
    """
        INSTRUCTION: mov
        SYNTAX:
            MOV reg, reg
            MOV reg, con
            MOV reg, mem
            MOV mem, reg
            MOV mem, mem
    """
    def f(self, ops, gdata):
        check_num_args(self.get_nm(), ops, 2)
        ops[0].set_val(ops[1].get_val())
        return ''


class Pop(Instruction):
    """
        INSTRUCTION: pop
        SYNTAX:
    """
    def f(self, ops, gdata):
        check_num_args("POP", ops, 1)
        # TBD!
        return ''


class Push(Instruction):
    """
        INSTRUCTION: push
        SYNTAX:
    """
    def f(self, ops, gdata):
        check_num_args("PUSH", ops, 1)
        # TBD!
        return ''


class Lea(Instruction):
    """
        INSTRUCTION: lea
        SYNTAX:
    """
    def f(self, ops, gdata):
        check_num_args("LEA", ops, 2)
        # TBD!
        return ''
