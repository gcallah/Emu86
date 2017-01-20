"""
Test our assembly interpreter.
"""

import sys
sys.path.append("..")


from unittest import TestCase, main

from Emu86.global_data import registers, flags, memory
from Emu86.assemble import assemble


class AssembleTestCase(TestCase):

    def test_mov(self):
        assemble("mov eax, 1", registers, memory, flags)
        self.assertEqual(registers["EAX"], 1)

    def test_add(self):
        registers["EAX"] = 2
        registers["EBX"] = 4
        assemble("add eax, ebx", registers, memory, flags)
        self.assertEqual(registers["EAX"], 6)

    def test_sub(self):
        registers["EAX"] = 2
        registers["EBX"] = 4
        assemble("sub eax, ebx", registers, memory, flags)
        self.assertEqual(registers["EAX"], -2)

    def test_imul(self):
        registers["EAX"] = 2
        registers["EBX"] = 4
        assemble("imul eax, ebx", registers, memory, flags)
        self.assertEqual(registers["EAX"], 8)

    def test_and(self):
        registers["EAX"] = 2
        registers["EBX"] = 3
        assemble("and eax, ebx", registers, memory, flags)
        self.assertEqual(registers["EAX"], 2)

    def test_or(self):
        registers["EAX"] = 2
        registers["EBX"] = 3
        assemble("or eax, ebx", registers, memory, flags)
        self.assertEqual(registers["EAX"], 3)
        
if __name__ == '__main__':
    main()
