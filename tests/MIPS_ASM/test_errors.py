#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".")


from unittest import TestCase, main

from assembler.virtual_machine import mips_machine
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
from assembler.errors import UNKNOWN_ERR, INVALID_INSTR, INVALID_OPRND
from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, INVALID_REG
from assembler.errors import MISSING_COMMA, MISSING_DATA, INVALID_TOKEN
from assembler.errors import REG_UNWRITABLE, STACK_OVERFLOW, STACK_UNDERFLOW
from assembler.errors import UNKNOWN_NM, MISSING_PC, INT_OUT_OF_RNG
from assembler.errors import TOO_BIG_FOR_SINGLE, TOO_BIG_FOR_DOUBLE, NOT_EVEN_REGISTER

class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 shove_up_reg R8, 1", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(INVALID_INSTR))

    def test_invalid_mem_loc(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 SW R10, 3(hell)", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_invalid_num_args(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ADDI R10, 10, 22, 34", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

# we have to clear up symbol handling to make this test work.
#    def test_unknown_name(self):
#        (output, error) = assemble("add fred, wilma", vmachine)
#        self.assertTrue(error.startswith(UNKNOWN_NM))

    def test_reg_unwritable(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ADDI R0, R8, 10", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(REG_UNWRITABLE))

    def test_comma_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 SUBI R8 R8 1", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(MISSING_COMMA))

    def test_comma_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ORI R10,,,, 1", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_data_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble(".data \n  x: .word", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(MISSING_DATA))

    def pc_data_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble(".data \n  x: .word", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(MISSING_PC))

    def test_mem_error_less(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 SW R10, -3(R28)", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_out_of_range(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ADDI R8, R8, 100000000", 'mips_asm', mips_machine)
        self.assertTrue(error.startswith(INT_OUT_OF_RNG))

    def test_too_big_for_single(self):
        mips_machine.base = "dec"
        (output, error, bit_code) = assemble(".data \n x: .float 2342323423.2", "mips_asm", mips_machine)
        self.assertTrue(error.startswith(TOO_BIG_FOR_SINGLE))

    def test_too_big_for_double(self):
        mips_machine.base = "dec"
        test = (2.0 * (10.0 ** 14.0) + 1.111111)
        (output, error, bit_code) = assemble(".data \n x: .double " + str(test), "mips_asm", mips_machine)
        self.assertTrue(error.startswith(TOO_BIG_FOR_DOUBLE))

    def test_not_even_register(self):
        mips_machine.base = "dec"
        (output, error, bit_code) = assemble("40000 LWC F7, 0(F28)", "mips_asm", mips_machine)
        self.assertTrue(error.startswith(NOT_EVEN_REGISTER))

if __name__ == '__main__':
    main()
