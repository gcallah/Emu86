#!/usr/bin/env python3
import sys
import random
sys.path.append(".") # noqa

from assembler.virtual_machine import intel_machine
from unittest import TestCase, main
from assembler.assemble import assemble, MAX_INSTRUCTIONS

FIRST_INST_ADDRESS = 1
# Edge case (yet to deal with): for the below instructions,
# jumping around the 1000th instruction.
NUM_TESTS = 100
NO_OP = "mov eax, eax\n"
TEST_LABEL = "test_label"


class TestControlFlow(TestCase):

    def test_jmp(self):
        """
        Jump to a random location from 1 to MAX_INSTRUCTIONS.
        Assert IP is set to that location by jump.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            assemble("jmp test_label", 'intel', intel_machine)
            self.assertEqual(intel_machine.get_ip(), label_addr)

    def test_je(self):
        """
        Jump iff zero flag is 1.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            zero_flag = random.getrandbits(1)
            intel_machine.flags["ZF"] = zero_flag
            assemble("je test_label", 'intel', intel_machine)
            if(zero_flag):
                self.assertEqual(intel_machine.get_ip(), label_addr)
            else:
                self.assertEqual(intel_machine.get_ip(), 1)

    def test_jne(self):
        """
        Jump iff zero flag is 0.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            zero_flag = random.getrandbits(1)
            intel_machine.flags["ZF"] = zero_flag
            assemble("jne test_label", 'intel', intel_machine)
            if(not zero_flag):
                self.assertEqual(intel_machine.get_ip(), label_addr)
            else:
                self.assertEqual(intel_machine.get_ip(), 1)

    def test_jg(self):
        """
        Jump iff both sign flag and zero flag are 0.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            sign_flag = random.getrandbits(1)
            zero_flag = random.getrandbits(1)
            intel_machine.flags["SF"] = sign_flag
            intel_machine.flags["ZF"] = zero_flag
            assemble("jg test_label", 'intel', intel_machine)
            if((not zero_flag) and (not sign_flag)):
                self.assertEqual(intel_machine.get_ip(), label_addr)
            else:
                self.assertEqual(intel_machine.get_ip(), 1)

    def test_jge(self):
        """
        Jump iff sign flag is 0.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            sign_flag = random.getrandbits(1)
            intel_machine.flags["SF"] = sign_flag
            assemble("jge test_label", 'intel', intel_machine)
            if(not sign_flag):
                self.assertEqual(intel_machine.get_ip(), label_addr)
            else:
                self.assertEqual(intel_machine.get_ip(), 1)

    def test_jl(self):
        """
        Jump iff sign flag is 1.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            sign_flag = random.getrandbits(1)
            intel_machine.flags["SF"] = sign_flag
            assemble("jl test_label", 'intel', intel_machine)
            if(sign_flag):
                self.assertEqual(intel_machine.get_ip(), label_addr)
            else:
                self.assertEqual(intel_machine.get_ip(), 1)

    def test_jle(self):
        """
        Jump iff either sign flag or zero flag are 1.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            intel_machine.labels["test_label"] = label_addr
            sign_flag = random.getrandbits(1)
            zero_flag = random.getrandbits(1)
            intel_machine.flags["SF"] = sign_flag
            intel_machine.flags["ZF"] = zero_flag
            assemble("jle test_label", 'intel', intel_machine)
            if(zero_flag or sign_flag):
                self.assertEqual(intel_machine.get_ip(), label_addr)
            else:
                self.assertEqual(intel_machine.get_ip(), 1)

    def test_call(self):
        """
        Tests call.

        At the time of writing this test,
        blank lines are skipped by the tokenizer.
        In order to have emu jump to the location of label_addr,
        we have to makeno-op lines to assign the correct locations
        to the lines we test.
        """
        for i in range(NUM_TESTS):
            intel_machine.re_init()
            intel_machine.base = "dec"
            call_instr_addr = random.randint(FIRST_INST_ADDRESS,
                                             MAX_INSTRUCTIONS)
            label_addr = random.randint(FIRST_INST_ADDRESS,
                                        MAX_INSTRUCTIONS)

            code_to_run = [NO_OP] * (MAX_INSTRUCTIONS + 1)
            code_to_run[call_instr_addr] = "call " + TEST_LABEL + "\n"
            prev_label_info = code_to_run[label_addr]
            code_to_run[label_addr] = TEST_LABEL + ": " + prev_label_info

            intel_machine.labels[TEST_LABEL] = label_addr
            intel_machine.set_ip(call_instr_addr)

            # We step once through the code, executing only `call`.
            assemble("".join(code_to_run), 'intel', intel_machine, step=True)

            self.assertEqual(intel_machine.get_ip(), label_addr)


if __name__ == '__main__':
    main()
