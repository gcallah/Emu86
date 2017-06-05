"""
tokens.py: contains classes we tokenize into.
"""

from abc import abstractmethod

from .errors import InvalidMemLoc, RegUnwritable,IntOutOfRng
from .global_data import gdata

BITS = 32   # we are on a 32-bit machine
MAX_INT = (2**(BITS-1)) - 1
MIN_INT = -(2**(BITS-1))

class Token:
    def __init__(self, name, val=0):
        self.name = name
        self.value = val

    def __str__(self):
        return str(self.name) + ": " + str(self.value)

    def get_val(self):
        return self.value

    def get_nm(self):
        return self.name


class Instruction(Token):
    """
    Class representing all instructions.
    """
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return str(self.name)

    def f(self, ops, gdata):
        self.fhook(ops, gdata)
        s = self.name + " "
        for op in ops:
            s += str(op)
            s += " "
        return s

    @abstractmethod
    def fhook(self, ops, gdata):
        pass

class Operand(Token):
    """
    Superclass of all operands.
    """
    def __init__(self, name, val=0):
        super().__init__(name, val)


class IntOp(Operand):
    def __init__(self, val=0):
        if(val > MAX_INT or val < MIN_INT):
            raise IntOutOfRng(str(val))

        super().__init__("IntOp", val)

    def __str__(self):
        return str(self.value)


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
        self.mem = memory

    def __str__(self):
        return "[" + str(self.name) + "]"

    def get_val(self):
        return int(self.mem[self.name])

    def set_val(self, val):
        self.mem[self.name] = val


class RegAddress(Address):
    def __init__(self, name, registers, memory, val=0):
        super().__init__(name, memory)
        self.regs = registers

    def get_mem_addr(self):
        # right now, memory addresses are strings. eeh!
        address = str(self.regs[self.name])
        if address in self.mem:
            return address
        else:
            # can't let user expand memory just by addressing it!
            raise InvalidMemLoc(address)

    def get_val(self):
        mem_addr = self.get_mem_addr()
        return int(self.mem[str(mem_addr)])

    def set_val(self, val):
        mem_addr = self.get_mem_addr()
        self.mem[mem_addr] = val


class Register(Location):
    def __init__(self, name, registers):
        super().__init__(name)
        self.registers = registers
        self.val = registers[self.name]
        self.writable = True
        if self.name in gdata.unwritable:
            self.writable = False

    def __str__(self):
        return str(self.name)

    def get_val(self):
        return int(self.registers[self.name])

    def set_val(self, val):
        if self.writable:
            self.registers[self.name] = val
        else:
            raise RegUnwritable(self.name)


class Symbol(Location):
    """
    Class to hold symbols such as labels.
    """
    def __init__(self, name):
        super().__init__(name)
