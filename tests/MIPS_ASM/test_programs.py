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

# for floating point to binary and back
import struct
import codecs
import binascii

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
        test_code = self.read_test_code("tests/MIPS_ASM/" + filnm)
        assemble(test_code, 'mips_asm', mips_machine)

    # def convert_hex_float(self, string):
    #     lst = string.split(".")
    #     int_part = int(lst[0], 16)
    #     float_part = float("." + lst[1])
    #     return int_part + float_part

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

    def test_jump(self):
        self.run_mips_test_code("test_jump.asm")
        self.assertEqual(mips_machine.registers["R8"], 3)

    def test_data(self):
        self.run_mips_test_code("data.asm")
        self.assertEqual(mips_machine.registers["R8"],  8)
        self.assertEqual(mips_machine.registers["R9"], 16)
        self.assertEqual(mips_machine.registers["R10"], 32)

    def test_array(self):
        self.run_mips_test_code("array.asm")
        self.assertEqual(mips_machine.registers["R8"],  3)
        self.assertEqual(mips_machine.registers["R9"], 50)
        self.assertEqual(mips_machine.registers["R10"], ord ('l'))
        self.assertEqual(mips_machine.registers["R11"], 5)

    def test_sum_calculation(self):
        self.run_mips_test_code("sum_test.asm")
        self.assertEqual(mips_machine.registers["R8"],  53)
        self.assertEqual(mips_machine.memory["4"], 53)

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

    def test_celsius_conversion(self):
        self.run_mips_test_code("cel_to_fah.asm")
        self.assertEqual(mips_machine.registers["R8"], 95)
        self.assertEqual(mips_machine.memory["4"], 95)
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

    def test_array_avg(self):
        self.run_mips_test_code("array_average_test.asm")
        self.assertEqual(mips_machine.registers["R16"], 10)
        self.assertEqual(mips_machine.registers["R8"], 89)
        self.assertEqual(mips_machine.registers["R9"], 10)
        self.assertEqual(mips_machine.registers["R10"], 40)
        self.assertEqual(mips_machine.registers["R12"], 8)
        self.assertEqual(mips_machine.registers["R13"], 9)

    def test_int_square_root(self):
        self.run_mips_test_code("int_square_root.asm")
        self.assertEqual(mips_machine.registers["R8"], 10)

    def test_add_to_array_elem_test(self):
        self.run_mips_test_code("change_array_elem_test.asm")
        self.assertEqual(mips_machine.registers["R8"], 361)
        self.assertEqual(mips_machine.registers["R13"], 361)
        self.assertEqual(mips_machine.registers["R17"], 10)
        self.assertEqual(mips_machine.registers["R9"], 40)
        self.assertEqual(mips_machine.registers["R10"], 10)

    ########################
    ##### FP TEST BELOW ####
    ########################
    def convertHiLoForFP(self):
        h_reg = str(mips_machine.registers["HI"])
        for i in range(0, 32-len(h_reg)):
            h_reg = "0" + h_reg
        l_reg = str(mips_machine.registers["LO"])
        for i in range(0, 32-len(l_reg)):
            l_reg = "0" + l_reg

        binary_result = h_reg + l_reg
        hex_result = hex(int(binary_result, 2))[2:]
        for i in range(0, 16-len(hex_result)):
            hex_result = "0"+hex_result
        bin_data = codecs.decode(hex_result, "hex")
        result = struct.unpack("d", bin_data)[0]
        return result

    # def float_to_hex(f):
    #     return hex(struct.unpack('<I', struct.pack('<f', f))[0])
    def float_to_hex(self, f):
        return binascii.hexlify(struct.pack('d', f))

    #loading data
    def test_fp_data(self):
        self.run_mips_test_code("fp_data.asm")
        self.assertEqual(mips_machine.registers["F8"],  8.0)
        self.assertEqual(mips_machine.registers["F9"], 10.5)
        self.assertEqual(mips_machine.registers["F10"], 20.555)

    # power function
    def test_fp_power(self):
        self.run_mips_test_code("fp_power.asm")
        self.assertEqual(mips_machine.registers["F8"], 166.375)

    #area function
    # def test_fp_area(self):
    #     self.run_mips_test_code("fp_area.asm")
    #     a = 12.2
    #     b = 12.5
    #     # ah = self.float_to_hex(a)
    #     # bh = self.float_to_hex(b)
    #     self.assertEqual(mips_machine.registers["F8"], a)
    #     self.assertEqual(mips_machine.registers["F9"], b)

    #     result = self.convertHiLoForFP()

    #     correct = a*b
    #     self.assertEqual(result, correct)



if __name__ == '__main__':
    main()
