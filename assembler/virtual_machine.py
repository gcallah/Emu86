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
INSTR_PTR_INTEL = "EIP"
INSTR_PTR_MIPS = "PC"
STACK_PTR_INTEL = "ESP"
STACK_PTR_MIPS = "R29"

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
        
        self.memory = OrderedDict()
        self.mem_init()

        self.stack = OrderedDict()
        self.stack_init()

        self.labels = {}
        self.symbols = {}
        self.flavor = None
        self.data_init = "on"


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
        for flag in self.flags:
            self.flags[flag] = 0
        self.mem_init()
        self.stack_init()
        self.data_init = "on"

    def empty_cell(self):
        return EMPTY_CELL

    def get_data_init(self):
        return self.data_init

    def set_data_init(self, on_or_off):
        self.data_init = on_or_off

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
                        (STACK_PTR_INTEL, STACK_TOP),
                        ('EBP', 0),
                        (INSTR_PTR_INTEL, 0),
                    ])

        self.unwritable = [INSTR_PTR_INTEL, STACK_PTR_INTEL]

        # for now we only need four of the flags
        self.flags = OrderedDict(
                    [
                        ('CF', 0),
                        ('OF', 0),
                        ('SF', 0),
                        ('ZF', 0),
                    ])

    def re_init(self):
        super().re_init()
        self.registers[STACK_PTR_INTEL] = STACK_TOP

    def inc_ip(self):
        ip = self.get_ip()
        ip += 1
        self.set_ip(ip)
    
    def set_ip(self, val):
        self.registers[INSTR_PTR_INTEL] = val
    
    def get_ip(self):
        return int(self.registers[INSTR_PTR_INTEL])

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

        self.registers[STACK_PTR_INTEL] = val
    
    def get_sp(self):
        return int(self.registers[STACK_PTR_INTEL])


class MIPSMachine(VirtualMachine):
    def __init__(self):
        super().__init__()
        self.unwritable = [INSTR_PTR_MIPS, 'R0', 
                           STACK_PTR_MIPS, 'HI', 'LO']
        self.registers = OrderedDict(
                    [
                        ('R0', 0),
                        ('R12', 0),
                        ('R24', 0),
                        ('R1', 0),
                        ('R13', 0),
                        ('R25', 0),
                        ('R2', 0),
                        ('R14', 0),
                        ('R26', 0),
                        ('R3', 0),
                        ('R15', 0),
                        ('R27', 0),
                        ('R4', 0),
                        ('R16', 0),
                        ('R28', 0),
                        ('R5', 0),
                        ('R17', 0),
                        ('R29', STACK_TOP),
                        ('R6', 0),
                        ('R18', 0),
                        ('R30', 0),
                        ('R7', 0),
                        ('R19', 0),
                        ('R31', 0),
                        ('R8', 0),
                        ('R20', 0),
                        ('LO', 0),
                        ('R20', 0),
                        ('R9', 0),
                        ('R21', 0),
                        ('HI', 0),
                        ('R10', 0),
                        ('R22', 0),
                        (INSTR_PTR_MIPS, 0),
                        ('R11', 0),
                        ('R23', 0),
                    ])

        self.flags = OrderedDict(
                    [
                        ('ZF', 0),
                    ])
    def re_init(self):
        super().re_init()
        self.registers[STACK_PTR_MIPS] = STACK_TOP

    def inc_ip(self):
        ip = self.get_ip()
        ip += 4
        self.set_ip(ip)
    
    def set_ip(self, val):
        self.registers[INSTR_PTR_MIPS] = val
    
    def get_ip(self):
        return int(self.registers[INSTR_PTR_MIPS])

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

        self.registers[STACK_PTR_MIPS] = val
    
    def get_sp(self):
        return int(self.registers[STACK_PTR_MIPS])

intel_machine = IntelMachine()
mips_machine = MIPSMachine()
