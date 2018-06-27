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
from assembler.virtual_machine import vmachine, STACK_TOP, STACK_BOTTOM
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
            vmachine.registers["EAX"] = a
            vmachine.registers["EBX"] = b
            assemble(instr + " eax, ebx", 'intel', vmachine)
            self.assertEqual(vmachine.registers["EAX"], correct)

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

    def one_op_test(self, operator, instr):
        for i in range(NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct = operator(a)
            vmachine.registers["EAX"] = a
            assemble(instr + " eax", 'intel', vmachine)
            self.assertEqual(vmachine.registers["EAX"], correct)

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

##################
# Push / Pop     #
##################

    def test_push_and_pop(self):
        correct_stack = [None]*(STACK_TOP+1) # Note: size(correct_stack) = size(stack + memory)
        for i in range(STACK_TOP, STACK_BOTTOM-1, -1): # Traverse the stack registers.
            a = random.randint(MIN_TEST, MAX_TEST)
            correct_stack[i] = a
            vmachine.registers["EAX"] = a
            assemble("push eax", 'intel', vmachine)

        for i in range(STACK_BOTTOM, STACK_TOP+1):
            assemble("pop ebx", 'intel', vmachine)
            self.assertEqual(vmachine.registers["EBX"], correct_stack[i])

##################
# Other          #
##################

    def test_mov(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            correct = a
            vmachine.registers["EAX"] = a
            assemble("mov eax, " + str(a), 'intel', vmachine)
            self.assertEqual(vmachine.registers["EAX"], correct)

    def test_idiv(self):
        for i in range(0, NUM_TESTS):
            a = random.randint(MIN_TEST, MAX_TEST)
            d = random.randint(MIN_TEST, MAX_TEST)
            b = 0
            while(b == 0): # Divisor can't be zero.
                b = random.randint(MIN_TEST, MAX_TEST)
            correct_quotient = (opfunc.lshift(d,REGISTER_SIZE) + a) // b
            correct_remainder = (opfunc.lshift(d,REGISTER_SIZE) + a) % b
            vmachine.registers["EAX"] = a
            vmachine.registers["EDX"] = d
            vmachine.registers["EBX"] = b
            assemble("idiv ebx", 'intel', vmachine)
            self.assertEqual(vmachine.registers["EAX"], correct_quotient)
            self.assertEqual(vmachine.registers["EDX"], correct_remainder)

    def test_cmp_eq(self):
        vmachine.registers["EAX"] = 1
        vmachine.registers["EBX"] = 1
        vmachine.flags["ZF"] = 0
        vmachine.flags["SF"] = 0
        assemble("cmp eax, ebx", 'intel', vmachine)
        self.assertEqual(vmachine.flags["ZF"], 1)
        self.assertEqual(vmachine.flags["SF"], 0)

    def test_cmp_l(self):
        vmachine.registers["EAX"] = 0
        vmachine.registers["EBX"] = 1
        vmachine.flags["ZF"] = 0
        vmachine.flags["SF"] = 0
        assemble("cmp eax, ebx", 'intel', vmachine)
        self.assertEqual(vmachine.flags["ZF"], 0)
        self.assertEqual(vmachine.flags["SF"], 1)
        
if __name__ == '__main__':
    main()
