"""
tokens.py: contains classes we tokenize into.
"""

from abc import abstractmethod

from errors import *  # import * OK here:
                       # these are *our* errors, after all!

class Token:
    def __init__(self, name, val=0):
        self.name = name
        self.value = val

    def __str__(self):
        return self.name + ": " + str(self.value)

    def get_val(self):
        return self.value

    def get_nm(self):
        return self.name


class Instruction(Token):
    """
    Class representing all instructions.
    """
    def __init__(self, name, instructions):
        super().__init__(name)
        if name not in instructions:
            raise InvalidInstruction(name)
        self.func = instructions[name]
        self.ops = []

    def exec(self, ops, gdata):
        return self.func(ops, gdata)


class Operand(Token):
    """
    Superclass of all operands.
    """
    def __init__(self, name, val=0):
        super().__init__(name, val)


class IntOp(Operand):
    def __init__(self, val=0):
        super().__init__("IntOp", val)


class Location(Operand):
    """
    Class to give common type to memory and registers.
    Adds set_val(), not possible for ints!
    """
    @abstractmethod
    def set_val(self):
        pass


class Address(Location):
    def __init__(self, name, memory, val=0):
        super().__init__(name)
        self.memory = memory

    def get_val(self):
        return int(self.memory[self.name])

    def set_val(self, val):
        self.memory[self.name] = val


class Register(Location):
    def __init__(self, name, registers):
        super().__init__(name)
        self.registers = registers

    def get_val(self):
        return int(self.registers[self.name])

    def set_val(self, val):
        self.registers[self.name] = val


class Symbol(Location):
    """
    Class to hold symbols such as labels.
    """
    def __init__(self, name):
        super().__init__(name)
