"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

Contains:
    cmp
    jmp
    jnz
    jz
    jg
    jge
    jl
    jle
    FlowBreak
    Jmp
"""


class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Uknown control flow exception."

def get_one_op(instr, ops):
    if len(ops) != 1:
        raise(InvalidNumArgs(instr))
    return ops[0]

def get_two_ops(instr, ops):
    if len(ops) != 2:
        raise(InvalidNumArgs(instr))
    return (ops[0], ops[1])

class Jmp(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


def jmp(ops, gdata):
    """
    Implments the JMP instruction.
    This is an unconditional jump.
    """
    target = get_one_op("JMP", ops)
    raise Jmp(target.name)

def cmp(ops, gdata):
    """
    Implments the CMP instruction.
    Compares op1 and op2, and sets (right now) the SF and ZF flags.
    It is not clear at this moment how to treat the OF and CF flags in Python,
    since Python integer arithmetic never carries or overflows!
    """
    (op1, op2) = get_two_ops("CMP", ops)
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

def je(ops, gdata):
    """
    Implments the JE instruction.
    Jumps if op1 == op2.
    """
    target = get_one_op("JE", ops)
    if gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

def jne(ops, gdata):
    """
    Implments the JNE instruction.
    Jumps if op1 != op2.
    """
    target = get_one_op("JNE", ops)
    if not gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

def jg(ops, gdata):
    """
    Implments the JG instruction.
    Jumps if op1 > op2.
    """
    target = get_one_op("JG", ops)
    if not gdata.flags['SF'] and not gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

def jge(ops, gdata):
    """
    Implments the JGE instruction.
    Jumps if op1 >= op2.
    """
    target = get_one_op("JGE", ops)
    if not gdata.flags['SF']:
        raise Jmp(target.name)
    return ''

def jl(ops, gdata):
    """
    Implments the JG instruction.
    Jumps if op1 > op2.
    """
    target = get_one_op("JG", ops)
    if gdata.flags['SF']:
        raise Jmp(target.name)
    return ''

def jle(ops, gdata):
    """
    Implments the JGE instruction.
    Jumps if op1 >= op2.
    """
    target = get_one_op("JGE", ops)
    if gdata.flags['SF'] or gdata.flags['ZF']:
        raise Jmp(target.name)
    return ''

