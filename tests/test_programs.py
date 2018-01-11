#!/usr/bin/env python3
import sys
sys.path.append(".")
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
        vmachine.re_init()
        test_code = self.read_test_code("tests/loop.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["ECX"], 16)

    def test_power(self):
        vmachine.re_init()
        test_code = self.read_test_code("tests/power.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EDX"], 65536)

    def test_gt(self):
        vmachine.re_init()
        test_code = self.read_test_code("tests/gt.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 17)
        self.assertEqual(vmachine.registers["EBX"], 16)
        self.assertEqual(vmachine.registers["ECX"], 16)
        self.assertEqual(vmachine.registers["EDX"], 19)

    def test_interrupt(self):
        vmachine.re_init()
        test_code = self.read_test_code("tests/test_interrupt.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 71)
        self.assertEqual(vmachine.registers["EBX"], 6)
        self.assertEqual(vmachine.registers["ECX"], 1)
        self.assertEqual(vmachine.registers["ESP"], 63)
        self.assertEqual(vmachine.memory["6"], 71)

    def test_key(self):
        vmachine.re_init()
        test_code = self.read_test_code("tests/key_test.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 71)
        self.assertEqual(vmachine.registers["EBX"], 71)
        self.assertEqual(vmachine.registers["ECX"], 1)
        self.assertEqual(vmachine.registers["ESP"], 63)
        self.assertEqual(vmachine.memory["9"], 83)

    def test_arithmetic_shift(self):
        vmachine.re_init()
        test_code = self.read_test_code("tests/arithmetic_shift.asm")
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 4)
        self.assertEqual(vmachine.registers["EBX"], 10)
        self.assertEqual(vmachine.registers["ECX"], 8)
        self.assertEqual(vmachine.registers["EDX"], 8)
        self.assertEqual(vmachine.memory["4"], 4)
       
        
if __name__ == '__main__':
    main()

