"""
Our x86 virtual machine representation.
"""

from collections import OrderedDict

from .errors import StackOverflow, StackUnderflow, InvalidArgument
from .MIPS.control_flow import Jal, Jr
from .MIPS.key_words import op_func_codes

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

# Why are these the right values?
MIPS_INTERRUPT_IP = 2147484032
RISC_INTERRUPT_IP = 470351872


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
        self.ip_div = 1
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

    def get_ip_div(self):
        return self.ip_div

    def get_start_ip(self):
        return self.start_ip

    def get_ip(self):
        pass

    def set_ip(self):
        pass

    def past_last_instr(self, token_lines):
        curr_ip = self.get_ip() - self.start_ip
        if curr_ip // self.get_ip_div() >= len(token_lines):
            return True
        return False

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

    def jump_to_label(self, label, source, jal=False):
        if label in self.labels:
            ip = self.labels[label]
            self.set_ip(ip + self.start_ip)
            self.next_stack_change = label
            return (True, source, "")
        else:
            try:
                ip = int(label)
                if jal:
                    ip = ip >> 2
                self.set_ip(ip)
                return (True, source, "")
            except Exception:
                return (False, source, f"Invalid label: {label}")

    def jump_handler(self, brk, source, instr_line):
        pass

    def exec_instr(self, instr_line):
        pass

    def create_bit_instr(self, instr_lst):
        return ''

    def set_next_stack_change(self):
        for label in self.labels:
            if self.get_ip() == self.labels[label]:
                self.next_stack_change = label


class IntelMachine(VirtualMachine):
    def __init__(self):
        super().__init__()

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
        self.instr = 0
        self.ops = 1

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

    def set_int_ip(self):
        pass

    def get_ip(self):
        return int(self.registers[INSTR_PTR_INTEL])

    def inc_sp(self, line_num):
        sp = self.get_sp()
        sp += 1
        self.set_sp(sp, line_num)

    def dec_sp(self, line_num):
        sp = self.get_sp()
        sp -= 1
        self.set_sp(sp, line_num)

    def set_sp(self, val, line_num):
        if val < STACK_BOTTOM - 1:
            raise StackOverflow(line_num)
        if val > STACK_TOP:
            raise StackUnderflow(line_num)

        self.registers[STACK_PTR_INTEL] = val

    def get_sp(self):
        return int(self.registers[STACK_PTR_INTEL])

    def jump_handler(self, brk, source, instr_line=None):
        return self.jump_to_label(brk.label, source, True)

    def exec_instr(self, instr_line, line_num):
        self.inc_ip()
        return instr_line[self.instr].f(instr_line[self.ops:], self, line_num)


