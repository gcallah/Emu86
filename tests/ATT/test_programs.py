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

    def run_att_test_code (self, filnm):
        vmachine.re_init()
        test_code = self.read_test_code(filnm)
        assemble(test_code, 'att', vmachine)

    def test_loop_att(self):
        self.run_att_test_code("tests/ATT/loop_att.asm")
        self.assertEqual(vmachine.registers["ECX"], 16)

    def test_power_att(self):
        self.run_att_test_code("tests/ATT/power_att.asm")
        self.assertEqual(vmachine.registers["EDX"], 65536)

    def test_gt_att(self):
        self.run_att_test_code("tests/ATT/gt_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 17)
        self.assertEqual(vmachine.registers["EBX"], 16)
        self.assertEqual(vmachine.registers["ECX"], 16)
        self.assertEqual(vmachine.registers["EDX"], 19)

    def test_interrupt_att(self):
        self.run_att_test_code("tests/ATT/test_interrupt_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 71)
        self.assertEqual(vmachine.registers["EBX"], 6)
        self.assertEqual(vmachine.registers["ECX"], 1)
        self.assertEqual(vmachine.registers["ESP"], 511)
        self.assertEqual(vmachine.memory["6"], 71)

    def test_key_att(self):
        self.run_att_test_code("tests/ATT/key_test_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 71)
        self.assertEqual(vmachine.registers["EBX"], 71)
        self.assertEqual(vmachine.registers["ECX"], 1)
        self.assertEqual(vmachine.registers["ESP"], 511)
        self.assertEqual(vmachine.memory["9"], 83)

    def test_arithmetic_shift_att(self):
        self.run_att_test_code("tests/ATT/arithmetic_shift_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 4)
        self.assertEqual(vmachine.registers["EBX"], 10)
        self.assertEqual(vmachine.registers["ECX"], 8)
        self.assertEqual(vmachine.registers["EDX"], 8)
        self.assertEqual(vmachine.memory["4"], 4)

    def test_jump_att(self):
        self.run_att_test_code("tests/ATT/test_jump_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 3)

    def test_data_att(self):
        self.run_att_test_code("tests/ATT/data_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 8)
        self.assertEqual(vmachine.registers["EBX"], 16)
        self.assertEqual(vmachine.registers["ECX"], 32)

    def test_array_att(self):
        self.run_att_test_code("tests/ATT/array_att.asm")
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

    def test_sum_calculation_att(self):
        self.run_att_test_code("tests/ATT/sum_test_att.asm")
        self.assertEqual(vmachine.registers["EAX"],  53)
        self.assertEqual(vmachine.memory["1"], 53)

    def test_arithmetic_expression_att(self):
        self.run_att_test_code("tests/ATT/arithmetic_expression_att.asm")
        self.assertEqual(vmachine.registers["EAX"],  -31)
        self.assertEqual(vmachine.registers["EBX"],  52)

    def test_area_att(self):
        self.run_att_test_code("tests/ATT/area_att.asm")
        self.assertEqual(vmachine.registers["EAX"],  35 * 27)

    def test_celsius_conversion_att(self):
        self.run_att_test_code("tests/ATT/cel_to_fah_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 95)
        self.assertEqual(vmachine.registers["EDX"], 2)
        self.assertEqual(vmachine.registers["EBX"], 5)

    def test_log_att(self):
        self.run_att_test_code("tests/ATT/log_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 1024)
        self.assertEqual(vmachine.registers["ECX"], 9)

    def test_mem_register_att(self):
        self.run_att_test_code("tests/ATT/mem_register_test_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 6)
        self.assertEqual(vmachine.memory["6"], 3)
        self.assertEqual(vmachine.memory["8"], 8)
        self.assertEqual(vmachine.memory["0"], 50)
        self.assertEqual(vmachine.memory["1"], 32)

    def test_array_avg_att(self):
        self.run_att_test_code("tests/ATT/array_average_test_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 9)
        self.assertEqual(vmachine.registers["ECX"], 100)
        self.assertEqual(vmachine.registers["EBX"], 100)
        self.assertEqual(vmachine.registers["EDX"], 89)

    def test_int_square_root_att(self):
        self.run_att_test_code("tests/ATT/int_square_root_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 10)

    def test_add_to_array_elem_test_att(self):
        self.run_att_test_code("tests/ATT/change_array_elem_test_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 3331)
        self.assertEqual(vmachine.registers["EDX"], 3331)
        self.assertEqual(vmachine.registers["ECX"], 100)
        self.assertEqual(vmachine.registers["EBX"], 100)

    def test_reg_mem_addition_att(self):
        self.run_att_test_code("tests/ATT/reg_mem_addition_test_att.asm")
        self.assertEqual(vmachine.registers["EAX"], 6)
        self.assertEqual(vmachine.registers["EBX"], 0)
        self.assertEqual(vmachine.registers["ECX"], 3)
        self.assertEqual(vmachine.memory["6"], 3)
        self.assertEqual(vmachine.memory["8"], 8)
        self.assertEqual(vmachine.memory["0"], 50)
        self.assertEqual(vmachine.memory["D"], 32)
        self.assertEqual(vmachine.memory["F"], 5)
        self.assertEqual(vmachine.memory["1B"], 5)
        self.assertEqual(vmachine.memory["24"], 5)


if __name__ == '__main__':
    main()
