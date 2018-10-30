"""
fp_arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT, Register, IntegerTok
from assembler.ops_check import one_op_arith
from .argument_check import * 

# for floating point to binary and back
import struct
import codecs
import binascii

def check_overflow(val, vm):
    if(val > MAX_INT):
        val = val - MAX_INT+1
    return val

def three_op_arith_reg(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)

    # go through the register ops and make sure that they're even numbered

    
    ops[0].set_val(
    check_overflow(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm)) 
    vm.changes.add(ops[0].get_nm())

#to convert a float to a hex
#using double for a significant amount of precisions
# (i think its up to 48 bits of precision)
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

#to convert the ieee 754 hex back to the actual float value
def hex_to_float(h):
    h2 = h[2:]
    h2 = binascii.unhexlify(h2)
    return struct.unpack('>f', h2)[0]

#'ADD.S': Adds('ADD.S'),
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
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.add)

#'SUB.S': Subs('SUB.S'),
class Subs(Instruction):
    """
        <instr>
             SUB.S
        </instr>
        <syntax>
            SUB.S reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.sub)

#'MULT.S': Mults('MULT.S'),
class Mults(Instruction):
    """
        <instr>
             MULT.S
        </instr>
        <syntax>
            MULT.S reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 3)
        check_reg_only(self.name, ops)
        a = ops[1].get_val()
        b = ops[2].get_val()
        result = a * b
        # this is the single version of mult for floats, so we don't want to be bigger than max single
        if (result > 2 ** 22):
            raise TooBigForSingle(str(result))

        ops[0].set_val(result)
        vm.changes.add(ops[0].get_nm())
        return ''

#'DIV.S': Divs('DIV.S'),
class Divs(Instruction):
    """
        <instr>
             DIVS
        </instr>
        <syntax>
            DIVS reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 3)
        check_reg_only(self.name, ops)
        if ops[2].get_val() == 0:
            raise DivisionZero()

        result = ops[1].get_val() / ops[2].get_val()
        # this is the single version of div for floats, so we don't want to be bigger than max single
        if (result > 2 ** 22):
            raise TooBigForSingle(str(result))
        ops[0].set_val(result)
        vm.changes.add(ops[0].get_nm())
        return ''

########################
# DOUBLE PRECISION BELOW
########################
#for double precision (64 bits) fps
# references:
    # https://docs.python.org/2/library/struct.html
    # https://stackoverflow.com/questions/52600983/converting-float-to-ieee754
    # https://stackoverflow.com/questions/19414847/how-to-convert-floating-point-number-in-python
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]
 
def f_to_b64(value):
    val = struct.unpack('q', struct.pack('d', value))[0]
    return "0" + getBin(val)

def b_to_f64(value):
    hx = hex(int(value, 2))   
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]

def three_op_double_arith_reg(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)

    # go through the register ops and make sure that they're even numbered
    print("ops 1", ops[1].get_val())
    print("ops 2", ops[2].get_val())
    
    ops[0].set_val(
    check_overflow(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm)) 
    vm.changes.add(ops[0].get_nm())

class Addd(Instruction):
    """
        <instr>
             ADD.S
        </instr>
        <syntax>
            ADD.S reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm):
        three_op_double_arith_reg(ops, vm, self.name, opfunc.add)