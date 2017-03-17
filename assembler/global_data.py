"""
Our x86 global data.
"""

from collections import OrderedDict

MEM_DIGITS = 2
MEM_SIZE = 32

class GlobalData:
    """
    Holds the memory, registers, flags, etc. that our assembly code
    will use. A singleton class.
    """
    def __init__(self):
        # the x86 registers
        self.registers = OrderedDict(
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
        self.flags = OrderedDict(
                    [
                        ('CF', 0),
                        ('OF', 0),
                        ('SF', 0),
                        ('ZF', 0),
                    ])
        
        self.memory = OrderedDict()
        self.mem_init()

    def mem_init(self):
        for i in range(0, MEM_SIZE):
                self.memory[str(i)] = 0

    def re_init(self):
        for reg in self.registers:
            self.registers[reg] = 0
        for flag in self.flags:
            self.flags[flag] = 0
        self.mem_init()
        

gdata = GlobalData()
