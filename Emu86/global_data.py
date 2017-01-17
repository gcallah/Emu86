"""
Our x86 global data.
"""

from collections import OrderedDict

MEM_DIGITS = 2
MEM_SIZE = 32

# the x86 registers
registers = OrderedDict(
            [
                ('EAX', 0),
                ('EBX', 0),
                ('ECX', 0),
                ('EDX', 0),
                ('ESI', 0),
                ('EDI', 0),
                ('ESP', 0),
                ('EBP', 0),
            ])

# for now we only need four of the flags
flags = OrderedDict(
            [
                ('CF', 0),
                ('OF', 0),
                ('SF', 0),
                ('ZF', 0),
            ])

memory = OrderedDict()
for i in range(0, MEM_SIZE):
        memory[str(i)] = 0
