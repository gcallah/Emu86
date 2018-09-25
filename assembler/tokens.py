"""
tokens.py: contains classes we tokenize into.
"""

from abc import abstractmethod

from .errors import InvalidMemLoc, RegUnwritable,IntOutOfRng, UnknownName, InvalidArgument
from .errors import NotSettable

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

class ConstantSign(Token):
    """
    Class used to differentiate between
    a constant and an offset
    """
    def __init__(self):
        super().__init__("$")

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
    def __init__(self, val=0, con=True):
        if(val > MAX_INT or val < MIN_INT):
            raise IntOutOfRng(str(val))

        super().__init__("Integer", val)
        self.con = con

    def __str__(self):
        return str(self.value)

    def get_val(self):
        return self.value

    def negate_val(self):
        self.value *= -1
        
class FloatTok(Operand):
    def __init__(self, val=0.0):
        super().__init__("Float", val)

    def __str__(self):
        return str(self.value)

    def get_val(self):
        return self.value

    def negate_val(self):
        self.value *= -1.0

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
        if self.name in self.mem:
            return int(self.mem[self.name])
        else:
            return 0

    def set_val(self, val):
        self.mem[self.name] = val


class RegAddress(Address):
    def __init__(self, name, vm, displacement = 0, multiplier = 1, val=0):
        super().__init__(name, vm, val)
        self.regs = vm.registers
        self.displacement = displacement
        self.multiplier = multiplier

    def get_mem_addr(self):
        # right now, memory addresses are strings. eeh!
        address = hex(int(self.regs[self.name]) *
                          self.multiplier).split('x')[-1].upper()
        disp = 0
        if isinstance(self.displacement, list):
            for disp_item in self.displacement:
                if isinstance(disp_item, Register):
                    disp += disp_item.get_val() * disp_item.get_multiplier()
                else:
                    disp += disp_item
        elif isinstance(self.displacement, Register):
            disp = self.displacement.get_val()
        elif self.displacement != 0:
            disp = self.displacement
        addr_val = int(self.regs[self.name]) * self.multiplier + disp
        if addr_val < 0:
            raise InvalidMemLoc(str(addr_val))
        address = hex(addr_val).split('x')[-1].upper()
        return address

    def get_val(self):
        mem_addr = self.get_mem_addr()
        if mem_addr in self.mem:
            return int(self.mem[str(mem_addr)])
        else:
            return 0

    def set_val(self, val):
        mem_addr = self.get_mem_addr()
        self.mem[mem_addr] = val

class Register(Location):
    def __init__(self, name, vm, val=0):
        super().__init__(name, vm, val)
        self.registers = vm.registers
        self.val = self.registers[self.name]
        self.writable = True
        self.multiplier = 1
        if self.name in vm.unwritable:
            self.writable = False

    def __str__(self):
        return str(self.name)

    def __str__(self):
        return str(self.name)

    def get_val(self):
        if self.name[0] == "F":
            return float(self.registers[self.name])
        return int(self.registers[self.name])

    def set_val(self, val):
        if self.writable:
            self.registers[self.name] = val
        else:
            raise RegUnwritable(self.name)

    def get_multiplier(self):
        return self.multiplier

    def set_multiplier(self, val):
        if val < 0:
            raise InvalidArgument(str(val))
        self.multiplier = val

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
