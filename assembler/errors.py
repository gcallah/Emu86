"""
Possible assembler errors.
"""

# Error messages (or at least their beginnings):
UNKNOWN_ERR = "Uknown parsing error."
INVALID_INSTR = "Invalid instruction: "
INVALID_OPRND = "Invalid operand: "
INVALID_NUM_ARGS = "Invalid number of args: "
INVALID_MEM_LOC = "Invalid memory location: "
STACK_FULL = "Stack is full: "
STACK_EMPTY = "Stack is empty: "
INVALID_REG = "Invalid register: "
REG_UNWRITABLE = "Write attempt to unwriteable register: "
INT_OUT_OF_RNG = "Integer out of range: "
STACK_OVERFLOW = "Stack overflow."
STACK_UNDERFLOW = "Stack underflow."

class Error(Exception):
    """
    Base class for all of our error exceptions.
    """
    def __init__(self, offender):
        self.msg = UNKNOWN_ERR

class RegUnwritable(Error):
    def __init__(self, offender):
        self.msg = REG_UNWRITABLE + offender

class InvalidInstruction(Error):
    def __init__(self, offender):
        self.msg = INVALID_INSTR + offender

class InvalidOperand(Error):
    def __init__(self, offender):
        self.msg = INVALID_OPRND + offender

class InvalidNumArgs(Error):
    def __init__(self, offender, correct_num, actual_num,
                 extra_arg=None):
        extra = ""
        if extra_arg is not None:
            extra = "; possible extra = " + str(extra_arg)
        self.msg = (INVALID_NUM_ARGS + offender
                    + " requires " + str(correct_num)
                    + " but we got " + str(actual_num)
                    + extra)

class InvalidMemLoc(Error):
    def __init__(self, offender):
        self.msg = INVALID_MEM_LOC + offender

class StackFull(Error):
    def __init__(self, offender):
        self.msg = STACK_FULL + offender

class StackEmpty(Error):
    def __init__(self,offender):
        self.msg = STACK_EMPTY + offender

class InvalidRegister(Error):
    def __init__(self, offender):
        self.msg = INVALID_REG + offender

class RegUnwritable(Error):
    def __init__(self, offender):
        self.msg = REG_UNWRITABLE + offender

class IntOutOfRng(Error):
    def __init__(self, offender):
        self.msg = INT_OUT_OF_RNG + offender

class StackOverflow(Error):
    def __init__(self):
        self.msg = STACK_OVERFLOW

class StackUnderflow(Error):
    def __init__(self):
        self.msg = STACK_UNDERFLOW

def check_num_args(instr, ops, correct_num):
    """
    See if we have the proper number of arguments.
    """
    l = len(ops)
    if l != correct_num:
        extra_arg = None
        if l > correct_num:
            extra_arg = ops[l - 1]
        raise InvalidNumArgs(instr, correct_num, len(ops),
                             extra_arg)
