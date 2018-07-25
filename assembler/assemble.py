"""
assemble.py
Executes assembly code typed in.
"""

import re

from .flowbreak import FlowBreak
from .errors import Error, InvalidInstruction, InvalidArgument, ExitProg
from .parse import add_debug, parse
from .lex import lex
from .tokens import Instruction
from .MIPS.control_flow import Jal, Jr
from .MIPS.key_words import op_func_codes

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

def jump_to_label(label, source, vm, jal = False):
    if label in vm.labels:
        ip = vm.labels[label]  # set i to line num of label
        vm.set_ip(ip + vm.start_ip)
        return (True, source, "")
    else:
        try:
            ip = int(label)
            if jal:
                ip = ip >> 2
            vm.set_ip(ip)
            return (True, source, "")
        except:
            return (False, source, "Invalid label: " + label)

def create_bit_pc(instr_lst):
    pc_bit = instr_lst[PC_MIPS].get_val()
    pc_bit = format(pc_bit, '#34b').split('b')[1]
    return pc_bit

def create_bit_instr(instr_lst, bit_code):
    op_func = None 
    func_code = None
    instr_nm = instr_lst[INSTR_MIPS].get_nm()
    rs = 0
    rt = 0
    try:
        op_func, func_code = op_func_codes[instr_nm]
    except:
        op_func = op_func_codes[instr_lst[INSTR_MIPS].get_nm()]
    if func_code != None:
        shamt = 0
        rd = 0
        if instr_nm == "SLL" or instr_nm == "SRL":
            try:
                rd = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
                rt = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
                shamt = instr_lst[OPS_MIPS + 2].get_val()
            except: 
                pass 
        elif instr_nm == "MULT" or instr_nm == "DIV":
            try:
                rs = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
                rt = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
                shamt = instr_lst[OPS_MIPS + 2].get_val()
            except:
                pass
        elif instr_nm == "MFLO" or instr_nm == "MFHI":
            try:
                rd = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            except:
                pass
        elif instr_nm == "JR":
            try:
                rs = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            except:
                pass
        else:
            try:
                rs = int(instr_lst[OPS_MIPS + 2].get_nm().split('R')[1])
                rt = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
                rd = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
            except: 
                pass
        rs = format(rs, '#07b').split('b')[1]
        rt = format(rt, '#07b').split('b')[1]
        rd = format(rd, '#07b').split('b')[1]
        shamt = format(shamt, '#07b').split('b')[1]
        code_lst = [op_func, rs, rt, rd, shamt, func_code, "\n"]
        bit_code += " ".join(code_lst)
    else:
        imm = 0
        if instr_nm != "JAL" and instr_nm != "J":
            if instr_nm != "LW" and instr_nm != "SW":
                try:
                    rs = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
                    rt = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
                    imm = int(instr_lst[OPS_MIPS + 2].get_val())
                except:
                    pass
            else:
                try:
                    rs = int(instr_lst[OPS_MIPS + 1].get_nm().split('R')[1])
                    rt = int(instr_lst[OPS_MIPS].get_nm().split('R')[1])
                    imm = int(instr_lst[OPS_MIPS + 1].displacement)
                except:
                    pass

            rs = format(rs, '#07b').split('b')[1]
            rt = format(rt, '#07b').split('b')[1]

            imm_code = bin(imm).split('b')[1]
            if imm < 0:
                imm_code = '1'*(16 - len(imm_code)) + imm_code
            else:
                imm_code = '0'*(16 - len(imm_code)) + imm_code
            code_lst = [op_func, rs, rt, imm_code, "\n"]
            bit_code += " ".join(code_lst)
        else:
            try:
                imm = int(instr_lst[OPS_MIPS].get_val())
            except:
                pass
            imm_code = bin(imm).split('b')[1]
            if imm < 0:
                imm_code = '1'*(26 - len(imm_code)) + imm_code
            else:
                imm_code = '0'*(26 - len(imm_code)) + imm_code
            code_lst = [op_func, imm_code, "\n"]
            bit_code += " ".join(code_lst)
    return bit_code


