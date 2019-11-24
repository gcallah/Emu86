"""
fp_arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import check_num_args, TooBigForSingle, DivisionZero
from assembler.tokens import Instruction, MAX_INT
from .argument_check import check_reg_only, check_even_register

# for floating point to binary and back
import struct
import binascii


def check_overflow(val, vm):
    if(val > MAX_INT):
        val = val - MAX_INT+1
    return val


def three_op_arith_reg(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3, line_num, type_ins=1)
    check_reg_only(instr, ops, line_num)

    # go through the register ops and make sure that they're even numbered
    for op in ops:
        check_even_register(op, line_num)

    ops[0].set_val(operator(ops[1].get_val(line_num),
                   ops[2].get_val(line_num)), line_num)
    # check_overflow(operator(ops[1].get_val(line_num),
    #                    ops[2].get_val(line_num)),
    #                    vm))
    vm.changes.add(ops[0].get_nm())


# to convert a float to a hex
# using double for a significant amount of precisions
# (i think its up to 48 bits of precision)
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


# to convert the ieee 754 hex back to the actual float value
def hex_to_float(h):
    h2 = h[2:]
    h2 = binascii.unhexlify(h2)
    return struct.unpack('>f', h2)[0]


# 'ADD.S': Adds('ADD.S'),
class Adds(Instruction):
    """
        <instr>
             ADD.S
        </instr>
        <syntax>
            ADD.S reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.add, line_num)


# 'SUB.S': Subs('SUB.S'),
class Subs(Instruction):
    """
        <instr>
             SUB.S
        </instr>
        <syntax>
            SUB.S reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.sub, line_num)


# 'MULT.S': Mults('MULT.S'),
class Mults(Instruction):
    """
        <instr>
             MULT.S
        </instr>
        <syntax>
            MULT.S reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 3, line_num, type_ins=1)
        check_reg_only(self.name, ops, line_num)
        a = ops[1].get_val(line_num)
        b = ops[2].get_val(line_num)
        result = a * b
        # this is the single version of mult for floats
        # so we don't want to be bigger than max single
        if (result > 2 ** 22):
            raise TooBigForSingle(str(result), line_num)

        ops[0].set_val(result, line_num)
        vm.changes.add(ops[0].get_nm())
        return ''


# 'DIV.S': Divs('DIV.S'),
class Divs(Instruction):
    """
        <instr>
             DIVS
        </instr>
        <syntax>
            DIVS reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 3, line_num, type_ins=1)
        check_reg_only(self.name, ops, line_num)
        if ops[2].get_val(line_num) == 0:
            raise DivisionZero(line_num)

        result = ops[1].get_val(line_num) / ops[2].get_val(line_num)
        # this is the single version of div for floats
        # so we don't want to be bigger than max single
        if (result > 2 ** 22):
            raise TooBigForSingle(str(result), line_num)
        ops[0].set_val(result, line_num)
        vm.changes.add(ops[0].get_nm())
        return ''

########################
# DOUBLE PRECISION BELOW
########################
# for double precision (64 bits) fps
# references:
# https://docs.python.org/2/library/struct.html
# https://stackoverflow.com/questions/52600983/converting-float-to-ieee754
# https://stackoverflow.com/questions/19414847/how-to-convert-floating-point-number-in-python # noqa
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:] # noqa


def f_to_b64(value):
    """

    :param value: float
    :return: binary 64 conversion of value in string format
    """
    if (value == 0):
        return "0"*64
    val = struct.unpack('q', struct.pack('d', value))[0]
    return "0" + getBin(val)


def b_to_f64(value):
    """

    :param value: binary value in string format
    :return: float 64 of binary number
    """
    if (value == "0"*64):
        return 0.0
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


def three_op_double_arith_reg(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3, line_num, type_ins=1)
    check_reg_only(instr, ops, line_num)

    is_a_neg = False
    is_b_neg = False

    # go through the register ops and make sure that they're even numbered
    # they are even good
    # first number from the pair of registers
    reg_number = int(ops[1].get_nm()[1:])
    curr_reg = "F" + str(reg_number + 0)
    next_reg = "F" + str(reg_number + 1)
    a_first_32 = vm.registers[curr_reg]
    a_last_32 = vm.registers[next_reg]
    a = a_first_32 + a_last_32
    if a != 0 and a[0] == "1":
        is_a_neg = True
        a = "0" + a[1:]

    # second number from the pair of registers
    reg_number = int(ops[2].get_nm()[1:])
    curr_reg = "F" + str(reg_number + 0)
    next_reg = "F" + str(reg_number + 1)
    b_first_32 = vm.registers[curr_reg]
    b_last_32 = vm.registers[next_reg]
    b = b_first_32 + b_last_32
    if b != 0 and b[0] == "1":
        is_b_neg = True
        b = "0" + b[1:]

    if a != 0:
        a = b_to_f64(a)

    if b != 0:
        b = b_to_f64(b)

    if is_a_neg:
        a *= -1
    if is_b_neg:
        b *= -1

    res = operator(a, b)
    is_res_neg = False
    if res < 0:
        is_res_neg = True
        res = abs(res)

    res_binary = f_to_b64(res)

    if (is_res_neg):
        res_binary = "1" + res_binary[1:]

    res_first_32 = res_binary[:32]
    res_last_32 = res_binary[32:]

    # save the result

    reg_number = int(ops[0].get_nm()[1:])
    curr_reg = "F" + str(reg_number + 0)
    next_reg = "F" + str(reg_number + 1)
    ops[0].set_val(res_first_32, line_num)
    vm.registers[next_reg] = res_last_32

    vm.changes.add(ops[0].get_nm())
    # vm.changes.add(vm.registers[curr_reg])
    vm.changes.add(vm.registers[next_reg])


class Addd(Instruction):
    """
        <instr>
             ADD.D
        </instr>
        <syntax>
            ADD.D reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm, line_num):
        three_op_double_arith_reg(ops, vm, self.name, opfunc.add, line_num)


class Subd(Instruction):
    """
        <instr>
            SUB.D
        </instr>
        <syntax>
            SUB.D reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm, line_num):
        three_op_double_arith_reg(ops, vm, self.name, opfunc.sub, line_num)


class Multd(Instruction):
    """
        <instr>
            MULT.D
        </instr>
        <syntax>
            MULT.D reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm, line_num):
        three_op_double_arith_reg(ops, vm, self.name, opfunc.mul, line_num)


class Divd(Instruction):
    """
        <instr>
            DIV.D
        </instr>
        <syntax>
            DIV.D reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm, line_num):
        three_op_double_arith_reg(ops, vm, self.name, opfunc.truediv, line_num)
