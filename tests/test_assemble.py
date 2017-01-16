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


if __name__ == '__main__':
    main()
