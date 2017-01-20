"""
Test our assembly interpreter.
"""

import sys
sys.path.append("..")


from unittest import TestCase, main

from Emu86.global_data import gdata
from Emu86.assemble import assemble


class AssembleTestCase(TestCase):

    def test_mov(self):
        assemble("mov eax, 1", gdata)
        self.assertEqual(gdata.registers["EAX"], 1)

    def test_add(self):
        gdata.registers["EAX"] = 2
        gdata.registers["EBX"] = 4
        assemble("add eax, ebx", gdata)
        self.assertEqual(gdata.registers["EAX"], 6)

    def test_sub(self):
        gdata.registers["EAX"] = 2
        gdata.registers["EBX"] = 4
        assemble("sub eax, ebx", gdata)
        self.assertEqual(gdata.registers["EAX"], -2)

    def test_imul(self):
        gdata.registers["EAX"] = 2
        gdata.registers["EBX"] = 4
        assemble("imul eax, ebx", gdata)
        self.assertEqual(gdata.registers["EAX"], 8)

    def test_and(self):
        gdata.registers["EAX"] = 27
        assemble("and eax, 23", gdata)
        self.assertEqual(gdata.registers["EAX"], 19)

    def test_or(self):
        gdata.registers["EAX"] = 2
        gdata.registers["EBX"] = 3
        assemble("or eax, ebx", gdata)
        self.assertEqual(gdata.registers["EAX"], 3)
        
if __name__ == '__main__':
    main()