def exec(tok_lines, flavor, vm, last_instr):
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
        last_intr = None
        if flavor == "mips":
            if ip // 4 >= len(tok_lines):
                raise InvalidInstruction("Past end of code.")
            (curr_instr, source) = tok_lines[ip // 4]
            if vm.get_ip() != curr_instr[PC_MIPS].get_val():
                raise InvalidArgument(hex(curr_instr[PC_MIPS].get_val()))
            vm.inc_ip()
            last_instr = curr_instr[INSTR_MIPS].f(curr_instr[OPS_MIPS:], vm)
        else:
            if ip >= len(tok_lines):
                raise InvalidInstruction("Past end of code.")

            (curr_instr, source) = tok_lines[ip]
            vm.inc_ip()
            last_instr = curr_instr[INSTR_INTEL].f(curr_instr[OPS_INTEL:], vm)
        return (True, source, "")
    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        add_debug("In FlowBreak", vm)
        dump_flags(vm)
        if isinstance(curr_instr[INSTR_MIPS], Jal):
            vm.registers["R31"] = vm.get_ip()
        if isinstance(curr_instr[INSTR_MIPS], Jr):
            return jump_to_label(brk.label, source, vm)
        return jump_to_label(brk.label, source, vm, True)
    except ExitProg as ep:
        raise ExitProg
    except Error as err:
        return (False, last_instr, err.msg)

def assemble(code, flavor, vm, step=False):
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            vm:
                Our virtual machine. Contains:
                registers: current register values.
                memory: current memory values.
                flags: current values of flags.
            flavor: Intel, AT&T, MIPS?
            step: are we stepping through code or running continuously?
        Returns:
            next 
            Error, if any.
    """
    last_instr = ''
    error = ''
    bit_code = ''

    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", "")

    tok_lines = None

    # break the code into tokens:
    try:
        #tok_lines = lex(code, vm)

        tok_lines = lex(code, flavor, vm)
        tok_lines = parse(tok_lines, flavor, vm)
    except Error as err:
        return (last_instr, err.msg, bit_code)

    try:
        if flavor == "mips":
            for curr_instr, source in tok_lines:
                bit_code += create_bit_pc(curr_instr) + " "
                bit_code = create_bit_instr(curr_instr, bit_code)
        if not step:
            add_debug("Setting ip to 0", vm)
            vm.set_ip(vm.start_ip)   # instruction pointer reset for 'run'
            count = 0
            if flavor == "mips":
                while (vm.get_ip() - vm.start_ip) // 4 < len(tok_lines) and count < MAX_INSTRUCTIONS:
                    (success, last_instr, error) = exec(tok_lines, flavor, vm, 
                                                        last_instr)
                    if not success:
                        return (last_instr, error, bit_code)
                    count += 1
            else:
                while vm.get_ip() < len(tok_lines) and count < MAX_INSTRUCTIONS:
                    (success, last_instr, error) = exec(tok_lines, flavor, vm, 
                                                        last_instr)
                    if not success:
                        return (last_instr, error, bit_code)
                    count += 1
        else:  # step through code
            count = 0
            if vm.get_ip() == 0:
                vm.set_ip(vm.start_ip)
            ip = vm.get_ip() - vm.start_ip
            if flavor == "mips":
                ip = ip // 4
            if ip < len(tok_lines):
                (success, last_instr, error) = exec(tok_lines, flavor, vm,
                                                    last_instr)
                count += 1
            else:
                last_instr = "Reached end of executable code."
                # rewind:
                vm.set_ip(vm.start_ip)
            return (last_instr, error, bit_code)
    except ExitProg as ep:
        last_instr = "Exiting program"

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (last_instr, error, bit_code)
