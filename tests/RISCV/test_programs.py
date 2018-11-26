#!/usr/bin/env python3
import sys
sys.path.append(".") # noqa

from assembler.virtual_machine import riscv_machine

from unittest import TestCase, main

from assembler.assemble import assemble
NUM_TESTS = 1000

"""
Test entire programs.

tests/RISV/sum_test.asm
"""


class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open(filenm, "r") as prog:
            return prog.read()

    def run_riscv_test_code(self, filnm):
        riscv_machine.re_init()
        riscv_machine.base = "hex"
        test_code = self.read_test_code("tests/RISCV/" + filnm)
        assemble(test_code, 'riscv', riscv_machine)

    def test_sum_calculation(self):
        self.run_riscv_test_code("sum_test.asm")
        self.assertEqual(riscv_machine.registers["X8"], 53)
        self.assertEqual(riscv_machine.memory["4"], 53)

    def test_arithmetic_expression(self):
        self.run_riscv_test_code("arithmetic_expression.asm")
        self.assertEqual(riscv_machine.registers["X8"], -31)
        self.assertEqual(riscv_machine.registers["X10"], 52)

    def test_array(self):
        self.run_riscv_test_code("array.asm")
        self.assertEqual(riscv_machine.registers["X8"],  3)
        self.assertEqual(riscv_machine.registers["X9"], 50)
        self.assertEqual(riscv_machine.registers["X10"], ord('l'))
        self.assertEqual(riscv_machine.registers["X11"], 5)

    def test_loop(self):
        self.run_riscv_test_code("loop.asm")
        self.assertEqual(riscv_machine.registers["X11"], 16)

    def test_add_to_array_elem_test(self):
        self.run_riscv_test_code("change_array_elem_test.asm")
        self.assertEqual(riscv_machine.registers["X8"], 361)
        self.assertEqual(riscv_machine.registers["X13"], 361)
        self.assertEqual(riscv_machine.registers["X17"], 10)
        self.assertEqual(riscv_machine.registers["X9"], 40)
        self.assertEqual(riscv_machine.registers["X10"], 10)


if __name__ == '__main__':
    main()
