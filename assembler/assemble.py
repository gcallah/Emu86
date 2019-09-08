"""
assemble.py
Executes assembly code typed in.
"""
from .flowbreak import FlowBreak
from .errors import Error, InvalidInstruction, InvalidArgument, ExitProg
from .parse import add_debug, parse
from .lex import lex
from .MIPS.control_flow import Jal, Jr
from .MIPS.key_words import op_func_codes
# from .RISCV.control_flow import  Jr, Jal

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

JMP_STR = "A jump instruction."


INSTR_INTEL = 0
OPS_INTEL = 1

PC_MIPS = 0
INSTR_MIPS = 1
OPS_MIPS = 2


def dump_flags(vm):
    for flag, val in vm.flags.items():
        add_debug("Flag = " + flag + "; val = " + str(val), vm)


def jump_to_label(label, source, vm, jal=False):
    if label in vm.labels:
        ip = vm.labels[label]  # set i to line num of label
        vm.set_ip(ip + vm.start_ip)
        vm.next_stack_change = label
        return (True, source, "")
    else:
        try:
            ip = int(label)
            if jal:
                ip = ip >> 2
            vm.set_ip(ip)
            return (True, source, "")
        except Exception:
            return (False, source, "Invalid label: " + label)


def create_bit_negative(value, bits):
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


def create_bit_r_format(instr_lst, op_func, func_code):
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
            rd = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            rt = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
            shamt = instr_lst[OPS_MIPS + 2].get_val()
        except Exception:
            pass

    # if function does not use rd
    elif func_code == "011000" or func_code == "011010":
        try:
            rs = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            rt = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
        except Exception:
            pass

    # if function only uses rd
    elif func_code == "010010" or func_code == "010000":
        try:
            rd = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
        except Exception:
            pass

    # if function only uses rs
    elif func_code == "001000":
        try:
            rs = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
        except Exception:
            pass

    # other arithmetic, logic functions
    else:
        try:
            rs = int(instr_lst[OPS_MIPS + 2].get_nm().split('R')[1])
            rt = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
            rd = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
        except Exception:
            pass
    # format the rs, rt, rd, shamt values into 5 bits
    rs = format(rs, '#07b').split('b')[1]
    rt = format(rt, '#07b').split('b')[1]
    rd = format(rd, '#07b').split('b')[1]
    shamt = format(shamt, '#07b').split('b')[1]
    code_lst = [op_func, rs, rt, rd, shamt, func_code, "\n"]
    return " ".join(code_lst)


def create_bit_i_format(instr_lst, op_func):
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
            rs = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
            rt = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            imm = int(instr_lst[OPS_MIPS + 2].get_val())
        except Exception:
            pass

    # if LW or SW
    else:
        try:
            rs = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
            rt = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            imm = int(instr_lst[OPS_MIPS + 1].displacement)
        except Exception:
            pass

    # format rs, rt into 5 bits
    rs = format(rs, '#07b').split('b')[1]
    rt = format(rt, '#07b').split('b')[1]

    # format imm to 16 bits signed
    imm_code = create_bit_negative(imm, 16)
    code_lst = [op_func, rs, rt, imm_code, "\n"]
    return " ".join(code_lst)


def create_bit_j_format(instr_lst, op_func):
    """
    Converts an J-format instruction into a string of bits

    Args:
        instr_lst: Line of code

    Returns:
        Formatted version of instruction
    """
    imm = 0
    try:
        imm = int(instr_lst[OPS_MIPS].get_val())
    except Exception:
        pass

    # format imm into 26 bits signed
    imm_code = create_bit_negative(imm, 26)
    code_lst = [op_func, imm_code, "\n"]
    return " ".join(code_lst)


def create_bit_instr(instr_lst):
    """
    Converts the instruction into code of bits

    Args:
        instr_lst: Line of code

    Returns:
        Formatted version of the instruction in bits
    """
    op_func = None
    func_code = None
    instr_nm = instr_lst[INSTR_MIPS].get_nm()
    try:
        op_func, func_code = op_func_codes[instr_nm]
    except Exception:
        op_func = op_func_codes[instr_lst[INSTR_MIPS].get_nm()]
    if func_code is not None:
        return create_bit_r_format(instr_lst, op_func, func_code)
    else:
        if instr_nm != "JAL" and instr_nm != "J":
            return create_bit_i_format(instr_lst, op_func)
        else:
            return create_bit_j_format(instr_lst, op_func)


