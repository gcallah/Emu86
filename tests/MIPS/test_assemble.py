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
from assembler.virtual_machine import mips_machine, STACK_TOP, STACK_BOTTOM
from assembler.assemble import assemble

NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 10   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 10   # right now we don't want to overflow!
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
            mips_machine.registers["T1"] = a
            mips_machine.registers["T2"] = b
            assemble(instr + " $t3, $t1, $t2", 'mips', mips_machine)
            self.assertEqual(mips_machine.registers["T3"], correct)

    def two_op_test_imm(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            correct = operator(a, b)
            correct_other = operator(b, a)
            mips_machine.registers["T1"] = a
            assemble(instr + " $t3, $t1, " + str(b), 'mips', mips_machine)
            assemble(instr + " $t4, " + str(b) + ", $t1", 'mips', mips_machine)
            self.assertEqual(mips_machine.registers["T3"], correct)
            self.assertEqual(mips_machine.registers["T4"], correct_other)

    def test_add(self):
        self.two_op_test(opfunc.add, "add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "sub")

    def test_and(self):
        self.two_op_test(opfunc.and_, "and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "or")

    def test_add_imm(self):
        self.two_op_test_imm(opfunc.add, "addi")

    def test_sub_imm(self):
        self.two_op_test_imm(opfunc.sub, "subi")

    def test_and_imm(self):
        self.two_op_test_imm(opfunc.and_, "andi")

    def test_or_imm(self):
        self.two_op_test_imm(opfunc.or_, "ori")

    def test_nor(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            b = random.randint(MIN_TEST, MAX_TEST)
            correct = opfunc.inv(opfunc.or_(a, b))
            mips_machine.registers["T1"] = a
            mips_machine.registers["T2"] = b
            assemble("nor $T3, $T1, $T2", 'mips', mips_machine)
            self.assertEqual(mips_machine.registers["T3"], correct)

    def test_slt_eq(self):
        mips_machine.registers["T1"] = 1
        mips_machine.registers["T2"] = 1
        mips_machine.flags["ZF"] = 0
        mips_machine.flags["SF"] = 0
        assemble("SLT $T3, $T1, $T2", 'mips', mips_machine)
        self.assertEqual(mips_machine.flags["ZF"], 1)
        self.assertEqual(mips_machine.flags["SF"], 0)
        self.assertEqual(mips_machine.registers["T3"], 0)

    def test_slt_l(self):
        mips_machine.registers["T1"] = 0
        mips_machine.registers["T2"] = 1
        mips_machine.flags["ZF"] = 0
        mips_machine.flags["SF"] = 0
        assemble("SLT $T3, $T1, $T2", 'mips', mips_machine)
        self.assertEqual(mips_machine.flags["ZF"], 0)
        self.assertEqual(mips_machine.flags["SF"], 1)
        self.assertEqual(mips_machine.registers["T3"], 1)

    def test_sll(self):
        self.two_op_test(opfunc.lshift, "sll",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_srl(self):
        self.two_op_test(opfunc.rshift, "srl",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)
        
if __name__ == '__main__':
    main()