class MIPSMachine(VirtualMachine):
    """
    Create a VM for running MIPS assembler.
    Why isn't flavor set here?
    """
    def __init__(self):
        super().__init__()
        self.ip_div = 4
        self.unwritable = [INSTR_PTR_MIPS, 'R0', 'F0', 'F29',
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
                        ('R29', 0),
                        ('R6', 0),
                        ('R18', 0),
                        ('R30', 0),
                        ('R7', 0),
                        ('R19', 0),
                        ('R31', 0),
                        ('R8', 0),
                        ('R20', 0),
                        ('R9', 0),
                        ('R21', 0),
                        ('HI', 0),
                        ('R10', 0),
                        ('R22', 0),
                        ('LO', 0),
                        ('R11', 0),
                        ('R23', 0),
                        (INSTR_PTR_MIPS, 0),
                        ('F0', 0),
                        ('F12', 0),
                        ('F24', 0),
                        ('F1', 0),
                        ('F13', 0),
                        ('F25', 0),
                        ('F2', 0),
                        ('F14', 0),
                        ('F26', 0),
                        ('F3', 0),
                        ('F15', 0),
                        ('F27', 0),
                        ('F4', 0),
                        ('F16', 0),
                        ('F28', 0),
                        ('F5', 0),
                        ('F17', 0),
                        ('F29', 0),
                        ('F6', 0),
                        ('F18', 0),
                        ('F30', 0),
                        ('F7', 0),
                        ('F19', 0),
                        ('F31', 0),
                        ('F8', 0),
                        ('F20', 0),
                        ('F9', 0),
                        ('F21', 0),
                        ('F10', 0),
                        ('F22', 0),
                        ('F11', 0),
                        ('F23', 0)
                    ])

        self.flags = OrderedDict(
                    [
                        ('COND', 0),
                    ])

        self.pc = 0
        self.instr = 1
        self.ops = 2

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

    def set_int_ip(self):
        self.set_ip(MIPS_INTERRUPT_IP)

    def get_ip(self):
        return int(self.registers[INSTR_PTR_MIPS])

    def inc_sp(self, line_num):
        sp = self.get_sp()
        sp += 1
        self.set_sp(sp, line_num)

    def dec_sp(self, line_num):
        sp = self.get_sp()
        sp -= 1
        self.set_sp(sp, line_num)

    def set_sp(self, val, line_num):
        if val < STACK_BOTTOM - 1:
            raise StackOverflow(line_num)
        if val > STACK_TOP:
            raise StackUnderflow(line_num)

        self.registers[STACK_PTR_MIPS] = val

    def get_sp(self):
        return int(self.registers[STACK_PTR_MIPS])

    def create_bit_negative(self, value, bits):
        """
        Converts an immediate value into a string of bits

        Args:
            value: Immediat value
            bits: Number of bits needed

        Returns:
            Formatted binary value of immediate
            in the number of bits inputted
        """
        imm_code = bin(value).split('b')[1]
        imm_code = '0'*(bits - len(imm_code)) + imm_code
        if value < 0:
            imm_lst = []
            for bit in imm_code:
                imm_lst.append(bit)
            flip_bit = False
            place = bits - 1
            while place >= 0:
                if not flip_bit and imm_lst[place] == "1":
                    flip_bit = True
                elif flip_bit:
                    if imm_lst[place] == "0":
                        imm_lst[place] = "1"
                    else:
                        imm_lst[place] = "0"
                place -= 1
            imm_code = "".join(imm_lst)
        return imm_code

    def create_bit_r_format(self, instr_lst, op_func, func_code):
        """
        Converts an R-format instruction into a string of bits

        Args:
            instr_lst: Line of code

        Returns:
            Formatted version of instruction
        """
        rs = 0
        rt = 0
        shamt = 0
        rd = 0

        # if instruction has shift value
        if func_code == "000000" or func_code == "000010":
            try:
                rd = int(instr_lst[self.ops].get_nm().split('R')[1])
                rt = int(instr_lst[self.ops + 1].get_nm().split('R')[1])
                shamt = instr_lst[self.ops + 2].get_val()
            except Exception:
                pass

        # if function does not use rd
        elif func_code == "011000" or func_code == "011010":
            try:
                rs = int(instr_lst[self.ops].get_nm().split('R')[1])
                rt = int(instr_lst[self.ops + 1].get_nm().split('R')[1])
            except Exception:
                pass

        # if function only uses rd
        elif func_code == "010010" or func_code == "010000":
            try:
                rd = int(instr_lst[self.ops].get_nm().split('R')[1])
            except Exception:
                pass

        # if function only uses rs
        elif func_code == "001000":
            try:
                rs = int(instr_lst[self.ops].get_nm().split('R')[1])
            except Exception:
                pass

        # other arithmetic, logic functions
        else:
            try:
                rs = int(instr_lst[self.ops + 2].get_nm().split('R')[1])
                rt = int(instr_lst[self.ops + 1].get_nm().split('R')[1])
                rd = int(instr_lst[self.ops].get_nm().split('R')[1])
            except Exception:
                pass
        # format the rs, rt, rd, shamt values into 5 bits
        rs = format(rs, '#07b').split('b')[1]
        rt = format(rt, '#07b').split('b')[1]
        rd = format(rd, '#07b').split('b')[1]
        shamt = format(shamt, '#07b').split('b')[1]
        code_lst = [op_func, rs, rt, rd, shamt, func_code, "\n"]
        return " ".join(code_lst)

    def create_bit_i_format(self, instr_lst, op_func):
        """
        Converts an I-format instruction into a string of bits

        Args:
            instr_lst: Line of code

        Returns:
            Formatted version of instruction
        """
        imm = 0
        rs = 0
        rt = 0
        # if not data movement instruction
        if op_func != "100011" and op_func != "101011":
            try:
                rs = int(instr_lst[self.ops + 1].get_nm().split('R')[1])
                rt = int(instr_lst[self.ops].get_nm().split('R')[1])
                imm = int(instr_lst[self.ops + 2].get_val())
            except Exception:
                pass

        # if LW or SW
        else:
            try:
                rs = int(instr_lst[self.ops + 1].get_nm().split('R')[1])
                rt = int(instr_lst[self.ops].get_nm().split('R')[1])
                imm = int(instr_lst[self.ops + 1].displacement)
            except Exception:
                pass

        # format rs, rt into 5 bits
        rs = format(rs, '#07b').split('b')[1]
        rt = format(rt, '#07b').split('b')[1]

        # format imm to 16 bits signed
        imm_code = self.create_bit_negative(imm, 16)
        code_lst = [op_func, rs, rt, imm_code, "\n"]
        return " ".join(code_lst)

    def create_bit_j_format(self, instr_lst, op_func):
        """
        Converts an J-format instruction into a string of bits

        Args:
            instr_lst: Line of code

        Returns:
            Formatted version of instruction
        """
        imm = 0
        try:
            imm = int(instr_lst[self.ops].get_val())
        except Exception:
            pass

        # format imm into 26 bits signed
        imm_code = self.create_bit_negative(imm, 26)
        code_lst = [op_func, imm_code, "\n"]
        return " ".join(code_lst)

    def create_bit_instr(self, instr_lst):
        """
        Converts the instruction into code of bits

        Args:
            instr_lst: Line of code

        Returns:
            Formatted version of the instruction in bits
        """
        op_func = None
        func_code = None
        instr_nm = instr_lst[self.instr].get_nm()
        try:
            op_func, func_code = op_func_codes[instr_nm]
        except Exception:
            op_func = op_func_codes[instr_lst[self.instr].get_nm()]
        if func_code is not None:
            return self.create_bit_r_format(instr_lst, op_func, func_code)
        else:
            if instr_nm != "JAL" and instr_nm != "J":
                return self.create_bit_i_format(instr_lst, op_func)
            else:
                return self.create_bit_j_format(instr_lst, op_func)

    def jump_handler(self, brk, source, instr_line):
        if isinstance(instr_line[self.instr], Jal):
            self.registers["R31"] = self.get_ip()
        if isinstance(instr_line[self.instr], Jr):
            return self.jump_to_label(brk.label, source)
        return self.jump_to_label(brk.label, source, True)

    def exec_instr(self, instr_line, line_num):
        if self.get_ip() != instr_line[self.pc].get_val(line_num):
            raise InvalidArgument(hex(instr_line[self.pc].get_val(line_num)),
                                  line_num)
        self.inc_ip()
        return instr_line[self.instr].f(instr_line[self.ops:], self, line_num)


