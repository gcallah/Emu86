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

tests/arithmetic_shift.asm  tests/data.asm  tests/gt.asm  tests/key_test.asm  tests/loop.asm  tests/power.asm  tests/test.asm  tests/test_control_flow.asm  tests/test_interrupt.asm
"""

class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open (filenm, "r") as prog:
            return prog.read()

    def run_intel_test_code (self, filnm):
        vmachine.re_init()
        test_code = self.read_test_code(filnm)
        assemble(test_code, 'intel', vmachine)

    def run_att_test_code (self, filnm):
        vmachine.re_init()
        test_code = self.read_test_code(filnm)
        assemble(test_code, 'att', vmachine)

    def test_loop(self):
        self.run_intel_test_code("tests/Intel/loop.asm")
        self.assertEqual(vmachine.registers["ECX"], 16)

    def test_power(self):
        self.run_intel_test_code("tests/Intel/power.asm")
        self.assertEqual(vmachine.registers["EDX"], 65536)

    def test_gt(self):
        self.run_intel_test_code("tests/Intel/gt.asm")
        self.assertEqual(vmachine.registers["EAX"], 17)
        self.assertEqual(vmachine.registers["EBX"], 16)
        self.assertEqual(vmachine.registers["ECX"], 16)
        self.assertEqual(vmachine.registers["EDX"], 19)

    def test_interrupt(self):
        self.run_intel_test_code("tests/Intel/test_interrupt.asm")
        self.assertEqual(vmachine.registers["EAX"], 71)
        self.assertEqual(vmachine.registers["EBX"], 6)
        self.assertEqual(vmachine.registers["ECX"], 1)
        self.assertEqual(vmachine.registers["ESP"], 511)
        self.assertEqual(vmachine.memory["6"], 71)

    def test_key(self):
        self.run_intel_test_code("tests/Intel/key_test.asm")
        self.assertEqual(vmachine.registers["EAX"], 71)
        self.assertEqual(vmachine.registers["EBX"], 71)
        self.assertEqual(vmachine.registers["ECX"], 1)
        self.assertEqual(vmachine.registers["ESP"], 511)
        self.assertEqual(vmachine.memory["9"], 83)

    def test_arithmetic_shift(self):
        self.run_intel_test_code("tests/Intel/arithmetic_shift.asm")
        self.assertEqual(vmachine.registers["EAX"], 4)
        self.assertEqual(vmachine.registers["EBX"], 10)
        self.assertEqual(vmachine.registers["ECX"], 8)
        self.assertEqual(vmachine.registers["EDX"], 8)
        self.assertEqual(vmachine.memory["4"], 4)

    def test_jump(self):
        self.run_intel_test_code("tests/Intel/test_jump.asm")
        self.assertEqual(vmachine.registers["EAX"], 3)

    def test_data(self):
        self.run_intel_test_code("tests/Intel/data.asm")
        self.assertEqual(vmachine.registers["EAX"],  8)
        self.assertEqual(vmachine.registers["EBX"], 16)
        self.assertEqual(vmachine.registers["ECX"], 32)

    def test_array(self):
        self.run_intel_test_code("tests/Intel/array.asm")
        self.assertEqual(vmachine.registers["EAX"],  3)
        self.assertEqual(vmachine.registers["EBX"], -50)
        self.assertEqual(vmachine.registers["ECX"], ord ('l'))
        self.assertEqual(vmachine.registers["EDX"], 5)
        list_x = [3, 8, 5, 2]
        string_z = "hello"
        for position in range(0, 4):
            self.assertEqual(vmachine.memory[str(position)], list_x[position])
        for position in range(4, 17):
            self.assertEqual(vmachine.memory[(hex(position).split('x')
                                             [-1]).upper()], -50)
        for position in range(17, 22):
            self.assertEqual(vmachine.memory[(hex(position).split('x')
                                             [-1]).upper()], 
                             ord(string_z[position - 17]))
        self.assertEqual(vmachine.memory[hex(22).split('x')[-1]], 0)

    def test_sum_calculation(self):
        self.run_intel_test_code("tests/Intel/sum_test.asm")
        self.assertEqual(vmachine.registers["EAX"],  53)
        self.assertEqual(vmachine.memory["1"], 53)

    def test_arithmetic_expression(self):
        self.run_intel_test_code("tests/Intel/arithmetic_expression.asm")
        self.assertEqual(vmachine.registers["EAX"],  -31)
        self.assertEqual(vmachine.registers["EBX"],  52)

    def test_area(self):
        self.run_intel_test_code("tests/Intel/area.asm")
        self.assertEqual(vmachine.registers["EAX"],  35 * 27)

    def test_celsius_conversion(self):
        self.run_intel_test_code("tests/Intel/cel_to_fah.asm")
        self.assertEqual(vmachine.registers["EAX"], 95)
        self.assertEqual(vmachine.registers["EDX"], 2)
        self.assertEqual(vmachine.registers["EBX"], 5)

    def test_log(self):
        self.run_intel_test_code("tests/Intel/log.asm")
        self.assertEqual(vmachine.registers["EAX"], 1024)
        self.assertEqual(vmachine.registers["ECX"], 9)

    def test_mem_register(self):
        self.run_intel_test_code("tests/Intel/mem_register_test.asm")
        self.assertEqual(vmachine.registers["EAX"], 6)
        self.assertEqual(vmachine.memory["6"], 3)
        self.assertEqual(vmachine.memory["8"], 8)
        self.assertEqual(vmachine.memory["0"], 50)
        self.assertEqual(vmachine.memory["1"], 32)

    def test_array_avg(self):
        self.run_intel_test_code("tests/Intel/array_average_test.asm")
        self.assertEqual(vmachine.registers["EAX"], 9)
        self.assertEqual(vmachine.registers["ECX"], 100)
        self.assertEqual(vmachine.registers["EBX"], 100)
        self.assertEqual(vmachine.registers["EDX"], 89)

    def test_int_square_root(self):
        self.run_intel_test_code("tests/Intel/int_square_root.asm")
        self.assertEqual(vmachine.registers["EAX"], 10)

    def test_add_to_array_elem_test(self):
        self.run_intel_test_code("tests/Intel/change_array_elem_test.asm")
        self.assertEqual(vmachine.registers["EAX"], 3331)
        self.assertEqual(vmachine.registers["EDX"], 3331)
        self.assertEqual(vmachine.registers["ECX"], 100)
        self.assertEqual(vmachine.registers["EBX"], 100)

if __name__ == '__main__':
    main()
