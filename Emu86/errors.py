"""
Possible assembler errors.
"""

class Error(Exception):
    """
    Base class for all of our exceptions.
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
    def __init__(self, offender, num):
        self.msg = ("Invalid number of args: " + offender
                    + " requires " + str(num))

class InvalidMemLoc(Error):
    def __init__(self, offender):
        self.msg = "Invalid memory location: " + offender

class InvalidRegister(Error):
    def __init__(self, offender):
        self.msg = "Invalid register: " + offender
