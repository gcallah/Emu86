"""
Our x86 global data.
"""

from collections import OrderedDict

from .errors import StackOverflow, StackUnderflow

MEM_DIGITS = 2

MEM_SIZE = 32
STACK_TOP = (MEM_SIZE * 2) - 1
STACK_BOTTOM = MEM_SIZE

INSTR_PTR = "EIP"
STACK_PTR = "ESP"

class GlobalData:
    """
    Holds the memory, registers, flags, etc. that our assembly code
    will use. A singleton class.
    """
    def __init__(self):
        # the x86 registers
        self.nxt_key = 0
        self.ret_str = "Some keys for int 22 to return."
        self.debug = ""
    
        self.unwritable = [INSTR_PTR, STACK_PTR]

        self.registers = OrderedDict(
                    [
                        ('EAX', 0),
                        ('EBX', 0),
                        ('ECX', 0),
                        ('EDX', 0),
                        ('ESI', 0),
                        ('EDI', 0),
                        (STACK_PTR, STACK_TOP),
                        ('EBP', 0),
                        (INSTR_PTR, 0),
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

        self.stack = OrderedDict()
        self.stack_init()

    def mem_init(self):
        for i in range(0, MEM_SIZE):
            self.memory[str(i)] = 0

    def stack_init(self):
        for i in range(STACK_TOP, STACK_BOTTOM - 1, -1):
            self.stack[str(i)] = 0

    def re_init(self):
        self.nxt_key = 0
        self.ip = 0
        for reg in self.registers:
            self.registers[reg] = 0
        # one gets a unique value:
        self.registers[STACK_PTR] = STACK_TOP
        for flag in self.flags:
            self.flags[flag] = 0
        self.mem_init()
        self.stack_init()
        
    def inc_ip(self):
        ip = self.get_ip()
        ip += 1
        self.set_ip(ip)
    
    def set_ip(self, val):
        self.registers[INSTR_PTR] = val
    
    def get_ip(self):
        return int(self.registers[INSTR_PTR])
        
    def inc_sp(self):
        sp = self.get_sp()
        sp += 1
        self.set_sp(sp)
        
    def dec_sp(self):
        sp = self.get_sp()
        sp -= 1
        self.set_sp(sp)
    
    def set_sp(self, val):
        if val > STACK_BOTTOM:
            raise StackOverflow()
        if val < STACK_TOP:
            raise StackUnderflow()

        self.registers[STACK_PTR] = val
    
    def get_sp(self):
        return int(self.registers[STACK_PTR])


gdata = GlobalData()
