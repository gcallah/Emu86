import re

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
INVALID_CONSTANT_VAL = "Invalid constant value: "
INVALID_SECTION = "Invalid section: "
INVALID_TOKEN = "Invalid argument: "
INVALID_PC = "Invalid PC: "
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
MISSING_OPS = "Missing operands where expected"
MISSING_PC = "Missing PC where expected"
MISSING_DATA = "Missing data values"
MISSING_COMMA = "Missing comma"
MISSING_OPENBRACK = "Missing opening bracket"
MISSING_OPENPAREN = "Missing opening parenthesis"
MISSING_CLOSEBRACK = "Missing closing bracket"
MISSING_CLOSEPAREN = "Missing closing parenthesis"
ZERO_DIVISION = "Division by zero"
OUT_OF_BOUNDS = "Displacement out of bounds"
TOO_BIG_FOR_SINGLE = "Value too big to store in a single precision: "
TOO_BIG_FOR_DOUBLE = "Value too big to store in a double: "
NOT_EVEN_REGISTER = "Invalid odd-numbered register: "
NOT_CORRECT_BITS = "Instruction expected integer of max length 20 bits"
TOO_PRECISE = "Floating point number has too many decimal places: "
INVALID_STRING = "The String Provided is Invalid"
STACK_FULL = "Cannot push another element, stack is full"

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


class InvalidConVal(Error):
    def __init__(self, offender):
        self.msg = INVALID_CONSTANT_VAL + offender


class InvalidInstruction(Error):
    def __init__(self, offender):
        self.msg = INVALID_INSTR + offender


class InvalidSection(Error):
    def __init__(self, offender):
        self.msg = INVALID_SECTION + offender


class InvalidArgument(Error):
    def __init__(self, offender):
        self.msg = INVALID_TOKEN + offender


class InvalidPc(Error):
    def __init__(self, offender):
        self.msg = INVALID_PC + offender


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
    def __init__(self, offender):
        self.msg = offender + ": " + PROGRAM_EXIT


class MissingOps(Error):
    def __init__(self):
        self.msg = MISSING_OPS


class MissingPc(Error):
    def __init__(self):
        self.msg = MISSING_PC


class MissingData(Error):
    def __init__(self):
        self.msg = MISSING_DATA


class MissingComma(Error):
    def __init__(self):
        self.msg = MISSING_COMMA


class MissingOpenParen(Error):
    def __init__(self):
        self.msg = MISSING_OPENPAREN


class MissingOpenBrack(Error):
    def __init__(self):
        self.msg = MISSING_OPENBRACK


class MissingCloseParen(Error):
    def __init__(self):
        self.msg = MISSING_CLOSEPAREN


class MissingCloseBrack(Error):
    def __init__(self):
        self.msg = MISSING_CLOSEBRACK


class DivisionZero(Error):
    def __init__(self):
        self.msg = ZERO_DIVISION


class OutofBounds(Error):
    def __init__(self):
        self.msg = OUT_OF_BOUNDS


class TooBigForSingle(Error):
    def __init__(self, offender):

        self.msg = TOO_BIG_FOR_SINGLE + offender


class TooBigForDouble(Error):
    def __init__(self, offender):
        self.msg = TOO_BIG_FOR_DOUBLE + offender


class NotEvenRegister(Error):
    def __init__(self, offender):
        self.msg = NOT_EVEN_REGISTER + offender


class IncorrectImmLength(Error):
    def __init__(self, offender):
        self.msg = NOT_CORRECT_BITS + offender


class TooPrecise(Error):
    def __init__(self, offender):
        self.msg = TOO_PRECISE + offender


class StackFull(Error):
    def __init__(self):
        self.msg = STACK_FULL


def check_num_args(instr, ops, correct_num, type_ins=0):
    """
    See if we have the proper number of arguments.
    """
    length = len(ops)
    if length != correct_num:
        extra_arg = None
        if length > correct_num:
            extra_arg = ops[length - 1]
        raise InvalidNumArgs(instr, correct_num, len(ops),
                             extra_arg)
    for i in range(0, length):
        if type_ins == 0 and (ops[i].get_val() > INT_MAX or
                              ops[i].get_val() < INT_MIN):
            raise IntOutOfRng(instr)


def is_notvalidstring(instr):
    match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", instr) # noqa!
