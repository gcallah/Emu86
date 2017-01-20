"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

Contains:
    JMP

    FlowBreak
    Jmp
"""

from .parse import get_one_op, get_two_ops


class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Uknown control flow exception."


class Jmp(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


def jmp(code, gdata, code_pos):
    """
    Implments the JMP instruction.
    This is an unconditional jump.
    """
    (target, code_pos) = get_one_op("JMP", code, gdata, code_pos)
    raise Jmp(target.name)

def cmp(code, gdata, code_pos):
    """
    Implments the CMP instruction.
    Compares op1 and op2, and sets (right now) the SF and ZF flags.
    It is not clear at this moment how to treat the OF and CF flags in Python,
    since Python integer arithmetic never carries or overflows!
    """
    (op1, op2, code_pos) = get_two_ops("CMP", code, gdata, code_pos)
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

def je(code, gdata, code_pos):
    """
    Implments the JE instruction.
    Jumps if op1 == op2.
    """
    (target, code_pos) = get_one_op("JE", code, gdata, code_pos)
    if gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

def jne(code, gdata, code_pos):
    """
    Implments the JNE instruction.
    Jumps if op1 != op2.
    """
    (target, code_pos) = get_one_op("JNE", code, gdata, code_pos)
    if not gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

def jg(code, gdata, code_pos):
    """
    Implments the JG instruction.
    Jumps if op1 > op2.
    """
    (target, code_pos) = get_one_op("JG", code, gdata, code_pos)
    if not gdata.flags['SF'] and not gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

def jge(code, gdata, code_pos):
    """
    Implments the JGE instruction.
    Jumps if op1 >= op2.
    """
    (target, code_pos) = get_one_op("JGE", code, gdata, code_pos)
    if not gdata.flags['SF']:
        raise Jmp(target.name)
    return ''

def jl(code, gdata, code_pos):
    """
    Implments the JG instruction.
    Jumps if op1 > op2.
    """
    (target, code_pos) = get_one_op("JG", code, gdata, code_pos)
    if gdata.flags['SF']:
        raise Jmp(target.name)
    return ''

def jle(code, gdata, code_pos):
    """
    Implments the JGE instruction.
    Jumps if op1 >= op2.
    """
    (target, code_pos) = get_one_op("JGE", code, gdata, code_pos)
    if gdata.flags['SF'] or gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