def exec(tok_lines, vm, last_instr):
    """
        Executes a single instruction at location reg[EIP] in tok_lines.
        Returns:
            success: was instruction valid?
            last_instr: any last_instr
            err_msg: if no success, what went wrong?
    """
    try:
        ip = vm.get_ip() - vm.start_ip
        curr_instr = None
        source = None
        last_instr = None
        if (vm.flavor == "mips_asm" or vm.flavor == "mips_mml" or
                vm.flavor == "riscv"):
            if ip // 4 >= len(tok_lines):
                raise InvalidInstruction("Past end of code.")
            (curr_instr, source) = tok_lines[ip // 4]
            if vm.get_ip() != curr_instr[PC_MIPS].get_val():
                raise InvalidArgument(hex(curr_instr[PC_MIPS].get_val()))
            vm.inc_ip()
            last_instr = curr_instr[INSTR_MIPS].f(curr_instr[OPS_MIPS:], vm)

    # if flavor == "riscv":
    #     if ip // 4 >= len(tok_lines):
    #         raise InvalidInstruction("Past end of code.")
    #     (curr_instr, source) = tok_lines[ip // 4]
    #     if vm.get_ip() != curr_instr[PC_RISCV].get_val():
    #         raise InvalidArgument(hex(curr_instr[PC_RISCV].get_val()))
    #     vm.inc_ip()
    #     last_instr = curr_instr[INSTR_RISCV].f(curr_instr[OPS_RISCV:], vm)

        else:
            if ip >= len(tok_lines):
                raise InvalidInstruction("Past end of code.")

            (curr_instr, source) = tok_lines[ip]
            vm.inc_ip()
            last_instr = curr_instr[INSTR_INTEL].f(curr_instr[OPS_INTEL:], vm)
        if vm.flavor != 'wasm':
            for label in vm.labels:
                if vm.get_ip() == vm.labels[label]:
                    vm.next_stack_change = label
        return (True, source, "")

    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        add_debug("In FlowBreak", vm)
        dump_flags(vm)
        if isinstance(curr_instr[INSTR_MIPS], Jal) and vm.flavor != 'riscv':
            vm.registers["R31"] = vm.get_ip()
        if isinstance(curr_instr[INSTR_MIPS], Jr) and vm.flavor != 'riscv':
            return jump_to_label(brk.label, source, vm)
        return jump_to_label(brk.label, source, vm, True)
    except ExitProg:
        raise ExitProg(source)
    except Error as err:
        return (False, last_instr, err.msg)


def assemble(code, vm, step=False):

    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            vm:
                Our virtual machine. Contains:
                registers: current register values.
                memory: current memory values.
                flags: current values of flags.
            step: are we stepping through code or running continuously?
        Returns:
            next
            Error, if any.
    """
    last_instr = ''
    error = ''
    bit_code = ''
    if vm.flavor != 'wasm' and vm.next_stack_change != "":

        vm.stack_change = vm.next_stack_change
        vm.next_stack_change = ""
        if len(vm.c_stack) != 0 and not isinstance(vm.c_stack[-1], int):
            vm.c_stack.pop()
        vm.c_stack.append(vm.stack_change)

    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", "")

    tok_lines = None

    # break the code into tokens:
    try:
        tok_lines = lex(code, vm)
        tok_lines = parse(tok_lines, vm)

    except Error as err:
        return (last_instr, err.msg, bit_code)

    try:
        if vm.flavor == "mips_asm" or vm.flavor == "mips_mml":
            for curr_instr, source in tok_lines:
                bit_code += create_bit_instr(curr_instr)
        if not step:
            add_debug("Setting ip to 0", vm)
            vm.set_ip(vm.start_ip)   # instruction pointer reset for 'run'
            count = 0
            if (vm.flavor == "mips_asm" or vm.flavor == "mips_mml" or
                    vm.flavor == "riscv"):
                while ((vm.get_ip() - vm.start_ip) // 4 < len(tok_lines) and
                       count < MAX_INSTRUCTIONS):
                    (success, last_instr, error) = exec(tok_lines, vm,
                                                        last_instr)
                    if not success:
                        return (last_instr, error, bit_code)
                    count += 1
            else:
                while (vm.get_ip() < len(tok_lines) and
                       count < MAX_INSTRUCTIONS):
                    (success, last_instr, error) = exec(tok_lines, vm,
                                                        last_instr)
                    if not success:
                        return (last_instr, error, bit_code)
                    count += 1
        else:  # step through code
            count = 0
            if vm.get_ip() == 0:
                vm.set_ip(vm.start_ip)
            ip = vm.get_ip() - vm.start_ip
            if (vm.flavor == "mips_asm" or vm.flavor == "mips_mml" or
                    vm.flavor == "riscv"):
                ip = ip // 4
            if ip < len(tok_lines):
                (success, last_instr, error) = exec(tok_lines, vm,
                                                    last_instr)
                count += 1
            else:
                last_instr = "Reached end of executable code."
                # rewind:
                vm.set_ip(vm.start_ip)

            return (last_instr, error, bit_code)
    except ExitProg as ep:

        last_instr = ep.msg.split(":")[0] + ": Exiting program"
        if vm.flavor == "mips_asm" or vm.flavor == "mips_mml":
            vm.set_ip(2147484032)
        elif vm.flavor == "riscv":
            vm.set_ip(470351872)

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''

    return (last_instr, error, bit_code)
