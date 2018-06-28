#!/usr/bin/env python3
import sys
import random
import string
sys.path.append(".")

from assembler.virtual_machine import vmachine, STACK_TOP, STACK_BOTTOM
from unittest import TestCase, main
from assembler.assemble import assemble, MAX_INSTRUCTIONS
from assembler.tokens import MAX_INT, MIN_INT

FIRST_INST_ADDRESS = 1
# Edge case (yet to deal with): for the below instructions,
# jumping around the 1000th instruction.
NUM_TESTS = 100
NO_OP = "mov %eax, %eax\n"
TEST_LABEL = "test_label"

class TestControlFlow(TestCase):


    def test_jmp(self):
        """
        Jump to a random location from 1 to MAX_INSTRUCTIONS.
        Assert IP is set to that location by jump.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_addr
            assemble("jmp test_label", 'att', vmachine)
            self.assertEqual(vmachine.get_ip(), label_addr)


    def test_je(self):
        """
        Jump iff zero flag is 1.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_addr
            zero_flag = random.getrandbits(1)
            vmachine.flags["ZF"] = zero_flag
            assemble("je test_label", 'att', vmachine)
            if(zero_flag):
                self.assertEqual(vmachine.get_ip(), label_addr)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_jne(self):
        """
        Jump iff zero flag is 0.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_addr
            zero_flag = random.getrandbits(1)
            vmachine.flags["ZF"] = zero_flag
            assemble("jne test_label", 'att', vmachine)
            if(not zero_flag):
                self.assertEqual(vmachine.get_ip(), label_addr)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_jg(self):
        """
        Jump iff both sign flag and zero flag are 0.
        """
        for i in range(NUM_TESTS):
          vmachine.re_init()
          label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
          vmachine.labels["test_label"] = label_addr
          sign_flag = random.getrandbits(1)
          zero_flag = random.getrandbits(1)
          vmachine.flags["SF"] = sign_flag
          vmachine.flags["ZF"] = zero_flag
          assemble("jg test_label", 'att', vmachine)
          if((not zero_flag) and (not sign_flag)):
            self.assertEqual(vmachine.get_ip(), label_addr)
          else:
            self.assertEqual(vmachine.get_ip(), 1)
       
    def test_jge(self):
        """
        Jump iff sign flag is 0.
        """
        for i in range(NUM_TESTS):
          vmachine.re_init()
          label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
          vmachine.labels["test_label"] = label_addr
          sign_flag = random.getrandbits(1)
          vmachine.flags["SF"] = sign_flag
          assemble("jge test_label", 'att', vmachine)
          if(not sign_flag):
            self.assertEqual(vmachine.get_ip(), label_addr)
          else:
            self.assertEqual(vmachine.get_ip(), 1)


    def test_jl(self):
        """
        Jump iff sign flag is 1.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_addr
            sign_flag = random.getrandbits(1)
            vmachine.flags["SF"] = sign_flag
            assemble("jl test_label", 'att', vmachine)
            if(sign_flag):
                self.assertEqual(vmachine.get_ip(), label_addr)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_jle(self):
        """
        Jump iff either sign flag or zero flag are 1.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_addr = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_addr
            sign_flag = random.getrandbits(1)
            zero_flag = random.getrandbits(1)
            vmachine.flags["SF"] = sign_flag
            vmachine.flags["ZF"] = zero_flag
            assemble("jle test_label", 'att', vmachine)
            if(zero_flag or sign_flag):
                self.assertEqual(vmachine.get_ip(), label_addr)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_call(self):
        """
        Tests call. 

        At the time of writing this test, blank lines are skipped by the tokenizer.
        In order to have emu jump to the location of label_addr, we have to make
        no-op lines to assign the correct locations to the lines we test.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            call_instr_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)
            label_addr = random.randint(FIRST_INST_ADDRESS, MAX_INSTRUCTIONS)

            code_to_run = [NO_OP] * (MAX_INSTRUCTIONS + 1)
            code_to_run[call_instr_addr] = "call " + TEST_LABEL + "\n"
            code_to_run[label_addr] = TEST_LABEL + ": " + code_to_run[label_addr]

            vmachine.labels[TEST_LABEL] = label_addr
            vmachine.set_ip(call_instr_addr)

            # We step once through the code, executing only `call`.
            assemble("".join(code_to_run), 'att', vmachine, step=True)

            self.assertEqual(vmachine.get_ip(), label_addr)

if __name__ == '__main__':
    main()

