#!/usr/bin/env python3
import sys
sys.path.append("..")
import random
import string

import operator as opfunc
import functools
from assembler.virtual_machine import vmachine

from unittest import TestCase, main

from assembler.assemble import assemble
NUM_TESTS=1000

"""
Test entire programs.
"""
class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open (filenm, "r") as prog:
            return prog.read()

    def test_loop(self):
        test_code = self.read_test_code("tests/loop.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["ECX"], 16)

    def test_power(self):
        test_code = self.read_test_code("tests/power.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 65536)

if __name__ == '__main__':
    main()

