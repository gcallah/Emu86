#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
sys.path.append(".") # noqa

from unittest import TestCase, main

from assembler.virtual_machine import intel_machine, STACK_BOTTOM, STACK_TOP
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
from assembler.errors import INVALID_INSTR
from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC
from assembler.errors import MISSING_COMMA, MISSING_DATA, INVALID_TOKEN
from assembler.errors import REG_UNWRITABLE, STACK_OVERFLOW, STACK_UNDERFLOW
from assembler.errors import UNKNOWN_NM, INVALID_CONSTANT_VAL, INT_OUT_OF_RNG


class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("shove_up_reg $1, %eax",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_INSTR))

    def test_invalid_mem_loc(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("mov $666, (hell)",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_invalid_num_args(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("add $10, $22, $34, %eax",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

    def test_unknown_name(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("add fred, wilma",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(UNKNOWN_NM))

    def test_reg_unwritable(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("mov $10, %EIP",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(REG_UNWRITABLE))

    def test_stack_overflow(self):
        intel_machine.base = "dec"
        intel_machine.registers["ESP"] = STACK_BOTTOM-1
        (output, error, bit_code) = assemble("push $1",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(STACK_OVERFLOW))

    def test_stack_underflow(self):
        intel_machine.base = "dec"
        intel_machine.registers["ESP"] = STACK_TOP
        (output, error, bit_code) = assemble("pop %ebx",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(STACK_UNDERFLOW))

    def test_comma_error(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("mov $1 %eax",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(MISSING_COMMA))

    def test_comma_token_error(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("mov $1,,,, %eax",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_data_error(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble(".data \n  x: .short",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(MISSING_DATA))

    def test_mem_error_less(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("mov $0, (-30)",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_incorrect_con_b(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("movb $10000, (30)",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_CONSTANT_VAL))

    def test_incorrect_con_w(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("movw $70000, (30)",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INVALID_CONSTANT_VAL))

    def test_incorrect_con_l(self):
        intel_machine.base = "dec"
        (output, error, bit_code) = assemble("movl $4294967296, (30)",
                                             'att', intel_machine)
        self.assertTrue(error.startswith(INT_OUT_OF_RNG))


if __name__ == '__main__':
    main()
