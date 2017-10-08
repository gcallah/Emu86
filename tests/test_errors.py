#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append("..")


from unittest import TestCase, main

from assembler.global_data import gdata, STACK_BOTTOM, STACK_TOP
from assembler.assemble import assemble
# UNKNOWN_ERR should NOT show up, so we won't write a test case for it.
from assembler.errors import UNKNOWN_ERR, INVALID_INSTR, INVALID_OPRND
from assembler.errors import INVALID_NUM_ARGS, INVALID_MEM_LOC, INVALID_REG
from assembler.errors import REG_UNWRITABLE, STACK_OVERFLOW, STACK_UNDERFLOW
from assembler.errors import UNKNOWN_NM


class ErrorTestCase(TestCase):

    def test_invalid_instr(self):
        (output, error) = assemble("shove_up_reg eax, 1", gdata)
        self.assertTrue(error.startswith(INVALID_INSTR))

    def test_invalid_mem_loc(self):
        (output, error) = assemble("mov [hell], 666", gdata)
        self.assertTrue(error.startswith(INVALID_MEM_LOC))

    def test_invalid_num_args(self):
        (output, error) = assemble("add eax, 10, 22, 34", gdata)
        self.assertTrue(error.startswith(INVALID_NUM_ARGS))

    def test_unknown_name(self):
        (output, error) = assemble("add fred, wilma", gdata)
        self.assertTrue(error.startswith(UNKNOWN_NM))

    def test_reg_unwritable(self):
        (output, error) = assemble("mov EIP, 10", gdata)
        self.assertTrue(error.startswith(REG_UNWRITABLE))

    def test_stack_overflow(self):
        gdata.registers["ESP"] = STACK_BOTTOM-1
        (output, error) = assemble("push 1", gdata)
        self.assertTrue(error.startswith(STACK_OVERFLOW))

    def test_stack_underflow(self):
        gdata.registers["ESP"] = STACK_TOP
        (output, error) = assemble("pop ebx", gdata)
        self.assertTrue(error.startswith(STACK_UNDERFLOW))

if __name__ == '__main__':
    main()
