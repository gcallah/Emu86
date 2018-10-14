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


#for double precision (64 bits) fps
# references:
    # https://docs.python.org/2/library/struct.html
    # https://stackoverflow.com/questions/52600983/converting-float-to-ieee754
    # https://stackoverflow.com/questions/19414847/how-to-convert-floating-point-number-in-python
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]
 
def f_to_b64(value):
    val = struct.unpack('q', struct.pack('d', value))[0]
    return getBin(val)

def b_to_f(value):
    hx = hex(int(value, 2))   
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]

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
            MULT.S reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 2)
        check_reg_only(self.name, ops)
        a = ops[0].get_val()
        b = ops[1].get_val()
        result = a * b
        #convert to bit format
        # hex_result = float_to_hex(result)
        vm.registers['LO'] = result
        vm.changes.add('LO')

        # binary_result = bin(int(hex_result, 16))[2:]
        # print("result in fp_arithmetic.py mults", result)
        # print("binary result before appending is", binary_result)
        # print("Hex result before appending is", hex_result)
        # #deal with the high and low registers
        # if len(binary_result) > 32:
        # # if result > 2 ** 32 - 1:
        #     print("over 32")
        #     #first 32 bits go into hi
        #     #last 32 bits go inot low
        #     for i in range(0, 64-len(binary_result)):
        #         binary_result = "0"+binary_result

        #     vm.registers['HI'] = int(binary_result[0:32]) #first 32
        #     vm.registers['LO'] = int(binary_result[32:]) #last 32
        # else:
        #     print("under 32")
        #     vm.registers['HI'] = 0 #first 32 bits -> all 0
        #     vm.registers['LO'] = int(binary_result) #last 32 bits
        # vm.changes.add('LO')
        # vm.changes.add('HI')
        return ''

#'DIV.S': Divs('DIV.S'),
class Divs(Instruction):
    """
        <instr>
             DIVS
        </instr>
        <syntax>
            DIVS reg, reg
        </syntax>
        <descr>
            Divide the numbers. Resultant is the converted
            to hex then binary. first 32 bits go into the 
            HI and the last 32 bits go into LO
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 2)
        check_reg_only(self.name, ops)
        if ops[1].get_val() == 0:
            raise DivisionZero()

        result = ops[0].get_val() / ops[1].get_val()
        #convert to bit format
        hex_result = float_to_hex(result)
        binary_result = bin(int(hex_result, 16))[2:]
        #deal with the high and low registers
        if len(binary_result) > 32:
        # if result > 2 ** 32 - 1:
            
            #first 32 bits go into hi
            #last 32 bits go inot low
            for i in range(0, 64-len(binary_result)):
                binary_result = "0"+binary_result

            vm.registers['HI'] = int(binary_result[0:32]) #first 32
            vm.registers['LO'] = int(binary_result[32:]) #last 32
        else:
            vm.registers['HI'] = int(binary_result)
            vm.registers['LO'] = 0
        vm.changes.add('LO')
        vm.changes.add('HI')
        return ''