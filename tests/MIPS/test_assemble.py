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
            assemble("40000 " + instr + " R10, R8, R9", 'mips', mips_machine)
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
            assemble("40000 " + instr + " R10, R9, " + hex_string, 'mips', mips_machine)
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

    def test_nor(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            b = random.randint(MIN_TEST, MAX_TEST)
            correct = opfunc.inv(opfunc.or_(a, b))
            mips_machine.registers["R8"] = a
            mips_machine.registers["R9"] = b
            mips_machine.base = "hex"
            assemble("40000 NOR R10, R8, R9", 'mips', mips_machine)
            self.assertEqual(mips_machine.registers["R10"], correct)

    def test_slt_eq(self):
        mips_machine.registers["R8"] = 1
        mips_machine.registers["R9"] = 1
        mips_machine.base = "hex"
        assemble("40000 SLT R10, R8, R9", 'mips', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 0)

    def test_slt_l(self):
        mips_machine.registers["R8"] = 0
        mips_machine.registers["R9"] = 1
        mips_machine.base = "hex"
        assemble("40000 SLT R10, R8, R9", 'mips', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 1)

    def test_slti_eq(self):
        mips_machine.registers["R9"] = 1
        mips_machine.base = "hex"
        assemble("40000 SLTI R10, R9, 1", 'mips', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 0)

    def test_slti_l(self):
        mips_machine.registers["R9"] = 0
        mips_machine.base = "hex"
        assemble("40000 SLTI R10, R9, 1", 'mips', mips_machine)
        self.assertEqual(mips_machine.registers["R10"], 1)

    def test_sll(self):
        self.two_op_test_imm(opfunc.lshift, "SLL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_srl(self):
        self.two_op_test_imm(opfunc.rshift, "SRL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)
        
if __name__ == '__main__':
    main()
