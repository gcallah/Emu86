"""
interrupts.py: interrupts in program
"""

from assembler.errors import ExitProg, check_num_args
from assembler.tokens import Instruction


class Syscall(Instruction):
    """
        <instr>
             SYSCALL
        </instr>
        <syntax>
            SYSCALL
        </syntax>
        <descr>
            Exits program
        </descr>
    """

    def fhook(self, ops, vm):
        check_num_args("SYSCALL", ops, 0)
        raise ExitProg(self.get_nm())
