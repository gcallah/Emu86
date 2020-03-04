#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".") # noqa 

import operator as opfunc

from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.virtual_machine import riscv_machine
from assembler.assemble import assemble

NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 100   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 100  # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS

riscv_machine.base = "hex"
riscv_machine.flavor = "riscv"


def check_overflow(val, vm):
    '''
    To emulate the wraparound that occurs when a number
    has too many bits to represent in machine code.

    '''
    if (val > MAX_INT):
        val = val - MAX_INT + 1
    return val


class AssembleTestCase(TestCase):

    #####################
    # Two Operand Tests #
    #####################

    def two_op_test(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for _ in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            correct = operator(a, b)
            riscv_machine.registers["X8"] = a
            riscv_machine.registers["X9"] = b
            assemble("40000 " + instr + " X10, X8, X9", riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)

    def two_op_test_unsigned(self, operator, instr,
                             low1=MIN_TEST, high1=MAX_TEST,
                             low2=MIN_TEST, high2=MAX_TEST):
        for _ in range(0, NUM_TESTS):
            a = abs(random.randint(low1, high1))
            b = abs(random.randint(low2, high2))
            correct = operator(a, b)
            riscv_machine.registers["X8"] = a
            riscv_machine.registers["X9"] = b
            assemble("40000 " + instr + " X10, X8, X9", riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)

    def two_op_test_imm(self, operator, instr,
                        low1=MIN_TEST, high1=MAX_TEST,
                        low2=MIN_TEST, high2=MAX_TEST):
        for _ in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            hex_string = hex(b)
            correct = operator(a, int(hex(b), 16))
            riscv_machine.registers["X9"] = a
            assemble(f"40000 {instr} X10, X9, {hex_string}", riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "ADD")

    def test_add_imm(self):
        self.two_op_test_imm(opfunc.add, "ADDI")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "SUB")

    def test_mul(self):
        self.two_op_test(opfunc.mul, "MUL",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=MIN_MUL, high2=MAX_MUL)

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
        assemble("40000 SLT X10, X9, X8", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 1)

    def test_sltu(self):
        riscv_machine.registers["X8"] = -1
        riscv_machine.registers["X9"] = 0
        assemble("40000 SLTU X10, X9, X8", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 1)

    def test_slti(self):
        riscv_machine.registers["X9"] = 0
        assemble("40000 SLTI X10, X9, 1", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 1)

    def test_sltiu(self):
        riscv_machine.registers["X9"] = 0
        neg_one = '-1'
        assemble("40000 SLTIU X10, X9, " + neg_one, riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 1)

    def test_div(self):
        self.two_op_test(opfunc.floordiv, "DIV")

    def test_divu(self):
        self.two_op_test_unsigned(opfunc.floordiv, "DIVU")

    def test_rem(self):
        self.two_op_test(opfunc.mod, "REM")

    def test_remu(self):
        self.two_op_test_unsigned(opfunc.mod, "REMU")

    def test_sra(self):
        riscv_machine.registers["X8"] = 10
        riscv_machine.registers["X9"] = 4
        assemble("40000 SRA X10, X8, X9", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 0)
        riscv_machine.registers["X8"] = -10
        riscv_machine.registers["X9"] = 4
        assemble("40000 SRA X10, X8, X9", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 15)

    def test_srai(self):
        riscv_machine.registers["X8"] = 10
        assemble("40000 SRAI X10, X8, 4", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 0)
        riscv_machine.registers["X8"] = -10
        assemble("40000 SRAI X10, X8, 4", riscv_machine)
        self.assertEqual(riscv_machine.registers["X10"], 15)

    def test_lui(self):
        for _ in range(0, NUM_TESTS):
            a = random.randint(0, 1048576)
            hex_string = hex(a).upper()
            correct = check_overflow(opfunc.lshift(a, 12), riscv_machine)
            assemble("40000 LUI X10, " + hex_string, riscv_machine)
            self.assertEqual(riscv_machine.registers["X10"], correct)


'''
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

'''


if __name__ == '__main__':
    main()
