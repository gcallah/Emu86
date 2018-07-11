#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append(".")


from unittest import TestCase, main

from assembler.virtual_machine import mips_machine, STACK_BOTTOM, STACK_TOP
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
from assembler.errors import UNKNOWN_ERR, INVALID_INSTR, INVALID_OPRND
from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, INVALID_REG
from assembler.errors import MISSING_COMMA, MISSING_DATA, INVALID_TOKEN
from assembler.errors import REG_UNWRITABLE, STACK_OVERFLOW, STACK_UNDERFLOW
from assembler.errors import UNKNOWN_NM


class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        (output, error) = assemble("shove_up_reg $t4, 1", 'mips', mips_machine)
        self.assertTrue(error.startswith(INVALID_INSTR))

    def test_invalid_mem_loc(self):
        (output, error) = assemble("sw $t3, 3(hell)", 'mips', mips_machine)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_invalid_num_args(self):
        (output, error) = assemble("addi $t4, 10, 22, 34", 'mips', mips_machine)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

# we have to clear up symbol handling to make this test work.
#    def test_unknown_name(self):
#        (output, error) = assemble("add fred, wilma", vmachine)
#        self.assertTrue(error.startswith(UNKNOWN_NM))

    def test_reg_unwritable(self):
        (output, error) = assemble("addi $zero, $s2, 10", 'mips', mips_machine)
        self.assertTrue(error.startswith(REG_UNWRITABLE))

    def test_comma_error(self):
        (output, error) = assemble("subi $t5 $t5 1", 'mips', mips_machine)
        self.assertTrue(error.startswith(MISSING_COMMA))

    def test_comma_error(self):
        (output, error) = assemble("ori $t5,,,, 1", 'mips', mips_machine)
        self.assertTrue(error.startswith(INVALID_TOKEN))

    def test_data_error(self):
        (output, error) = assemble(".data \n  x: .word", 'mips', mips_machine)
        self.assertTrue(error.startswith(MISSING_DATA))


if __name__ == '__main__':
    main()
