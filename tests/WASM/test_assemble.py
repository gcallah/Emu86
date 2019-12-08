#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
sys.path.append(".") # noqa
import random

import operator as opfunc
# import functools

from unittest import TestCase, main

from assembler.tokens import MAX_INT, MIN_INT, BITS
from assembler.virtual_machine import wasm_machine  # STACK_TOP, STACK_BOTTOM
from assembler.assemble import assemble


NUM_TESTS = 100
MAX_SHIFT = BITS // 2
MIN_TEST = MIN_INT // 10   # right now we don't want to overflow!
MAX_TEST = MAX_INT // 10   # right now we don't want to overflow!
MAX_MUL = 10000  # right now we don't want to overflow!
MIN_MUL = -10000  # right now we don't want to overflow!
REGISTER_SIZE = BITS

wasm_machine.base = "dec"
wasm_machine.flavor = "wasm"
LINE_NUM = 1


class AssembleTestCase(TestCase):

    #####################
    # Two Operand Tests #
    #####################

    def one_op_test(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            correct = operator(a)
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = a
            wasm_machine.inc_sp(LINE_NUM)
            assemble(instr, wasm_machine)
            wasm_machine.dec_sp(LINE_NUM)
            sp = wasm_machine.get_sp()
            position = hex(sp).split('x')[-1].upper()
            self.assertEqual(wasm_machine.stack[position], correct)

    def two_op_test(self, operator, instr,
                    low1=MIN_TEST, high1=MAX_TEST,
                    low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = random.randint(low1, high1)
            b = random.randint(low2, high2)
            correct = operator(a, b)
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = b
            wasm_machine.inc_sp(LINE_NUM)
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = a
            wasm_machine.inc_sp(LINE_NUM)
            assemble(instr, wasm_machine)
            wasm_machine.dec_sp(LINE_NUM)
            position = hex(wasm_machine.get_sp()).split('x')[-1].upper()
            self.assertEqual(wasm_machine.stack[position], correct)

    def two_op_test_unsigned(self, operator, instr,
                             low1=MIN_TEST, high1=MAX_TEST,
                             low2=MIN_TEST, high2=MAX_TEST):
        for i in range(0, NUM_TESTS):
            a = abs(random.randint(low1, high1))
            b = abs(random.randint(low2, high2))
            correct = operator(a, b)
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = b
            wasm_machine.inc_sp(LINE_NUM)
            sp = wasm_machine.get_sp()
            wasm_machine.stack[hex(sp).split('x')[-1].upper()] = a
            wasm_machine.inc_sp(LINE_NUM)
            assemble(instr, wasm_machine)
            wasm_machine.dec_sp(LINE_NUM)
            sp = wasm_machine.get_sp()
            position = hex(sp).split('x')[-1].upper()
            self.assertEqual(wasm_machine.stack[position], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "i32.add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "i32.sub")

    def test_mul(self):
        self.two_op_test(opfunc.mul, "i32.mul")

    def test_div_s(self):
        self.two_op_test(opfunc.floordiv, "i32.div_s")

    def test_div_u(self):
        self.two_op_test_unsigned(opfunc.floordiv, "i32.div_u")

    def test_rem_s(self):
        self.two_op_test(opfunc.mod, "i32.rem_s")

    def test_rem_u(self):
        self.two_op_test_unsigned(opfunc.mod, "i32.rem_u")

    def test_and(self):
        self.two_op_test(opfunc.and_, "i32.and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "i32.or")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "i32.xor")

    def test_shl(self):
        self.two_op_test(opfunc.lshift, "i32.shl",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_shr_s(self):
        self.two_op_test(opfunc.rshift, "i32.shr_s",
                         low1=MIN_MUL, high1=MAX_MUL,
                         low2=0, high2=MAX_SHIFT)

    def test_shr_u(self):
        self.two_op_test_unsigned(opfunc.rshift, "i32.shr_u",
                                  low1=MIN_MUL, high1=MAX_MUL,
                                  low2=0, high2=MAX_SHIFT)

    def test_rotl(self):
        def calc_correct_rotl(a, b):
            a_bin = bin(a)[2:]
            diff = 0
            if len(a_bin) < 32:
                diff = 32 - len(a_bin)
            for i in range(0, diff):
                a_bin = "0" + a_bin
            b = b % 32  # only for i32
            result = a_bin[b:] + a_bin[:b]
            return int(result, 2)
        self.two_op_test_unsigned(calc_correct_rotl, "i32.rotl")

    def test_rotr(self):
        def calc_correct_rotr(a, b):
            a_bin = bin(a)[2:]
            diff = 0
            if len(a_bin) < 32:
                diff = 32 - len(a_bin)
            for i in range(0, diff):
                a_bin = "0" + a_bin
            b = b % 32  # only for i32
            result = a_bin[-b:] + a_bin[:len(a_bin)-b]
            return int(result, 2)
        self.two_op_test_unsigned(calc_correct_rotr, "i32.rotr")

    def test_clz(self):
        def calc_correct_clz(a):
            a_bin = bin(a)[2:]
            result = 0
            for i in a_bin:
                if i == "0":
                    result += 1
                else:
                    break
            return result
        self.one_op_test(calc_correct_clz, "i32.clz")

    def test_ctz(self):
        def calc_correct_ctz(a):
            a_bin = bin(a)[2:]
            result = 0
            for i in a_bin[::-1]:
                if i == "0":
                    result += 1
                else:
                    break
            return result
        self.one_op_test(calc_correct_ctz, "i32.ctz")

    def test_popcnt(self):
        def calc_correct_popcnt(a):
            a_bin = bin(a)[2:]
            result = 0
            for i in a_bin:
                if i == "1":
                    result += 1
            return result
        self.one_op_test(calc_correct_popcnt, "i32.popcnt")

    def test_eqz(self):
        def calc_correct_eqz(a):
            if a == 0:
                return True
            else:
                return False
        self.one_op_test(calc_correct_eqz, "i32.eqz")


if __name__ == '__main__':
    main()
