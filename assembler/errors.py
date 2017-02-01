"""
Possible assembler errors.
"""

class Error(Exception):
    """
    Base class for all of our error exceptions.
    """
    def __init__(self, offender):
        self.msg = "Uknown parsing error."

class InvalidInstruction(Error):
    def __init__(self, offender):
        self.msg = "Invalid instruction: " + offender

class InvalidOperand(Error):
    def __init__(self, offender):
        self.msg = "Invalid operand: " + offender

class InvalidNumArgs(Error):
    def __init__(self, offender, correct_num, actual_num):
        self.msg = ("Invalid number of args: " + offender
                    + " requires " + str(correct_num)
                    + " but we got " + str(actual_num))

class InvalidMemLoc(Error):
    def __init__(self, offender):
        self.msg = "Invalid memory location: " + offender

class InvalidRegister(Error):
    def __init__(self, offender):
        self.msg = "Invalid register: " + offender

def check_num_args(instr, ops, correct_num):
    """
    See if we have the proper number of arguments.
    """
    if len(ops) != correct_num:
        raise InvalidNumArgs(instr, correct_num, len(ops))
