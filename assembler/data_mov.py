"""
data_mov.py: data movement instructions.
"""

from .errors import check_num_args
from .tokens import Instruction


class Mov(Instruction):
    """
        <instr>
             mov
        </instr>
        <syntax>
            MOV reg, reg
            MOV reg, con
            MOV reg, mem
            MOV mem, reg
            MOV mem, mem
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args(self.get_nm(), ops, 2)
        ops[0].set_val(ops[1].get_val())


class Pop(Instruction):
    """
        <instr>
             pop
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args("POP", ops, 1)
        # TBD!


class Push(Instruction):
    """
        <instr>
             push
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args("PUSH", ops, 1)
        # TBD!


class Lea(Instruction):
    """
        <instr>
             lea
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args("LEA", ops, 2)
        # TBD!
