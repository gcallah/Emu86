#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
sys.path.append(".") # noqa
import random

import operator as opfunc
import functools

from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.virtual_machine import wasm_machine, STACK_TOP, STACK_BOTTOM
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
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = b
            wasm_machine.inc_sp()
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = a
            wasm_machine.base = "dec"
            assemble(instr, 'wasm', wasm_machine)
            sp = wasm_machine.get_sp()
            self.assertEqual(wasm_machine.stack[hex(sp).split('x')[-1].upper()], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "i32.add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "i32.sub")

    def test_mul(self):
        self.two_op_test(opfunc.mul, "i32.mul")

if __name__ == '__main__':
    main()