"""
Our x86 virtual machine representation.
"""

from collections import OrderedDict

from .errors import StackOverflow, StackUnderflow

MEM_DIGITS = 2

MEM_SIZE = 256
STACK_TOP = (MEM_SIZE * 2) - 1
STACK_BOTTOM = MEM_SIZE
# STACK_TOP = MEM_SIZE - 1
# STACK_BOTTOM = 0
EMPTY_CELL = 0
INSTR_PTR = "EIP"
STACK_PTR = "ESP"

class VirtualMachine:
    """
    Holds the memory, registers, flags, etc. that our assembly code
    will use. A singleton class.
    """
    def __init__(self):
        # the x86 registers
        self.nxt_key = 0
        self.ret_str = "GIRONAGIRONAGETSGETS"
        self.debug = ""
    
        self.unwritable = [INSTR_PTR, STACK_PTR]
        
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

        self.labels = {}
        self.symbols = {}
        self.flavor = None


    def __str__(self):
        return ("Registers: " + str(self.registers) + "\n"
                + "Flags: " + str(self.flags) + "\n"
                + "Memory: " + str(self.memory) + "\n"
                + "Stack: " + str(self.stack) + "\n"
                + "Labels: " + str(self.labels))

    def mem_init(self):
        for i in range(0, MEM_SIZE):
            self.memory[hex(i).split('x')[-1].upper()] = 0

    def stack_init(self):
        for i in range(STACK_TOP, STACK_BOTTOM - 1, -1):
            self.stack[hex(i).split('x')[-1].upper()] = 0

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
        self.flavor = None
        
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
        if val < STACK_BOTTOM - 1:
            raise StackOverflow()
        if val > STACK_TOP:
            raise StackUnderflow()

        self.registers[STACK_PTR] = val
    
    def get_sp(self):
        return int(self.registers[STACK_PTR])

    def empty_cell(self):
        return EMPTY_CELL

class IntelMachine(VirtualMachine):
    def __init__(self):
        super().__init__()
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


class MIPSMachine(VirtualMachine):
    def __init__(self):
        super().__init__()
        self.registers = OrderedDict(
                    [
                        ('V0', 0),
                        ('V1', 0),
                        ('A0', 0),
                        ('A1', 0),
                        ('A2', 0),
                        ('A3', 0),
                        ('T0', 0),
                        ('T1', 0),
                        ('T2', 0),
                        ('T3', 0),
                        ('T4', 0),
                        ('T5', 0),
                        ('T6', 0),
                        ('T7', 0),
                        ('T8', 0),
                        ('T9', 0),
                        ('S0', 0),
                        ('S1', 0),
                        ('S2', 0),
                        ('S3', 0),
                        ('S4', 0),
                        ('S5', 0),
                        ('S6', 0),
                        ('S7', 0),
                        ('K0', 0),
                        ('K1', 0)
                    ])

vmachine = IntelMachine()
mips_machine = MIPSMachine()
