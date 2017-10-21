#!/usr/bin/env python3
import sys
import random
import string
sys.path.append("..")

from assembler.virtual_machine import vmachine, STACK_TOP, STACK_BOTTOM
from unittest import TestCase, main
from assembler.assemble import assemble, MAX_INSTRUCTIONS
from assembler.tokens import MAX_INT, MIN_INT


FIRST_INST_ADDRESS = 1
NUM_TESTS=1000

class TestControlFlow(TestCase):


    def test_jmp(self):
        """
        Jump to a random location from 0 to MAX_INSTRUCTIONS.
        Assert IP is set to that location by jump.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_loc
            assemble("jmp test_label", vmachine)
            self.assertEqual(vmachine.get_ip(), label_loc)


    def test_je(self):
        """
        Jump iff zero flag is 1.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_loc
            zero_flag = random.getrandbits(1)
            vmachine.flags["ZF"] = zero_flag
            assemble("je test_label", vmachine)
            if(zero_flag):
                self.assertEqual(vmachine.get_ip(), label_loc)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_jne(self):
        """
        Jump iff zero flag is 0.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_loc
            zero_flag = random.getrandbits(1)
            vmachine.flags["ZF"] = zero_flag
            assemble("jne test_label", vmachine)
            if(not zero_flag):
                self.assertEqual(vmachine.get_ip(), label_loc)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_jg(self):
        """
        Jump iff both sign flag and zero flag are 0.
        """
        for i in range(NUM_TESTS):
          vmachine.re_init()
          label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
          vmachine.labels["test_label"] = label_loc
          sign_flag = random.getrandbits(1)
          zero_flag = random.getrandbits(1)
          vmachine.flags["SF"] = sign_flag
          vmachine.flags["ZF"] = zero_flag
          assemble("jg test_label", vmachine)
          if((not zero_flag) and (not sign_flag)):
            self.assertEqual(vmachine.get_ip(), label_loc)
          else:
            self.assertEqual(vmachine.get_ip(), 1)
       
    def test_jge(self):
        """
        Jump iff sign flag is 0.
        """
        for i in range(NUM_TESTS):
          vmachine.re_init()
          label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
          vmachine.labels["test_label"] = label_loc
          sign_flag = random.getrandbits(1)
          vmachine.flags["SF"] = sign_flag
          assemble("jge test_label", vmachine)
          if(not sign_flag):
            self.assertEqual(vmachine.get_ip(), label_loc)
          else:
            self.assertEqual(vmachine.get_ip(), 1)


    def test_jl(self):
        """
        Jump iff sign flag is 1.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_loc
            sign_flag = random.getrandbits(1)
            vmachine.flags["SF"] = sign_flag
            assemble("jl test_label", vmachine)
            if(sign_flag):
                self.assertEqual(vmachine.get_ip(), label_loc)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_jle(self):
        """
        Jump iff either sign flag or zero flag are 1.
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_loc
            sign_flag = random.getrandbits(1)
            zero_flag = random.getrandbits(1)
            vmachine.flags["SF"] = sign_flag
            vmachine.flags["ZF"] = zero_flag
            assemble("jle test_label", vmachine)
            if(zero_flag or sign_flag):
                self.assertEqual(vmachine.get_ip(), label_loc)
            else:
                self.assertEqual(vmachine.get_ip(), 1)

    def test_call(self):
        """
        
        """
        for i in range(NUM_TESTS):
            vmachine.re_init()
            ip_before_jump = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.set_ip(ip_before_jump)
            label_loc = random.randint(FIRST_INST_ADDRESS,MAX_INSTRUCTIONS)
            vmachine.labels["test_label"] = label_loc
            assemble("call test_label", vmachine)
            print(i)
            self.assertEqual(vmachine.get_ip(), label_loc)
            self.assertEqual(vmachine.stack[str(STACK_TOP)], ip_before_jump)

if __name__ == '__main__':
    main()

