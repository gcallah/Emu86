"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

"""

from .errors import check_num_args
from .tokens import Instruction


class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Uknown control flow exception."

def get_one_op(instr, ops):
    check_num_args(instr, ops, 1)
    return ops[0]

def get_two_ops(instr, ops):
    check_num_args(instr, ops, 2)
    return (ops[0], ops[1])

class Jump(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


class Jmp(Instruction):
    """
    This is an unconditional jump.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Cmpf(Instruction):
    """
    Implments the CMP instruction.
    Compares op1 and op2, and sets (right now) the SF and ZF flags.
    It is not clear at this moment how to treat the OF and CF flags in Python,
    since Python integer arithmetic never carries or overflows!
    """
    def f(self, ops, gdata):
        (op1, op2) = get_two_ops(self.get_nm(), ops)
        res = op1.get_val() - op2.get_val()
        # set the proper flags
        # zero flag:
        if res == 0:
            gdata.flags['ZF'] = 1
        else:
            gdata.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            gdata.flags['SF'] = 1
        else:
            gdata.flags['SF'] = 0
        return ''

class Je(Instruction):
    """
    Jumps if op1 == op2.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if gdata.flags['ZF']:
            raise Jump(target.name)
        return ''

class Jne(Instruction):
    """
    Jumps if op1 != op2.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if not gdata.flags['ZF']:
            raise Jump(target.name)
        return ''

class Jg(Instruction):
    """
    Jumps if op1 > op2.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if not gdata.flags['SF'] and not gdata.flags['ZF']:
            raise Jump(target.name)
        return ''

class Jge(Instruction):
    """
    Jumps if op1 >= op2.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if not gdata.flags['SF']:
            raise Jump(target.name)
        return ''

class Jl(Instruction):
    """
    Jumps if op1 > op2.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if gdata.flags['SF']:
            raise Jump(target.name)
        return ''

class Jle(Instruction):
    """
    Jumps if op1 >= op2.
    """
    def f(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if gdata.flags['SF'] or gdata.flags['ZF']:
            raise Jump(target.name)
        return ''

