"""
tokens.py: contains classes we tokenize into.
"""

from abc import abstractmethod

from .errors import InvalidMemLoc, RegUnwritable,IntOutOfRng, UnknownName
from .errors import NotSettable
from .virtual_machine import vmachine

BITS = 32   # we are on a 32-bit machine
MAX_INT = (2**(BITS-1)) - 1
MIN_INT = -(2**(BITS-1))

VALS = 0
MEM_LOC = 1 

def add_debug(s, vm):
    vm.debug += (s + "\n")


class Token:
    def __init__(self, name, val=0):
        self.name = name
        self.value = val

    def __str__(self):
        return str(self.name)

    def set_val(self, val):
        raise NotSettable(str(self))

    def get_val(self):
        return self.value

    def get_nm(self):
        return self.name

class Section(Token):
    def __init__(self, name):
        super().__init__(name)

class OpenBracket(Token):
    def __init__(self):
        super().__init__("[")

class CloseBracket(Token):
    def __init__(self):
        super().__init__("]")

class OpenParen(Token):
    def __init__(self):
        super().__init__("(")

class CloseParen(Token):
    def __init__(self):
        super().__init__(")")

class DataType(Token):
    def __init__(self, name):
        super().__init__(name)

class Comma(Token):
    def __init__(self):
        super().__init__(",")
        
class Instruction(Token):
    """
    Class representing all instructions.
    """
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return str(self.name)

    def f(self, ops, vmachine):
        return self.fhook(ops, vmachine)

    @abstractmethod
    def fhook(self, ops, vmachine):
        pass

class Operand(Token):
    """
    Superclass of all operands.
    """
    def __init__(self, name, val=0):
        super().__init__(name, val)


class IntegerTok(Operand):
    def __init__(self, val=0):
        if(val > MAX_INT or val < MIN_INT):
            raise IntOutOfRng(str(val))

        super().__init__("Integer", val)

    def __str__(self):
        return str(self.value)

    def get_val(self):
        return self.value

    def negate_val(self):
        self.value *= -1

class StringTok(Token):
    def __init__(self, name):
        super().__init__(name)

class DupTok(Token):
    def __init__(self):
        super().__init__("DUP")

class QuestionTok(Token):
    def __init__(self):
        super().__init__("?")

class PlusTok(Token):
    def __init__(self):
        super().__init__("+")

class MinusTok(Token):
    def __init__(self):
        super().__init__("-")


class Location(Operand):
    """
    Class to give common type to memory and registers.
    Adds set_val(), not possible for ints!
    """
    def __init__(self, name, vm, val=0):
        super().__init__(name, val)
        self.vm = vm

    @abstractmethod
    def set_val(self, val):
        pass


class Address(Location):
    def __init__(self, name, vm, val=0):
        super().__init__(name, vm, val)
        self.mem = vm.memory

    def __str__(self):
        return "[" + str(self.name) + "]"

    def get_val(self):
        return int(self.mem[self.name])

    def set_val(self, val):
        self.mem[self.name] = val


class RegAddress(Address):
    def __init__(self, name, vm, displacement = 0, val=0):
        super().__init__(name, vm, val)
        self.regs = vm.registers
        self.displacement = displacement

    def get_mem_addr(self):
        # right now, memory addresses are strings. eeh!
        address = hex(self.regs[self.name]).split('x')[-1].upper()
        if self.displacement != 0:
            address = hex(int(self.regs[self.name]) + 
                          self.displacement).split('x')[-1].upper()
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

class SymAddress(Token):
    def __init__(self, name, displacement):
        super().__init__(name, displacement)

class Register(Location):
    def __init__(self, name, vm, val=0):
        super().__init__(name, vm, val)
        self.registers = vm.registers
        self.val = self.registers[self.name]
        self.writable = True
        if self.name in vm.unwritable:
            self.writable = False

    def __str__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def get_val(self):
        return int(self.registers[self.name])

    def set_val(self, val):
        if self.writable:
            self.registers[self.name] = val
        else:
            raise RegUnwritable(self.name)

    def negate_val(self):
        self.val *= -1

class Label(Location):
    """
    Class to hold labels for jumps.
    """
    def __init__(self, name, vm, val=0):
        super().__init__(name, vm, val)
        self.labels = vm.labels
        if self.name not in self.labels and val != 0:
            self.labels[self.name] = val

    def get_val(self):
        if self.name not in self.labels:
            raise UnknownLabel(self.name)
        else:
            return self.labels[self.name]

    def set_val(self, val):
        raise LabelNotSettable

class NewSymbol(Token):
    def __init__(self, name, index = None):
        super().__init__(name)

class Symbol(Location):
    """
    Class to hold symbols such as variable names.
    """
    def __init__(self, name, vm):
        super().__init__(name, vm)
        self.vm = vm
        self.check_nm()

    def check_nm(self):
        if self.name not in self.vm.symbols:
            raise UnknownName(self.name)

    def set_val(self, val):
        self.check_nm()
        self.vm.symbols[self.name] = val

    def get_val(self):
        self.check_nm()
        add_debug("Symbol " + self.name + " = "
                  + str(self.vm.symbols[self.name]),
                  self.vm)
        return self.vm.symbols[self.name]

