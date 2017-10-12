"""
assemble.py
Executes assembly code typed in.
"""

import re

from .control_flow import FlowBreak
from .errors import Error, InvalidInstruction
from .parse import lex, add_debug
from .tokens import Instruction

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

JMP_STR = "A jump instruction."


INSTR = 0
OPS = 1

def dump_flags(vm):
    for flag, val in vm.flags.items():
        add_debug("Flag = " + flag + "; val = " + str(val), vm)

def jump_to_label(label, vm):
    pass

def exec(tok_lines, vm, last_instr):
    """
        Executes a single instruction at location reg[EIP] in tok_lines.
        Returns:
            success: was instruction valid?
            last_instr: any last_instr
            err_msg: if no success, what went wrong?
    """
    try:
        ip = vm.get_ip()
        if ip >= len(tok_lines):
            raise InvalidInstruction("Past end of code.")

        curr_instr = tok_lines[ip]
        vm.inc_ip()
        last_instr = curr_instr[INSTR].f(curr_instr[OPS], vm)
        return (True, last_instr, "")
    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        add_debug("In FlowBreak", vm)
        dump_flags(vm)
        label = brk.label
        if label in vm.labels:
            ip = vm.labels[label]  # set i to line num of label
            vm.set_ip(ip)
            return (True, JMP_STR, "")
        else:
            return (False, JMP_STR, "Invalid label: " + label)
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
        Returns:
            next 
            Error, if any.
    """
    last_instr = ''
    error = ''

    if code is None or len(code) == 0:
        return ("", "Must submit code to run.")

    tok_lines = None

    # break the code into tokens:
    try:
        tok_lines = lex(code, vm)
    except Error as err:
        return (last_instr, err.msg)

    if not step:
        add_debug("Setting ip to 0", vm)
        vm.set_ip(0)   # instruction pointer reset for 'run'
        count = 0
        while vm.get_ip() < len(tok_lines) and count < MAX_INSTRUCTIONS:
            (success, last_instr, error) = exec(tok_lines, vm, 
                                                last_instr)
            if not success:
                return (last_instr, error)
            count += 1
    else:  # step through code
        ip = vm.get_ip()
        add_debug("Next key = " + str(vm.nxt_key), vm)
        add_debug("Ret str = " + str(vm.ret_str), vm)
        if ip < len(tok_lines):
            (success, last_instr, error) = exec(tok_lines, vm,
                                                last_instr)
        else:
            last_instr = "Reached end of executable code."
            # rewind:
            vm.set_ip(0)
        return (last_instr, error)

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (last_instr, error)
