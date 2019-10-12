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
FLOAT_STACK_LIMIT = 8
EMPTY_CELL = 0
INSTR_PTR_INTEL = "EIP"
INSTR_PTR_MIPS = "PC"
INSTR_PTR_RISCV = "PC"
STACK_PTR_INTEL = "ESP"
STACK_PTR_MIPS = "R29"
STACK_PTR_RISCV = "X2"


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
        self.labels_init()

        self.symbols = OrderedDict()
        self.symbols_init()

        self.c_stack = []
        self.cstack_init()

        self.flavor = None
        self.data_init = "on"
        self.start_ip = 0
        self.changes = set()
        self.base = None
        self.stack_change = ""
        self.next_stack_change = ""

    def __str__(self):
        return ("Registers: " + str(self.registers) + "\n"
                + "Flags: " + str(self.flags) + "\n"
                + "Memory: " + str(self.memory) + "\n"
                + "Stack: " + str(self.stack) + "\n"
                + "Labels: " + str(self.labels))

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
        self.changes_init()
        self.symbols_init()
        self.labels_init()
        self.cstack_init()
        self.stack_change = ""
        self.next_stack_change = ""

    def mem_init(self):
        self.memory.clear()

    def changes_init(self):
        self.changes.clear()

    def symbols_init(self):
        self.symbols.clear()

    def labels_init(self):
        self.labels.clear()

    def cstack_init(self):
        del self.c_stack[:]

    def order_mem(self):
        lst = []
        for key in self.memory:
            lst.append(key)
        for hex_key in range(0, len(lst)):
            lst[hex_key] = int(lst[hex_key], 16)
        lst.sort()
        sorted_mem = OrderedDict()
        for decimal_key in lst:
            hex_sorted_key = hex(decimal_key).split('x')[-1].upper()
            sorted_mem[hex_sorted_key] = self.memory[hex_sorted_key]
        self.memory = sorted_mem

    def empty_cell(self):
        return EMPTY_CELL

    def get_data_init(self):
        return self.data_init

    def set_data_init(self, on_or_off):
        self.data_init = on_or_off


class IntelMachine(VirtualMachine):
    def __init__(self):
        super().__init__()
        # self.fp_stack_registers = OrderedDict(
        #             [
        #                 ('ST7', 0.0),
        #                 ('ST6', 0.0),
        #                 ('ST5', 0.0),
        #                 ('ST4', 0.0),
        #                 ('ST3', 0.0),
        #                 ('ST2', 0.0),
        #                 ('ST1', 0.0),
        #                 ('ST0', 0.0),
        #             ])
        self.float_stack_bottom = -1

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
                        ('ST0', 0.0),
                        ('ST1', 0.0),
                        ('ST2', 0.0),
                        ('ST3', 0.0),
                        ('ST4', 0.0),
                        ('ST5', 0.0),
                        ('ST6', 0.0),
                        ('ST7', 0.0),
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

    def is_FP_stack_empty(self):
        return self.float_stack_bottom == -1

    def is_FP_stack_full(self):
        return self.float_stack_bottom == FLOAT_STACK_LIMIT - 1

    def push_to_Float_Stack(self, val):
        if self.float_stack_bottom == -1:
            self.registers["ST0"] = val
        else:
            for i in range(self.float_stack_bottom + 1, 0, -1):
                self.registers[f'ST{i}'] = self.registers[f'ST{i - 1}']
            self.registers["ST0"] = val
        self.float_stack_bottom += 1
        self.changes.add('ST0')

    def get_register_at_float_stack_top(self):
        return "ST"+str(self.float_stack_top)

    def get_float_stack_register_at_offset(self, k):
        return "ST" + str((self.float_stack_top + k) % FLOAT_STACK_LIMIT)

    def pop_from_Float_Stack(self):
        curr_value_float_stack_top = self.registers['ST0']
        for i in range(0, self.float_stack_bottom):
            self.registers[f'ST{i}'] = self.registers[f'ST{i + 1}']
        self.registers[f'ST{self.float_stack_bottom}'] = 0.0
        self.float_stack_bottom -= 1
        return curr_value_float_stack_top

    def get_next_register(self):
        self.float_stack_top = (self.float_stack_top - 1) % FLOAT_STACK_LIMIT
        return self.float_stack_top

    def reset_FP_Stack(self):
        self.float_stack_bottom = -1
        for i in range(FLOAT_STACK_LIMIT):
            self.registers["ST"+str(i)] = 0.0

    def re_init(self):
        super().re_init()
        self.reset_FP_Stack()
        self.registers[STACK_PTR_INTEL] = STACK_TOP

    def stack_init(self):
        for i in range(STACK_TOP, STACK_BOTTOM - 1, -1):
            self.stack[hex(i).split('x')[-1].upper()] = 0

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
        self.unwritable = [INSTR_PTR_MIPS, 'R0', 'F0', 'F29',
                           STACK_PTR_MIPS, 'HI', 'LO']
        rRegisterList = ['R0', 'R12', 'R24', 'R1', 'R13', 'R25','R2', 'R14', 'R26', 'R3', 'R15', 'R27','R4', 'R16', 'R28', 'R5', 'R17', 'R29','R6', 'R18', 'R30', 'R7', 'R19', 'R31', 'R8', 'R20', 'R9', 'R21', 'HI', 'R10', 'R22', 'R22', 'LO', 'R11', 'R23']
        fRegisterList = ['F0','F12','F24','F1','F13','F25','F2','F14','F26','F3','F15','F27','F4','F16','F28','F5','F17','F29','F6','F18','F30','F7','F19','F31','F8','F20','F9','F21','F10','F22','F11','F23']

        registerList = []

        for rRegister in rRegisterList:
            registerList.append((rRegister, 0))
        registerList.append((INSTR_PTR_MIPS, 0))
        for rRegister in fRegisterList:
            registerList.append((rRegister, 0))

        self.registers = OrderedDict(list)

        self.flags = OrderedDict(
                    [
                        ('COND', 0),
                    ])

    def re_init(self):
        super().re_init()
        self.registers[STACK_PTR_MIPS] = STACK_TOP
        self.changes.clear()

    def stack_init(self):
        for i in range(STACK_TOP - 3, STACK_BOTTOM - 1, -4):
            self.stack[hex(i).split('x')[-1].upper()] = 0

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


