"""
tokens.py: contains classes we tokenize into.
"""

# for floating point to binary and back
import struct
import binascii
import sys

from abc import abstractmethod

from .errors import InvalidMemLoc, RegUnwritable, IntOutOfRng
from .errors import UnknownName, InvalidArgument
from .errors import NotSettable, UnknownLabel, LabelNotSettable
from .errors import TooBigForSingle, TooBigForDouble

BITS = 32   # we are on a 32-bit machine
MAX_INT = (2**(BITS-1)) - 1
MIN_INT = -(2**(BITS-1))

MAX_FLOAT = sys.float_info.max
MIN_FLOAT = sys.float_info.min

VALS = 0
MEM_LOC = 1


def add_debug(s, vm):
    vm.debug += (s + "\n")


# 32 bits
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


def hex_to_float(h):
    h2 = h[2:]
    h2 = binascii.unhexlify(h2)
    return struct.unpack('>f', h2)[0]


# 64 bits
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:] # noqa


def h_to_b64(value):
    return "0" + hex(int(value, 2))


def f_to_b64(value):
    if (value == 0):
        return "0"*64
    val = struct.unpack('q', struct.pack('d', value))[0]
    return "0" + getBin(val)


def b_to_f64(value):
    if (value == "0"*64):
        return 0.0
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


class Token:
    def __init__(self, name, val=0):
        self.name = name
        self.value = val

    def __str__(self):
        return str(self.name)

    def set_val(self, val):
        raise NotSettable(str(self))

    def get_val(self, line_num=None):
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

    def f(self, ops, vmachine, line_number):
        return self.fhook(ops, vmachine, line_number)

    @abstractmethod
    def fhook(self, ops, vmachine, line_number):
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

    def get_val(self, line_num):
        return self.value

    def negate_val(self):
        self.value *= -1


class FloatTok(Operand):
    def __init__(self, data_type=".float", val=0.0):
        self.data_type = data_type
        # do a bit of error checking for precision for the hex value
        if data_type == ".float":
            # if type(val) is float:
            #     temp_hex = float_to_hex(val)
            #     temp_val = hex_to_float(temp_hex)
            #     if (temp_val != val):
            #         raise TooBigForSingle(str(val))
            if type(val) is str:
                temp_float = hex_to_float(val)
                temp_hex = float_to_hex(temp_float)
                if (temp_hex != val):
                    raise TooBigForSingle(str(val))
        elif data_type == ".double":
            if type(val) is float:
                temp_bin = f_to_b64(val)
                temp_float = b_to_f64(temp_bin)
                if (temp_float != val):
                    raise TooBigForDouble(str(val))
            elif type(val) is str:
                temp_float = b_to_f64(val)
                temp_bin2 = f_to_b64(temp_float)
                temp_float2 = b_to_f64(temp_bin2)
                if temp_float != temp_float2:
                    raise TooBigForDouble(str(val))

        super().__init__("Float", val)

    def __str__(self):
        return str(self.get_val())

    def get_type(self):
        return self.data_type

    # self.value is either going to be a float (12.2)
    # or a hexadecimal string ('0x41433333')
    # we need to be able to reconcile the actual value of it
    # if it's a hex string (IEEE 754)
    def get_val(self, line_num):
        if type(self.value) is float:
            return self.value

        # it is single precision as hexadecimal
        # convert the hexadecimal to be a float
        if self.data_type == ".float":
            return float('%.3f' % (hex_to_float(self.value)))
        else:
            return float('%.4f' % (b_to_f64(self.value)))

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

    def get_val(self, line_num):
        if self.name in self.mem:
            if "." in str(self.mem[self.name]):
                return float(self.mem[self.name])
            return int(self.mem[self.name])
        else:
            return 0

    def set_val(self, val, line_num):
        self.mem[self.name] = val

    def get_mem_addr(self, line_num):
        return self.name


class RegAddress(Address):
    def __init__(self, name, vm, displacement=0, multiplier=1, val=0):
        super().__init__(name, vm, val)
        self.regs = vm.registers
        self.displacement = displacement
        self.multiplier = multiplier

    def get_mem_addr(self, line_num):
        # right now, memory addresses are strings. eeh!
        address = hex(int(self.regs[self.name]) *
                      self.multiplier).split('x')[-1].upper()
        disp = 0
        if isinstance(self.displacement, list):
            for disp_item in self.displacement:
                if isinstance(disp_item, Register):
                    disp += disp_item.get_val(line_num) * \
                            disp_item.get_multiplier()
                else:
                    disp += disp_item
        elif isinstance(self.displacement, Register):
            disp = self.displacement.get_val(line_num)
        elif self.displacement != 0:
            disp = self.displacement
        addr_val = int(self.regs[self.name]) * self.multiplier + disp
        if addr_val < 0:
            raise InvalidMemLoc(str(addr_val), line_num)
        address = hex(addr_val).split('x')[-1].upper()
        return address

    def get_val(self, line_num):
        mem_addr = self.get_mem_addr(line_num)
        if mem_addr in self.mem:
            return self.mem[str(mem_addr)]
        else:
            return 0

    def set_val(self, val, line_num):
        mem_addr = self.get_mem_addr(line_num)
        self.mem[str(mem_addr)] = val


class Register(Location):
    def __init__(self, name, vm, val=0):
        super().__init__(name, vm, val)
        # isFloat = False
        # if name[:2].upper() == 'ST':
        #     isFloat = True
        # if isFloat:
        #     self.registers = vm.fp_stack_registers
        # # if FLOAT ==True:
        # #     self.registers = vm.fp_stack_registers
        # #     #self.val = self.registers[self.name]
        # #     print("registers changed")
        # else:
        #     self.registers = vm.registers
        self.registers = vm.registers
        self.val = self.registers[self.name]
        self.writable = True
        self.multiplier = 1
        if self.name in vm.unwritable:
            self.writable = False

    def __str__(self):
        return str(self.name)

    def get_val(self, line_num):
        if self.name[:2].upper() == "ST" or self.name[0].upper() == "F":
            return float(self.registers[self.name])
        return int(self.registers[self.name])

    def set_val(self, val, line_num):
        if self.writable:
            self.registers[self.name] = val
        else:
            raise RegUnwritable(self.name, line_num)

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

    def get_val(self, line_num):
        if self.name not in self.labels:
            raise UnknownLabel(self.name)
        else:
            return self.labels[self.name]

    def set_val(self, val):
        raise LabelNotSettable(self.name)


class NewSymbol(Token):
    def __init__(self, name, index=None):
        super().__init__(name)
        self.val = 0

    def get_val(self, line_num):
        return self.val

    def set_val(self, value):
        self.val = value


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

    def get_val(self, line_num):
        self.check_nm()
        add_debug("Symbol " + self.name + " = "
                  + str(self.vm.symbols[self.name]),
                  self.vm)
        return self.vm.symbols[self.name]
