#!/usr/bin/env python3
import sys
sys.path.append(".") # noqa

from assembler.virtual_machine import wasm_machine

from unittest import TestCase, main

from assembler.assemble import assemble


class TestPrograms(TestCase):

    def read_test_code(self, filenm):
        with open(filenm, "r") as prog:
            return prog.read()

    def run_wasm_test_code(self, filnm):
        wasm_machine.re_init()
        wasm_machine.base = "dec"
        wasm_machine.flavor = "wasm"
        test_code = self.read_test_code(filnm)
        assemble(test_code, wasm_machine)

    def test_sum_calculation(self):
        self.run_wasm_test_code("tests/WASM/sum_test.asm")
        self.assertEqual(wasm_machine.globals['number'], -105)
        self.assertEqual(wasm_machine.stack['100'],  53)

    def test_area(self):
        self.run_wasm_test_code("tests/WASM/area.asm")
        self.assertEqual(wasm_machine.locals["area"], 945)
        self.assertEqual(wasm_machine.locals["length"], 35)
        self.assertEqual(wasm_machine.locals["width"], 27)


if __name__ == '__main__':
    main()
