import sys
import random
import string
sys.path.append("..")

import operator as opfunc
import functools
from assembler.virtual_machine import vmachine

from unittest import TestCase, main

from assembler.assemble import assemble
NUM_TESTS=1000

"""
Semi Unit Tests

Step through code until result happens.


At the moment test after the arithmetic instructions are
tested, as these tests depend on those.
"""
class TestControlFlow(TestCase):

    def test_jmp(self):
        test_code = """
                mov eax, 0
                jmp label
                dec eax
                label: inc eax
                """
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 1)


    def test_je(self):
        test_code = """
                mov eax, 0
                cmp eax, 0
                je label
                dec eax
                label: inc eax
                """
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 1)

        test_code = """
                mov eax, 1
                cmp eax, 0
                je label
                dec eax
                label: inc eax
                """
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 1)


    def test_jne(self):
        test_code = """
                mov eax, 0
                cmp eax, 0
                jne label
                dec eax
                label: inc eax
                """
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 0)

        test_code = """
                mov eax, 1
                cmp eax, 0
                jne label
                dec eax
                label: inc eax
                """
        assemble(test_code, vmachine)
        self.assertEqual(vmachine.registers["EAX"], 2)
"""
A thought for testing.

INTENDED RESULT
    { if Test_Label before JMP, then 1

1 MOV EAX, 0
2
3
4 Test_Label: INC EAX
5
6
7
8 JMP Test_Label
9 DEC EAX 
10 


INTENDED RESULT
    { if Test_Label after JMP, then 1

1 MOV EAX, 0
2
3 JMP Test_Label
4 
5
6 DEC EAX
7 DEC EAX
8
9 Test_Label: INC EAX
10 
*** ASSEMBLE ***

"""

if __name__ == '__main__':
    main()

