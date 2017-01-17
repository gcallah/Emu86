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


def jmp(code, registers, memory, flags, code_pos):
    """
    Implments the JMP instruction.
    """
    (target, code_pos) = get_one_op("JMP", code, registers, memory, flags, code_pos)
    raise Jmp(target.name)

def cmp(code, registers, memory, flags, code_pos):
    """
    Implments the CMP instruction.
    """
    (op1, op2, code_pos) = get_two_ops("CMP", code, registers, memory, flags, code_pos)
    res = op1.get_val() - op2.get_val()
    # set the proper flags
    # zero flag:
    if res == 0:
        flags['ZF'] = 1
    else:
        flags['ZF'] = 0
    # sign flag:
    if res < 0:
        flags['SF'] = 1
    else:
        flags['SF'] = 0
    return ''

def je(code, registers, memory, flags, code_pos):
    """
    Implments the JE instruction.
    """
    (target, code_pos) = get_one_op("JE", code, registers, memory, flags, code_pos)
    if flags['ZF']:
        raise Jmp(target.name)
    return ''

def jne(code, registers, memory, flags, code_pos):
    """
    Implments the JNE instruction.
    """
    (target, code_pos) = get_one_op("JNE", code, registers, memory, flags, code_pos)
    if not flags['ZF']:
        raise Jmp(target.name)
    return ''

