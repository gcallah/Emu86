#!/usr/bin/env python3
import sys
sys.path.append(".")
import random
import string

import operator as opfunc
import functools
from assembler.virtual_machine import mips_machine

from unittest import TestCase, main

from assembler.assemble import assemble
NUM_TESTS=1000

"""
Test entire programs.

tests/arithmetic_shift.asm  tests/data.asm  tests/gt.asm  tests/key_test.asm  tests/loop.asm  tests/power.asm  tests/test.asm  tests/test_control_flow.asm  tests/test_interrupt.asm
"""

class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open (filenm, "r") as prog:
            return prog.read()

    def run_mips_test_code (self, filnm):
        mips_machine.re_init()
        mips_machine.base = "hex"
        test_code = self.read_test_code("tests/MIPS_MML/" + filnm)
        assemble(test_code, 'mips_mml', mips_machine)

    def test_loop(self):
        self.run_mips_test_code("loop.asm")
        self.assertEqual(mips_machine.registers["R11"], 16)

    def test_power(self):
        self.run_mips_test_code("power.asm")
        self.assertEqual(mips_machine.registers["R8"], 65536)

    def test_gt(self):
        self.run_mips_test_code("gt.asm")
        self.assertEqual(mips_machine.registers["R8"], 17)
        self.assertEqual(mips_machine.registers["R9"], 16)
        self.assertEqual(mips_machine.registers["R13"], 16)
        self.assertEqual(mips_machine.registers["R14"], 19)

    # def test_interrupt(self):
    #     self.run_intel_test_code("tests/Intel/test_interrupt.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 71)
    #     self.assertEqual(intel_machine.registers["EBX"], 6)
    #     self.assertEqual(intel_machine.registers["ECX"], 1)
    #     self.assertEqual(intel_machine.registers["ESP"], 511)
    #     self.assertEqual(intel_machine.memory["6"], 71)

    # def test_key(self):
    #     self.run_intel_test_code("tests/Intel/key_test.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 71)
    #     self.assertEqual(intel_machine.registers["EBX"], 71)
    #     self.assertEqual(intel_machine.registers["ECX"], 1)
    #     self.assertEqual(intel_machine.registers["ESP"], 511)
    #     self.assertEqual(intel_machine.memory["9"], 83)

    def test_arithmetic_shift(self):
        self.run_mips_test_code("arithmetic_shift.asm")
        self.assertEqual(mips_machine.registers["R10"], 4)
        self.assertEqual(mips_machine.registers["R11"], 10)
        self.assertEqual(mips_machine.registers["R12"], 8)
        self.assertEqual(mips_machine.registers["R13"], 8)
        self.assertEqual(mips_machine.memory["4"], 4)

    # def test_jump(self):
    #     self.run_mips_test_code("tests/MIPS/test_jump.asm")
    #     self.assertEqual(mips_machine.registers["R8"], 3)

    def test_data(self):
        self.run_mips_test_code("data.asm")
        self.assertEqual(mips_machine.registers["R8"],  8)
        self.assertEqual(mips_machine.registers["R9"], 16)
        self.assertEqual(mips_machine.registers["R10"], 32)

    def test_array(self):
        self.run_mips_test_code("array.asm")
        self.assertEqual(mips_machine.registers["R8"],  3)
        self.assertEqual(mips_machine.registers["R9"], 50)

    def test_sum_calculation(self):
        self.run_mips_test_code("sum_test.asm")
        self.assertEqual(mips_machine.registers["R8"], 263)
        self.assertEqual(mips_machine.memory["24"], 263)

    def test_arithmetic_expression(self):
        self.run_mips_test_code("arithmetic_expression.asm")
        self.assertEqual(mips_machine.registers["R8"], -31)
        self.assertEqual(mips_machine.registers["R10"], 52)

    def test_area(self):
        self.run_mips_test_code("area.asm")
        self.assertEqual(mips_machine.registers["R8"], 35)
        self.assertEqual(mips_machine.registers["R9"], 27)
        self.assertEqual(mips_machine.registers["R10"], 35 * 27)
        self.assertEqual(mips_machine.registers["LO"], 35 * 27)
        self.assertEqual(mips_machine.registers["HI"], 0)
        self.assertEqual(mips_machine.memory["1000"], 35 * 27)

    def test_celsius_conversion(self):
        self.run_mips_test_code("cel_to_fah.asm")
        self.assertEqual(mips_machine.registers["R8"], 95)
        self.assertEqual(mips_machine.memory["100"], 95)
        self.assertEqual(mips_machine.registers["HI"], 2)
        self.assertEqual(mips_machine.registers["R9"], 5)

    def test_log(self):
        self.run_mips_test_code("log.asm")
        self.assertEqual(mips_machine.registers["R9"], 1024)
        self.assertEqual(mips_machine.registers["R8"], 9)

    # def test_mem_register(self):
    #     self.run_intel_test_code("tests/Intel/mem_register_test.asm")
    #     self.assertEqual(intel_machine.registers["EAX"], 6)
    #     self.assertEqual(intel_machine.memory["6"], 3)
    #     self.assertEqual(intel_machine.memory["8"], 8)
    #     self.assertEqual(intel_machine.memory["0"], 50)
    #     self.assertEqual(intel_machine.memory["1"], 32)

    # def test_array_avg(self):
    #     self.run_mips_test_code("tests/MIPS/array_average_test.asm")
    #     self.assertEqual(mips_machine.registers["R16"], 10)
    #     self.assertEqual(mips_machine.registers["R8"], 89)
    #     self.assertEqual(mips_machine.registers["R9"], 10)
    #     self.assertEqual(mips_machine.registers["R10"], 40)
    #     self.assertEqual(mips_machine.registers["R12"], 8)
    #     self.assertEqual(mips_machine.registers["R13"], 9)

    def test_int_square_root(self):
        self.run_mips_test_code("int_square_root.asm")
        self.assertEqual(mips_machine.registers["R8"], 10)

    # def test_add_to_array_elem_test(self):
    #     self.run_mips_test_code("tests/MIPS/change_array_elem_test.asm")
    #     self.assertEqual(mips_machine.registers["R8"], 361)
    #     self.assertEqual(mips_machine.registers["R13"], 361)
    #     self.assertEqual(mips_machine.registers["R17"], 10)
    #     self.assertEqual(mips_machine.registers["R9"], 40)
    #     self.assertEqual(mips_machine.registers["R10"], 10)

if __name__ == '__main__':
    main()
