#!/usr/bin/env python3
import sys
sys.path.append(".") # noqa

from assembler.virtual_machine import intel_machine

from unittest import TestCase, main

from assembler.assemble import assemble
"""
Test entire programs.

tests/tests_Intel/area.asm
tests/tests_Intel/arithmetic_expression.asm
tests/tests_Intel/array.asm
tests/tests_Intel/array_average_test.asm
tests/tests_Intel/cel_to_fah.asm
tests/tests_Intel/change_array_elem.asm
tests/tests_Intel/int_square_root.asm
tests/tests_Intel/log.asm
tests/tests_Intel/mem_register_test.asm
tests/tests_Intel/sum_test
tests/tests_Intel/arithmetic_shift.asm
tests/tests_Intel/data.asm
tests/tests_Intel/gt.asm
tests/tests_Intel/key_test.asm
tests/tests_Intel/loop.asm
tests/tests_Intel/power.asm
tests/tests_Intel/test.asm
tests/tests_Intel/test_interrupt.asm

"""

TEST_DIR_NAME = "tests/tests_Intel/"


class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open(filenm, "r") as prog:
            return prog.read()

    def run_intel_test_code(self, filnm):
        intel_machine.re_init()
        intel_machine.base = "dec"
        intel_machine.flavor = "intel"
        test_code = self.read_test_code(TEST_DIR_NAME + filnm)
        assemble(test_code, intel_machine)

    def test_loop(self):
        self.run_intel_test_code("loop.asm")
        self.assertEqual(intel_machine.registers["ECX"], 16)

    def test_power(self):
        self.run_intel_test_code("power.asm")
        self.assertEqual(intel_machine.registers["EDX"], 65536)

    def test_gt(self):
        self.run_intel_test_code("gt.asm")
        self.assertEqual(intel_machine.registers["EAX"], 17)
        self.assertEqual(intel_machine.registers["EBX"], 16)
        self.assertEqual(intel_machine.registers["ECX"], 16)
        self.assertEqual(intel_machine.registers["EDX"], 19)

    def test_interrupt(self):
        self.run_intel_test_code("test_interrupt.asm")
        self.assertEqual(intel_machine.registers["EAX"], 71)
        self.assertEqual(intel_machine.registers["EBX"], 6)
        self.assertEqual(intel_machine.registers["ECX"], 1)
        self.assertEqual(intel_machine.registers["ESP"], 511)
        self.assertEqual(intel_machine.memory["6"], 71)

    def test_key(self):
        self.run_intel_test_code("key_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 71)
        self.assertEqual(intel_machine.registers["EBX"], 71)
        self.assertEqual(intel_machine.registers["ECX"], 1)
        self.assertEqual(intel_machine.registers["ESP"], 511)
        self.assertEqual(intel_machine.memory["9"], 83)

    def test_arithmetic_shift(self):
        self.run_intel_test_code("arithmetic_shift.asm")
        self.assertEqual(intel_machine.registers["EAX"], 4)
        self.assertEqual(intel_machine.registers["EBX"], 10)
        self.assertEqual(intel_machine.registers["ECX"], 8)
        self.assertEqual(intel_machine.registers["EDX"], 8)
        self.assertEqual(intel_machine.memory["4"], 4)

    def test_jump(self):
        self.run_intel_test_code("test_jump.asm")
        self.assertEqual(intel_machine.registers["EAX"], 3)

    def test_data(self):
        self.run_intel_test_code("data.asm")
        self.assertEqual(intel_machine.registers["EAX"],  8)
        self.assertEqual(intel_machine.registers["EBX"], 16)
        self.assertEqual(intel_machine.registers["ECX"], 32)

    def test_array(self):
        self.run_intel_test_code("array.asm")
        self.assertEqual(intel_machine.registers["EAX"],  3)
        self.assertEqual(intel_machine.registers["EBX"], -50)
        self.assertEqual(intel_machine.registers["ECX"], ord('l'))
        self.assertEqual(intel_machine.registers["EDX"], 5)
        list_x = [3, 8, 5, 2]
        string_z = "hello"
        for position in range(0, 4):
            self.assertEqual(intel_machine.memory[str(position)],
                             list_x[position])
        for position in range(4, 17):
            mem_loc = (hex(position).split('x')[-1]).upper()
            self.assertEqual(intel_machine.memory[mem_loc], -50)
        for position in range(17, 22):
            mem_loc = (hex(position).split('x')[-1]).upper()
            self.assertEqual(intel_machine.memory[mem_loc],
                             ord(string_z[position - 17]))
        self.assertEqual(intel_machine.memory[hex(22).split('x')[-1]], 0)

    def test_sum_calculation(self):
        self.run_intel_test_code("sum_test.asm")
        self.assertEqual(intel_machine.registers["EAX"],  53)
        self.assertEqual(intel_machine.memory["1"], 53)

    def test_arithmetic_expression(self):
        self.run_intel_test_code("arithmetic_expression.asm")
        self.assertEqual(intel_machine.registers["EAX"],  -31)
        self.assertEqual(intel_machine.registers["EBX"],  52)

    def test_area(self):
        self.run_intel_test_code("area.asm")
        self.assertEqual(intel_machine.registers["EAX"], 945)

    def test_celsius_conversion(self):
        self.run_intel_test_code("cel_to_fah.asm")
        self.assertEqual(intel_machine.registers["EAX"], 95)
        self.assertEqual(intel_machine.memory["1"], 95)
        self.assertEqual(intel_machine.registers["EDX"], 2)
        self.assertEqual(intel_machine.registers["EBX"], 5)

    def test_log(self):
        self.run_intel_test_code("log.asm")
        self.assertEqual(intel_machine.registers["EAX"], 1024)
        self.assertEqual(intel_machine.registers["ECX"], 9)

    def test_mem_register(self):
        self.run_intel_test_code("mem_register_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 6)
        self.assertEqual(intel_machine.memory["6"], 3)
        self.assertEqual(intel_machine.memory["8"], 8)
        self.assertEqual(intel_machine.memory["0"], 50)
        self.assertEqual(intel_machine.memory["1"], 32)

    def test_array_avg(self):
        self.run_intel_test_code("array_average_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 9)
        self.assertEqual(intel_machine.registers["ECX"], 100)
        self.assertEqual(intel_machine.registers["EBX"], 100)
        self.assertEqual(intel_machine.registers["EDX"], 89)

    def test_int_square_root(self):
        self.run_intel_test_code("int_square_root.asm")
        self.assertEqual(intel_machine.registers["EAX"], 10)

    def test_add_to_array_elem_test(self):
        self.run_intel_test_code("change_array_elem_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 3331)
        self.assertEqual(intel_machine.registers["EDX"], 3331)
        self.assertEqual(intel_machine.registers["ECX"], 100)
        self.assertEqual(intel_machine.registers["EBX"], 100)

    def test_fp_sum(self):
        self.run_intel_test_code("fp_sum_test.asm")
        self.assertEqual(intel_machine.registers["ST0"], 16.6 + 128.4)
        self.assertEqual(intel_machine.registers["ST1"], 16.6)

    def test_fp_area(self):
        self.run_intel_test_code("fp_area.asm")
        self.assertAlmostEqual(intel_machine.registers["ST0"], 16.6 * 128.4)
        self.assertEqual(intel_machine.registers["ST1"], 16.6)

    def test_fp_cel_to_fah(self):
        self.run_intel_test_code("fp_cel_to_fah.asm")
        fah_val = 35.4 * 9 / 5 + 32
        self.assertAlmostEqual(intel_machine.registers["ST0"], fah_val)
        self.assertEqual(intel_machine.memory["1"], fah_val)

    def test_fp_power(self):
        self.run_intel_test_code("fp_power.asm")
        float_power_val = 14.8 ** 4
        self.assertAlmostEqual(intel_machine.registers["ST0"], float_power_val)


if __name__ == '__main__':
    main()
