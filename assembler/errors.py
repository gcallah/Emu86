"""
Possible assembler errors.
"""

# Error messages (or at least their beginnings):
UNKNOWN_ERR = "Uknown parsing error."
INVALID_INSTR = "Invalid instruction: "
INVALID_OPRND = "Invalid operand: "
INVALID_NUM_ARGS = "Invalid number of args: "
INVALID_MEM_LOC = "Invalid memory location: "
INVALID_REG = "Invalid register: "
REG_UNWRITABLE = "Write attempt to unwriteable register: "
INT_OUT_OF_RNG = "Integer out of range: "

INT_MAX=(2**31)-1
INT_MIN=-(2**31)

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

class InvalidRegister(Error):
    def __init__(self, offender):
        self.msg = INVALID_REG + offender

class RegUnwritable(Error):
    def __init__(self, offender):
        self.msg = REG_UNWRITABLE + offender

class IntOutOfRng(Error):
    def __init__(self, offender):
        self.msg = INT_OUT_OF_RNG + offender

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