class RISCVMachine(VirtualMachine):
    # make sure to account for the lack of HI and LO in display

    def __init__(self):
        super().__init__()
        self.unwritable = [INSTR_PTR_RISCV, 'X0', STACK_PTR_RISCV]
        self.registers = OrderedDict(
                        [
                            ('X0', 0),
                            ('X11', 0),
                            ('X22', 0),
                            ('X1', 0),
                            ('X12', 0),
                            ('X23', 0),
                            ('X2', 0),
                            ('X13', 0),
                            ('X24', 0),
                            ('X3', 0),
                            ('X14', 0),
                            ('X25', 0),
                            ('X4', 0),
                            ('X15', 0),
                            ('X26', 0),
                            ('X5', 0),
                            ('X16', 0),
                            ('X27', 0),
                            ('X6', 0),
                            ('X17', 0),
                            ('X28', 0),
                            ('X7', 0),
                            ('X18', 0),
                            ('X29', 0),
                            ('X8', 0),
                            ('X19', 0),
                            ('X30', 0),
                            ('X9', 0),
                            ('X20', 0),
                            ('X31', 0),
                            ('X10', 0),
                            ('X21', 0),
                            (INSTR_PTR_RISCV, 0)
                        ])
        self.flags = OrderedDict(
                    [
                        ('COND', 0),
                    ])

    def re_init(self):
        super().re_init()
        self.registers[STACK_PTR_RISCV] = STACK_TOP
        self.changes.clear()

    def stack_init(self):
        for i in range(STACK_TOP - 3, STACK_BOTTOM - 1, -4):
            self.stack[hex(i).split('x')[-1].upper()] = 0

    def inc_ip(self):
        ip = self.get_ip()
        ip += 4
        self.set_ip(ip)

    def set_ip(self, val):
        self.registers[INSTR_PTR_RISCV] = val

    def get_ip(self):
        return int(self.registers[INSTR_PTR_RISCV])

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

        self.registers[STACK_PTR_RISCV] = val

    def get_sp(self):
        return int(self.registers[STACK_PTR_RISCV])


class WASMMachine(VirtualMachine):
    def __init__(self):
        super().__init__()
        self.locals = OrderedDict()
        self.locals_init()

        self.globals = OrderedDict()
        self.globals_init()

        self.stack_ptr = STACK_BOTTOM
        self.ip = 0

    def re_init(self):
        self.nxt_key = 0
        self.ip = 0
        self.mem_init()
        self.stack_init()
        self.data_init = "on"
        self.changes_init()
        self.symbols_init()
        self.labels_init()
        self.cstack_init()
        self.locals_init()
        self.globals_init()
        self.stack_change = ""
        self.next_stack_change = ""
        self.stack_ptr = STACK_BOTTOM

    def locals_init(self):
        self.locals.clear()

    def globals_init(self):
        self.globals.clear()

    def stack_init(self):
        for i in range(STACK_TOP - 3, STACK_BOTTOM - 1, -4):
            self.stack[hex(i).split('x')[-1].upper()] = 0

    def inc_sp(self):
        sp = self.get_sp()
        sp += 4
        self.set_sp(sp)

    def dec_sp(self):
        sp = self.get_sp()
        sp -= 4
        self.set_sp(sp)

    def set_sp(self, val):
        if val < STACK_BOTTOM - 1:
            raise StackOverflow()
        if val > STACK_TOP:
            raise StackUnderflow()

        self.stack_ptr = val

    def get_sp(self):
        return self.stack_ptr

    def inc_ip(self):
        ip = self.get_ip()
        ip += 1
        self.set_ip(ip)

    def set_ip(self, val):
        self.ip = val

    def get_ip(self):
        return self.ip


intel_machine = IntelMachine()
mips_machine = MIPSMachine()
riscv_machine = RISCVMachine()
wasm_machine = WASMMachine()
