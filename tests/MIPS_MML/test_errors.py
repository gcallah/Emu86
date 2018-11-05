#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
sys.path.append(".") # noqa


from unittest import TestCase, main

from assembler.virtual_machine import mips_machine
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
# from assembler.errors import UNKNOWN_ERR, INVALID_INSTR, INVALID_OPRND
# from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, INVALID_REG
# from assembler.errors import MISSING_COMMA, MISSING_DATA, INVALID_TOKEN
# from assembler.errors import REG_UNWRITABLE, STACK_OVERFLOW, STACK_UNDERFLOW
# from assembler.errors import UNKNOWN_NM, MISSING_PC, INT_OUT_OF_RNG

from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, MISSING_COMMA
from assembler.errors import INVALID_TOKEN, REG_UNWRITABLE, INT_OUT_OF_RNG


class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 shove_up_reg R8, 1",
                                             'mips_mml', mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_invalid_mem_loc(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 SW R10, 3(hell)",
                                             'mips_mml', mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_invalid_num_args(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ADDI R10, 10, 22, 34",
                                             'mips_mml', mips_machine)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

# we have to clear up symbol handling to make this test work.
#    def test_unknown_name(self):
#        (output, error) = assemble("add fred, wilma", vmachine)
#        self.assertTrue(error.startswith(UNKNOWN_NM))

    def test_reg_unwritable(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ADDI R0, R8, 10",
                                             'mips_mml', mips_machine)
        self.assertTrue(error.startswith(REG_UNWRITABLE))

    def test_comma_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 SUBI R8 R8 1", 'mips_mml',
                                             mips_machine)
        self.assertTrue(error.startswith(MISSING_COMMA))

    def test_comma_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ORI R10,,,, 1", 'mips_mml',
                                             mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_data_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble(".data \n  x: .word", 'mips_mml',
                                             mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def pc_data_error(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("R8, R8, 1", 'mips_mml',
                                             mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_mem_error_less(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 SW R10, -3(R28)",
                                             'mips_mml', mips_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_out_of_range(self):
        mips_machine.base = "hex"
        (output, error, bit_code) = assemble("40000 ADDI R8, R8, 100000000",
                                             'mips_mml', mips_machine)
        self.assertTrue(error.startswith(INT_OUT_OF_RNG))


if __name__ == '__main__':
    main()
