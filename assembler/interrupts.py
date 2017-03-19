"""
interrupts.py: data movement instructions.
"""

from .errors import check_num_args, InvalidOperand
from .tokens import Instruction, IntOp

nxt_key = 0
ret_str = "Good work in assembly!"

def read_key(gdata):
    # we are faking 'reading' from the keyboard
    global ret_str
    global nxt_key
    c = ret_str[nxt_key]
    nxt_key = (nxt_key + 1) % len(ret_str)
    gdata.registers['EAX'] = ord(c)
    return ""


int_vectors = {
    22: {0: read_key }
}


class Interrupt(Instruction):
    """
        INSTRUCTION: int
        SYNTAX:
            INT con, con
    """

    def f(self, ops, gdata):
        check_num_args(self.get_nm(), ops, 2)
        if type(ops[0]) != IntOp:
            raise InvalidOperand(ops[0])
        if type(ops[1]) != IntOp:
            raise InvalidOperand(ops[1])
        interrupt_class = int_vectors[ops[0].get_val()]
        interrupt_handler = interrupt_class[ops[1].get_val()]
        c = interrupt_handler(gdata)
        return str(c)
