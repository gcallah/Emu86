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
INVALID_VAR_DECL = "Invalid variable declaration: "
INVALID_DATA_TYPE = "Invalid data type: "
INVALID_DATA_VAL = "Invalid data value: "
INVALID_SECTION = "Invalid section: "
INVALID_TOKEN = "Invalid argument: "
LABEL_NOT_SETTABLE = "Label values can't be reset."
NOT_SETTABLE = "This operand type can't have its value set: "
PROGRAM_EXIT = "Program exit"
REG_UNWRITABLE = "Write attempt to unwriteable register: "
STACK_OVERFLOW = "Stack overflow."
STACK_UNDERFLOW = "Stack underflow."
UNKNOWN_ERR = "Unknown parsing error."
UNKNOWN_INT = "Unknown interrupt instruction: "
UNKNOWN_NM = "Unknown symbol: "
UNKNOWN_LABEL = "Unknown label: "
MISSING_DATA = "Missing data values"

INT_MAX = (2**31)-1
INT_MIN = -(2**31)

class Error(Exception):
    """
    Base class for all of our error exceptions.
    """
    def __init__(self, offender):
        self.msg = UNKNOWN_ERR

class UnknownInt(Error):
    def __init__(self, offender):
        self.msg = UNKNOWN_INT + offender

class RegUnwritable(Error):
    def __init__(self, offender):
        self.msg = REG_UNWRITABLE + offender

class InvalidVarDeclaration(Error):
    def __init__(self, offender):
        self.msg = INVALID_VAR_DECL + offender

class InvalidDataType(Error):
    def __init__(self, offender):
        self.msg = INVALID_DATA_TYPE + offender

class InvalidDataVal(Error):
    def __init__(self, offender):
        self.msg = INVALID_DATA_VAL + offender

class InvalidInstruction(Error):
    def __init__(self, offender):
        self.msg = INVALID_INSTR + offender

class InvalidSection(Error):
    def __init__(self, offender):
        self.msg = INVALID_SECTION + offender

class InvalidArgument(Error):
    def __init__(self, offender):
        self.msg = INVALID_TOKEN + offender

class NotSettable(Error):
    def __init__(self, offender):
        self.msg = NOT_SETTABLE + offender

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

class MissingData(Error):
    def __init__(self):
        self.msg = MISSING_DATA

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
        if(ops[i].get_val() > INT_MAX or ops[i].get_val() < INT_MIN ):
            raise IntOutOfRng(instr)
