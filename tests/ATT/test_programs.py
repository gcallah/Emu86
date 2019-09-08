#!/usr/bin/env python3
import sys
sys.path.append(".") # noqa

from assembler.virtual_machine import intel_machine

from unittest import TestCase, main

from assembler.assemble import assemble

"""
Test entire programs.

tests/ATT/area.asm
tests/ATT/arithmetic_expression.asm
tests/ATT/array.asm
tests/ATT/array_average_test.asm
tests/ATT/cel_to_fah.asm
tests/ATT/change_array_elem.asm
tests/ATT/int_square_root.asm
tests/ATT/log.asm
tests/ATT/mem_register_test.asm
tests/ATT/mov_extra_test.asm
tests/ATT/sum_test
tests/ATT/arithmetic_shift.asm
tests/ATT/data.asm
tests/ATT/gt.asm
tests/ATT/key_test.asm
tests/ATT/loop.asm
tests/ATT/power.asm
tests/ATT/test.asm
tests/ATT/test_interrupt.asm

"""


class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open(filenm, "r") as prog:
            return prog.read()

    def run_att_test_code(self, filnm):
        intel_machine.re_init()
        intel_machine.base = "dec"
        intel_machine.flavor = "att"
        test_code = self.read_test_code(filnm)
        assemble(test_code, intel_machine)

    def test_loop_att(self):
        self.run_att_test_code("tests/ATT/loop.asm")
        self.assertEqual(intel_machine.registers["ECX"], 16)

    def test_power_att(self):
        self.run_att_test_code("tests/ATT/power.asm")
        self.assertEqual(intel_machine.registers["EDX"], 65536)

    def test_gt_att(self):
        self.run_att_test_code("tests/ATT/gt.asm")
        self.assertEqual(intel_machine.registers["EAX"], 17)
        self.assertEqual(intel_machine.registers["EBX"], 16)
        self.assertEqual(intel_machine.registers["ECX"], 16)
        self.assertEqual(intel_machine.registers["EDX"], 19)

    def test_interrupt_att(self):
        self.run_att_test_code("tests/ATT/test_interrupt.asm")
        self.assertEqual(intel_machine.registers["EAX"], 71)
        self.assertEqual(intel_machine.registers["EBX"], 6)
        self.assertEqual(intel_machine.registers["ECX"], 1)
        self.assertEqual(intel_machine.registers["ESP"], 511)
        self.assertEqual(intel_machine.memory["6"], 71)

    def test_key_att(self):
        self.run_att_test_code("tests/ATT/key_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 71)
        self.assertEqual(intel_machine.registers["EBX"], 71)
        self.assertEqual(intel_machine.registers["ECX"], 1)
        self.assertEqual(intel_machine.registers["ESP"], 511)
        self.assertEqual(intel_machine.memory["9"], 83)

    def test_arithmetic_shift_att(self):
        self.run_att_test_code("tests/ATT/arithmetic_shift.asm")
        self.assertEqual(intel_machine.registers["EAX"], 4)
        self.assertEqual(intel_machine.registers["EBX"], 10)
        self.assertEqual(intel_machine.registers["ECX"], 8)
        self.assertEqual(intel_machine.registers["EDX"], 8)
        self.assertEqual(intel_machine.memory["4"], 4)

    def test_jump_att(self):
        self.run_att_test_code("tests/ATT/test_jump.asm")
        self.assertEqual(intel_machine.registers["EAX"], 3)

    def test_data_att(self):
        self.run_att_test_code("tests/ATT/data.asm")
        self.assertEqual(intel_machine.registers["EAX"], 8)
        self.assertEqual(intel_machine.registers["EBX"], 16)
        self.assertEqual(intel_machine.registers["ECX"], 32)

    def test_array_att(self):
        self.run_att_test_code("tests/ATT/array.asm")
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

    def test_sum_calculation_att(self):
        self.run_att_test_code("tests/ATT/sum_test.asm")
        self.assertEqual(intel_machine.registers["EAX"],  53)
        self.assertEqual(intel_machine.memory["1"], 53)

    def test_arithmetic_expression_att(self):
        self.run_att_test_code("tests/ATT/arithmetic_expression.asm")
        self.assertEqual(intel_machine.registers["EAX"],  -31)
        self.assertEqual(intel_machine.registers["EBX"],  52)

    def test_area_att(self):
        self.run_att_test_code("tests/ATT/area.asm")
        self.assertEqual(intel_machine.registers["EAX"],  35 * 27)

    def test_celsius_conversion_att(self):
        self.run_att_test_code("tests/ATT/cel_to_fah.asm")
        self.assertEqual(intel_machine.registers["EAX"], 95)
        self.assertEqual(intel_machine.registers["EDX"], 2)
        self.assertEqual(intel_machine.registers["EBX"], 5)

    def test_log_att(self):
        self.run_att_test_code("tests/ATT/log.asm")
        self.assertEqual(intel_machine.registers["EAX"], 1024)
        self.assertEqual(intel_machine.registers["ECX"], 9)

    def test_mem_register_att(self):
        self.run_att_test_code("tests/ATT/mem_register_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 6)
        self.assertEqual(intel_machine.registers["EBX"], 0)
        self.assertEqual(intel_machine.registers["ECX"], 4)
        self.assertEqual(intel_machine.memory["6"], 3)
        self.assertEqual(intel_machine.memory["8"], 8)
        self.assertEqual(intel_machine.memory["0"], 50)
        self.assertEqual(intel_machine.memory["D"], 32)
        self.assertEqual(intel_machine.memory["10"], 5)
        self.assertEqual(intel_machine.memory["1C"], 5)
        self.assertEqual(intel_machine.memory["28"], 5)

    def test_array_avg_att(self):
        self.run_att_test_code("tests/ATT/array_average_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 9)
        self.assertEqual(intel_machine.registers["ECX"], 100)
        self.assertEqual(intel_machine.registers["EBX"], 100)
        self.assertEqual(intel_machine.registers["EDX"], 89)

    def test_int_square_root_att(self):
        self.run_att_test_code("tests/ATT/int_square_root.asm")
        self.assertEqual(intel_machine.registers["EAX"], 10)

    def test_add_to_array_elem_test_att(self):
        self.run_att_test_code("tests/ATT/change_array_elem_test.asm")
        self.assertEqual(intel_machine.registers["EAX"], 3331)
        self.assertEqual(intel_machine.registers["EDX"], 3331)
        self.assertEqual(intel_machine.registers["ECX"], 100)
        self.assertEqual(intel_machine.registers["EBX"], 100)

    def test_mov_extra_att(self):
        self.run_att_test_code("tests/ATT/mov_extra_test.asm")
        self.assertEqual(intel_machine.memory["0"], 104)
        self.assertEqual(intel_machine.memory["2"], 24931098)
        self.assertEqual(intel_machine.memory["3"], 10000)


if __name__ == '__main__':
    main()
    pass
