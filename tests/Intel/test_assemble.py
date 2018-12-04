#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".") # noqa
# sys.path.insert(0,'/Users/nikhilvaidyamath/Desktop/
# devops1/Emu86/assembler/Intel/fp_arithmetic.py')

import operator as opfunc
import functools
from assembler.Intel.fp_arithmetic import FAndf, FOrf, FNotf, FXor, FNeg
from assembler.Intel.fp_arithmetic import FShr, FShl, FMul
from area import Area
from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.virtual_machine import intel_machine, STACK_TOP, STACK_BOTTOM
from assembler.assemble import assemble


NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 10   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 10   # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS

INT = 0
FLOAT = 1


class AssembleTestCase(TestCase):

    #####################
    # Two Operand Tests #
    #####################

    def two_op_test(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST,
                    op_type=INT):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            if op_type == FLOAT:
                a = random.uniform(low1, high1)
                b = random.uniform(low2, high2)
                correct = float(operator(a, b))
            else:
                correct = operator(a, b)

            intel_machine.registers["EAX"] = a
            intel_machine.registers["EBX"] = b
            intel_machine.base = "dec"
            if op_type == FLOAT:
                self.assertEqual(float(operator(intel_machine.registers["EAX"],
                                 intel_machine.registers["EBX"])), correct)
            else:
                assemble(instr + " eax, ebx", 'intel', intel_machine)
                self.assertEqual(intel_machine.registers["EAX"], correct)

    def test_fadd(self):
        # print("fadd")
        self.two_op_test(opfunc.add, "FADD", op_type=FLOAT)

    def test_fsub(self):
        # print("fsub")
        self.two_op_test(opfunc.sub, "FSUB", op_type=FLOAT)

    def test_FAndf(self):
        self.two_op_test(FAndf.andFunc, "FAndf", op_type=FLOAT)

    def test_xorf(self):
        self.two_op_test(FXor.xorFunc, "FXor", op_type=FLOAT)

    def test_FOrf(self):
        self.two_op_test(FOrf.orFunc, "FOrf", op_type=FLOAT)

    def test_FMul(self):
        self.two_op_test(FMul.multiply, "FMul", op_type=FLOAT)
    # def test_fmul(self):
    #     self.two_op_test_float(opfunc.mul, "FMUL")

    # def test_FAndf(self):
    #     self.two_op_test(opfunc.and_, "FAndf")

    def test_add(self):
        self.two_op_test(opfunc.add, "add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "sub")

    def test_imul(self):
        self.two_op_test(opfunc.mul, "imul",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=MIN_MUL, high2=MAX_MUL)

    def test_and(self):
        self.two_op_test(opfunc.and_, "and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "or")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "xor")
    def computeArea(self):
        self.two_op_test(Area.computeArea, "Area")
    # def test_FShr(self):
    #     self.two_op_test_float(opfunc.rshift, "FShr",
    #                      low1=MIN_MUL, high1=MAX_MUL,
    #                      low2=0, high2=MAX_SHIFT)
    # def test_FShl(self):
    #     self.two_op_test_float(opfunc.lshift, "FShl",
    #                      low1=MIN_MUL, high1=MAX_MUL,
    #                      low2=0, high2=MAX_SHIFT)

    # def test_FOrf(self):
    #     self.two_op_test_float(opfunc.or_, "FOrf")

    # def test_FNeg(self):
    #     self.two_op_test_float(opfunc.neg, "FNeg")

    # def test_FDec(self):
    #     fdec = functools.partial(opfunc.add, -1)
    #     self.one_op_test_float(Fdec, "FDec")

    # def test_FOrf(self):
    #     self.two_op_test_float(opfunc.or_, "FOrf")

    # def test_FInc(self):
    #     FInc = functools.partial(opfunc.add, 1)
    #     self.one_op_test_float(FInc, "FInc")

    # def test_FNotf(self):
    #     self.one_op_test(opfunc.inv, "FNotf")

    def test_shl(self):
        self.two_op_test(opfunc.lshift, "shl",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_shr(self):
        self.two_op_test(opfunc.rshift, "shr",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    ###################
    # Single Op Tests #
    ###################

    def one_op_test(self, operator, instr, op_type=None):
        for i in range(NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            if op_type == FLOAT:
                a = float(random.uniform(MIN_TEST, MAX_TEST))
            correct = operator(a)
            intel_machine.registers["EAX"] = a
            intel_machine.base = "dec"
            if op_type == FLOAT:
                result = operator(intel_machine.registers["EAX"])
                self.assertEqual(result, correct)
            else:
                assemble(instr + " eax", 'intel', intel_machine)
                self.assertEqual(intel_machine.registers["EAX"], correct)

    def test_FShr(self):
        self.one_op_test(FShr.shiftRightFunc, "FShr", op_type=FLOAT)

    def test_FShl(self):
        self.one_op_test(FShl.shiftLeftFunc, "FShl", op_type=FLOAT)

    def test_FNeg(self):
        self.one_op_test(FNeg.FnegFunc, "FNeg", op_type=FLOAT)

    def test_FNotf(self):
        self.one_op_test(FNotf.notFunc, "FNotf", op_type=FLOAT)

    def test_not(self):
        self.one_op_test(opfunc.inv, "not")

    def test_neg(self):
        self.one_op_test(opfunc.neg, "neg")

    def test_inc(self):
        inc = functools.partial(opfunc.add, 1)
        self.one_op_test(inc, "inc")

    def test_dec(self):
        dec = functools.partial(opfunc.add, -1)
        self.one_op_test(dec, "dec")

    # def test_FNeg(self):
    #     self.one_op_test_float(opfunc.neg, "FNeg")

    ##################
    # Push / Pop     #
    ##################

    def test_push_and_pop(self):
        # Note: size(correct_stack) = size(stack + memory)
        correct_stack = [None] * (STACK_TOP+1)

        # Traverse the stack registers.
        for i in range(STACK_TOP, STACK_BOTTOM-1, -1):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct_stack[i] = a
            intel_machine.registers["EAX"] = a
            intel_machine.base = "dec"
            assemble("push eax", 'intel', intel_machine)

        for i in range(STACK_BOTTOM, STACK_TOP+1):
            assemble("pop ebx", 'intel', intel_machine)
            self.assertEqual(intel_machine.registers["EBX"], correct_stack[i])

    ##################
    # Other          #
    ##################

    def test_mov(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct = a
            intel_machine.registers["EAX"] = a
            intel_machine.base = "dec"
            assemble("mov eax, " + str(a), 'intel', intel_machine)
            self.assertEqual(intel_machine.registers["EAX"], correct)

    def test_idiv(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            d = random.randint(MIN_TEST, MAX_TEST)
            b = 0
            while(b == 0):    # Divisor can't be zero.
                b = random.randint(MIN_TEST, MAX_TEST)
            correct_quotient = (opfunc.lshift(d, REGISTER_SIZE) + a) // b
            correct_remainder = (opfunc.lshift(d, REGISTER_SIZE) + a) % b
            intel_machine.registers["EAX"] = a
            intel_machine.registers["EDX"] = d
            intel_machine.registers["EBX"] = b
            intel_machine.base = "dec"
            assemble("idiv ebx", 'intel', intel_machine)
            self.assertEqual(intel_machine.registers["EAX"],
                             correct_quotient)
            self.assertEqual(intel_machine.registers["EDX"],
                             correct_remainder)

    def test_cmp_eq(self):
        intel_machine.registers["EAX"] = 1
        intel_machine.registers["EBX"] = 1
        intel_machine.flags["ZF"] = 0
        intel_machine.flags["SF"] = 0
        intel_machine.base = "dec"
        assemble("cmp eax, ebx", 'intel', intel_machine)
        self.assertEqual(intel_machine.flags["ZF"], 1)
        self.assertEqual(intel_machine.flags["SF"], 0)

    def test_cmp_l(self):
        intel_machine.registers["EAX"] = 0
        intel_machine.registers["EBX"] = 1
        intel_machine.flags["ZF"] = 0
        intel_machine.flags["SF"] = 0
        intel_machine.base = "dec"
        assemble("cmp eax, ebx", 'intel', intel_machine)
        self.assertEqual(intel_machine.flags["ZF"], 0)
        self.assertEqual(intel_machine.flags["SF"], 1)


if __name__ == '__main__':
    main()
