#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".")

import operator as opfunc
import functools

from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.virtual_machine import mips_machine
from assembler.assemble import assemble

# for floating point to binary and back
import struct
import codecs
import binascii
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]
 
def f_to_b64(value):
    val = struct.unpack('q', struct.pack('d', value))[0]
    return "0" + getBin(val)

def b_to_f64(value):
    hx = hex(int(value, 2))   
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]

NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 100   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 100  # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS

class AssembleTestCase(TestCase):

#####################
# Two Operand Tests #
#####################

    def two_op_test(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            correct = operator(a, b)
            mips_machine.registers["R8"] = a
            mips_machine.registers["R9"] = b
            mips_machine.base = "hex"
            assemble("40000 " + instr + " R10, R8, R9", 'mips_asm', mips_machine)
            self.assertEqual(mips_machine.registers["R10"], correct)

    def two_op_test_imm(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            hex_string = hex(b)
            correct = operator(a, int(hex(b), 16))
            mips_machine.registers["R9"] = a
            mips_machine.base = "hex"
            assemble("40000 " + instr + " R10, R9, " + hex_string, 'mips_asm', mips_machine)
            self.assertEqual(mips_machine.registers["R10"], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "ADD")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "SUB")

    def test_and(self):
        self.two_op_test(opfunc.and_, "AND")

    def test_or(self):
        self.two_op_test(opfunc.or_, "OR")

    def test_add_imm(self):
        self.two_op_test_imm(opfunc.add, "ADDI")
        
    def test_and_imm(self):
        self.two_op_test_imm(opfunc.and_, "ANDI")

    def test_or_imm(self):
        self.two_op_test_imm(opfunc.or_, "ORI")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "XOR")

    def test_mult(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_MUL, MAX_MUL)
            b = random.randint(MIN_MUL, MAX_MUL)
            correct = opfunc.mul(a, b)
            mips_machine.registers["R8"] = a
            mips_machine.registers["R9"] = b
            mips_machine.base = "hex"
            low_correct, high_correct = 0, 0
            assemble("40000 MULT R8, R9", 'mips_mml', mips_machine)
            if correct > 2 ** 32 - 1:
                low_correct = opfunc.lshift(correct, 32)
                high_correct = opfunc.rshift(correct, 32)
            else:
                low_correct = correct
                high_correct = 0
            self.assertEqual(mips_machine.registers["HI"], high_correct)
            self.assertEqual(mips_machine.registers["LO"], low_correct)

    def test_nor(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            b = random.randint(MIN_TEST, MAX_TEST)
            correct = opfunc.inv(opfunc.or_(a, b))
            mips_machine.registers["R8"] = a
            mips_machine.registers["R9"] = b
            mips_machine.base = "hex"
            assemble("40000 NOR R10, R8, R9", 'mips_asm', mips_machine)
            self.assertEqual(mips_machine.registers["R10"], correct)

    def test_slt_eq(self):
        mips_machine.registers["R8"] = 1
        mips_machine.registers["R9"] = 1
        mips_machine.base = "hex"
        assemble("40000 SLT R10, R8, R9", 'mips_asm', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 0)

    def test_slt_l(self):
        mips_machine.registers["R8"] = 0
        mips_machine.registers["R9"] = 1
        mips_machine.base = "hex"
        assemble("40000 SLT R10, R8, R9", 'mips_asm', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 1)

    def test_slti_eq(self):
        mips_machine.registers["R9"] = 1
        mips_machine.base = "hex"
        assemble("40000 SLTI R10, R9, 1", 'mips_asm', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 0)

    def test_slti_l(self):
        mips_machine.registers["R9"] = 0
        mips_machine.base = "hex"
        assemble("40000 SLTI R10, R9, 1", 'mips_asm', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 1)

    def test_sll(self):
        self.two_op_test_imm(opfunc.lshift, "SLL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_srl(self):
        self.two_op_test_imm(opfunc.rshift, "SRL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)
        
    def two_op_test_float(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.uniform(low1, high1)
            b = random.uniform(low2, high2)
            correct = operator(a, b)
            mips_machine.registers["F8"] = a
            mips_machine.registers["F10"] = b
            mips_machine.base = "hex"
            assemble("40000 " + instr + " F12, F8, F10", 'mips_asm', mips_machine)
            self.assertEqual(mips_machine.registers["F12"], correct)

    def two_op_test_double_float(self, operator, instr, 
                    low1=0, high1=MAX_TEST,
                    low2=0, high2=MAX_TEST):
        for i in range(0, 1):
            a = random.uniform(low1, high1)
            b = random.uniform(low2, high2)
            correct = operator(a,b)

            a_binary = f_to_b64(a)
            mips_machine.registers["F8"] = a_binary[:32]
            mips_machine.registers["F9"] = a_binary[32:]
            
            b_binary = f_to_b64(b)
            mips_machine.registers["F10"] = b_binary[:32]
            mips_machine.registers["F11"] = b_binary[32:]
            mips_machine.base = "hex"
            r = assemble("40000 " + instr + " F12, F8, F10", 'mips_asm', mips_machine)

            # the answer from the assembly call will be in the F12, F13 registers
            first_32 = str(mips_machine.registers["F12"])
            last_32 = str(mips_machine.registers["F13"])

            binary_result = first_32 + last_32
            result = b_to_f64(binary_result)
            self.assertEqual(result, correct)


            # h_reg = str(mips_machine.registers["HI"])
            # for i in range(0, 32-len(h_reg)):
            #     h_reg = "0" + h_reg
            # l_reg = str(mips_machine.registers["LO"])
            # for i in range(0, 32-len(l_reg)):
            #     l_reg = "0" + l_reg

            # binary_result = h_reg + l_reg
            # hex_result = hex(int(binary_result, 2))[2:]
            # for i in range(0, 16-len(hex_result)):
            #     hex_result = "0"+hex_result
            # bin_data = codecs.decode(hex_result, "hex")
            # result = struct.unpack("d", bin_data)[0]
            # # print ("result", result)
            # self.assertEqual(result, correct)

    # def test_adds(self):
    #     self.two_op_test_float(opfunc.add, "ADD.S")

    # def test_subs(self):
    #     self.two_op_test_float(opfunc.sub, "SUB.S")

    # def test_mults(self):
    #     self.two_op_test_float(opfunc.mul, "MULT.S", low1 = 0, high1 = 2 ** 11, low2 = 0, high2 = 2 ** 11)

    # def test_divs(self):
    #     self.two_op_test_float(opfunc.truediv, "DIV.S", low1 = 0, high1 = 2 ** 11, low2 = 0, high2 = 2 ** 11)

    def test_addd(self):
        self.two_op_test_double_float(opfunc.add, 'ADD.D')


if __name__ == '__main__':
    main()
