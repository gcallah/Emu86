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
from assembler.virtual_machine import riscv_machine
from assembler.assemble import assemble

# for floating point to binary and back
import struct
import codecs
import binascii

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
            riscv_machine.registers["X8"] = a
            riscv_machine.registers["X9"] = b
            riscv_machine.base = "hex"
            assemble("40000 " + instr + " X10, X8, X9", 'riscv', riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)

    def two_op_test_unsigned(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = abs(random.randint(low1, high1))
            b = abs(random.randint(low2, high2))
            correct = operator(a, b)
            riscv_machine.registers["X8"] = a
            riscv_machine.registers["X9"] = b
            riscv_machine.base = "hex"
            assemble("40000 " + instr + " X10, X8, X9", 'riscv', riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)

    def two_op_test_imm(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            hex_string = hex(b)
            correct = operator(a, int(hex(b), 16))
            riscv_machine.registers["X9"] = a
            riscv_machine.base = "hex"
            assemble("40000 " + instr + " X10, X9, " + hex_string, 'riscv', riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "ADD")

    def test_add_imm(self):
        self.two_op_test_imm(opfunc.add, "ADDI")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "SUB")

    def test_mul(self):
        self.two_op_test(opfunc.mul, "MUL", 
                         low1 = MIN_MUL, high1 = MAX_MUL, 
                         low2 = MIN_MUL, high2 = MAX_MUL)

    def test_and(self):
        self.two_op_test(opfunc.and_, "AND")

    def test_and_imm(self):
        self.two_op_test_imm(opfunc.and_, "ANDI")

    def test_or(self):
        self.two_op_test(opfunc.or_, "OR")
        
    def test_or_imm(self):
        self.two_op_test_imm(opfunc.or_, "ORI")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "XOR")

    def test_xor_imm(self):
        self.two_op_test_imm(opfunc.xor, "XORI")

    def test_srl(self):
        self.two_op_test(opfunc.rshift, "SRL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)
    
    def test_sll(self):
        self.two_op_test(opfunc.lshift, "SLL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_srl_imm(self):
        self.two_op_test_imm(opfunc.rshift, "SRLI",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)
    
    def test_sll_imm(self):
        self.two_op_test_imm(opfunc.lshift, "SLLI",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_slt(self): 
        riscv_machine.registers["X8"] = 1
        riscv_machine.registers["X9"] = 0
        riscv_machine.base = "hex"
        assemble("40000 SLT X10, X9, X8", 'riscv', riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 1)

    def test_sltu(self): 
        riscv_machine.registers["X8"] = 1
        riscv_machine.registers["X9"] = 0
        riscv_machine.base = "hex"
        assemble("40000 SLTU X10, X9, X8", 'riscv', riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 1)

    def test_div(self): 
        self.two_op_test(opfunc.floordiv, "DIV")

    def test_divu(self):
        self.two_op_test_unsigned(opfunc.floordiv, "DIVU")

    def test_rem(self): 
        self.two_op_test(opfunc.mod, "REM")

    def test_remu(self): 
        self.two_op_test_unsigned(opfunc.mod, "REMU")




'''
    def test_nor(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            b = random.randint(MIN_TEST, MAX_TEST)
            correct = opfunc.inv(opfunc.or_(a, b))
            riscv_machine.registers["R8"] = a
            riscv_machine.registers["R9"] = b
            riscv_machine.base = "hex"
            assemble("40000 NOR R10, R8, R9", 'riscv', riscv_machine)
            self.assertEqual(riscv_machine.registers["R10"], correct)

    def test_slt_eq(self):
        riscv_machine.registers["R8"] = 1
        riscv_machine.registers["R9"] = 1
        riscv_machine.base = "hex"
        assemble("40000 SLT R10, R8, R9", 'riscv', riscv_machine)
        self.assertEqual(riscv_machine.registers["R10"], 0)

    def test_slt_l(self):
        riscv_machine.registers["R8"] = 0
        riscv_machine.registers["R9"] = 1
        riscv_machine.base = "hex"
        assemble("40000 SLT R10, R8, R9", 'riscv', riscv_machine)
        self.assertEqual(riscv_machine.registers["R10"], 1)

    def test_slti_eq(self):
        riscv_machine.registers["R9"] = 1
        riscv_machine.base = "hex"
        assemble("40000 SLTI R10, R9, 1", 'riscv', riscv_machine)
        self.assertEqual(riscv_machine.registers["R10"], 0)

    def test_slti_l(self):
        riscv_machine.registers["R9"] = 0
        riscv_machine.base = "hex"
        assemble("40000 SLTI R10, R9, 1", 'riscv', riscv_machine)
        self.assertEqual(riscv_machine.registers["R10"], 1)
        
    def two_op_test_float(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.uniform(low1, high1)
            b = random.uniform(low2, high2)
            correct = operator(a, b)
            riscv_machine.registers["F8"] = a
            riscv_machine.registers["F9"] = b
            riscv_machine.base = "hex"
            assemble("40000 " + instr + " F10, F8, F9", 'riscv', riscv_machine)
            self.assertEqual(riscv_machine.registers["F10"], correct)

    def two_op_test_hilo_float(self, operator, instr, 
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, 1):
            a = random.uniform(low1, high1)
            b = random.uniform(low2, high2)
            correct = operator(a,b)
            riscv_machine.registers["F8"] = a
            riscv_machine.registers["F9"] = b
            riscv_machine.base = "hex"
            r = assemble("40000 " + instr + " F8, F9", 'riscv', riscv_machine)

            h_reg = str(riscv_machine.registers["HI"])
            for i in range(0, 32-len(h_reg)):
                h_reg = "0" + h_reg
            l_reg = str(riscv_machine.registers["LO"])
            for i in range(0, 32-len(l_reg)):
                l_reg = "0" + l_reg

            binary_result = h_reg + l_reg
            hex_result = hex(int(binary_result, 2))[2:]
            for i in range(0, 16-len(hex_result)):
                hex_result = "0"+hex_result
            bin_data = codecs.decode(hex_result, "hex")
            result = struct.unpack("d", bin_data)[0]
            self.assertEqual(result, correct)

    def test_adds(self):
        self.two_op_test_float(opfunc.add, "ADD.S")

    def test_subs(self):
        self.two_op_test_float(opfunc.sub, "SUB.S")

    def test_mults(self):
        self.two_op_test_hilo_float(opfunc.mul, "MULT.S")

'''

if __name__ == '__main__':
    main()