class RISCVMachine(VirtualMachine):
    # make sure to account for the lack of HI and LO in display

    def __init__(self):
        super().__init__()
        self.ip_div = 4
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

        self.pc = 0
        self.instr = 1
        self.ops = 2

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

    def set_int_ip(self):
        self.set_ip(RISC_INTERRUPT_IP)

    def get_ip(self):
        return int(self.registers[INSTR_PTR_RISCV])

    def inc_sp(self, line_num):
        sp = self.get_sp()
        sp += 1
        self.set_sp(sp, line_num)

    def dec_sp(self, line_num):
        sp = self.get_sp()
        sp -= 1
        self.set_sp(sp, line_num)

    def set_sp(self, val, line_num):
        if val < STACK_BOTTOM - 1:
            raise StackOverflow(line_num)
        if val > STACK_TOP:
            raise StackUnderflow(line_num)

        self.registers[STACK_PTR_RISCV] = val

    def get_sp(self):
        return int(self.registers[STACK_PTR_RISCV])

    def exec_instr(self, instr_line, line_num):
        if self.get_ip() != instr_line[self.pc].get_val(line_num):
            raise InvalidArgument(hex(instr_line[self.pc].get_val(line_num)),
                                  line_num)
        self.inc_ip()
        return instr_line[self.instr].f(instr_line[self.ops:], self, line_num)

    def jump_handler(self, brk, source, instr_line):
        return self.jump_to_label(brk.label, source, True)


class WASMMachine(VirtualMachine):
    def __init__(self):
        super().__init__()
        self.locals = OrderedDict()
        self.locals_init()

        self.globals = OrderedDict()
        self.globals_init()

        self.stack_ptr = STACK_BOTTOM
        self.ip = 0

        self.instr = 0
        self.ops = 1

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

    def inc_sp(self, line_num):
        sp = self.get_sp()
        sp += 4
        self.set_sp(sp, line_num)

    def dec_sp(self, line_num):
        sp = self.get_sp()
        sp -= 4
        self.set_sp(sp, line_num)

    def set_sp(self, val, line_num):
        if val < STACK_BOTTOM - 1:
            raise StackOverflow(line_num)
        if val > STACK_TOP:
            raise StackUnderflow(line_num)

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

    def exec_instr(self, instr_line, line_num):
        self.inc_ip()
        return instr_line[self.instr].f(instr_line[self.ops:], self, line_num)

    def set_next_stack_change(self):
        pass


intel_machine = IntelMachine()
mips_machine = MIPSMachine()
riscv_machine = RISCVMachine()
wasm_machine = WASMMachine()
