"""
Possible assembler errors.
"""

# Error messages (or at least their beginnings):
INT_OUT_OF_RNG = "Integer out of range: "
INVALID_INSTR = "Invalid instruction: "
INVALID_OPRND = "Invalid operand: "
INVALID_NUM_ARGS = "Invalid number of args: "
INVALID_MEM_LOC = "Invalid memory location: "
INVALID_REG = "Invalid register: "
LABEL_NOT_SETTABLE = "Label values can't be reset."
PROGRAM_EXIT = "Program exit"
REG_UNWRITABLE = "Write attempt to unwriteable register: "
STACK_OVERFLOW = "Stack overflow."
STACK_UNDERFLOW = "Stack underflow."
UNKNOWN_ERR = "Uknown parsing error."
UNKNOWN_INT = "Uknown interrupt instruction."
UNKNOWN_NM = "Unknown symbol: "
UNKNOWN_NM = "Unknown label: "

INT_MAX=(2**31)-1
INT_MIN=-(2**31)

class Error(Exception):
    """
    Base class for all of our error exceptions.
    """
    def __init__(self, offender):
        self.msg = UNKNOWN_ERR

class UnknownInt(Error):
    def __init__(self):
        self.msg = UNKNOWN_INT

class RegUnwritable(Error):
    def __init__(self, offender):
        self.msg = REG_UNWRITABLE + offender

class InvalidInstruction(Error):
    def __init__(self, offender):
        self.msg = INVALID_INSTR + offender

class LabelNotSettable(Error):
    def __init__(self, offender):
        self.msg = LABEL_NOT_SETTABLE + offender

class UnknownLabel(Error):
    def __init__(self, offender):
        self.msg = UNKNOWN_LABEL + offender

class UnknownName(Error):
    def __init__(self, offender):
        self.msg = UNKNOWN_NM + offender

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

class ExitProg(Error):
    def __init__(self):
        self.msg = PROGRAM_EXIT

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
    for i in range(0,l-1):
        if(ops[i].get_val()>INT_MAX or ops[i].get_val()<INT_MIN ):
            raise IntOutOfRng(instr)
