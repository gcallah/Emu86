"""
assemble.py
Executes assembly code typed in.
"""

import re

from .flowbreak import FlowBreak
from .errors import Error, InvalidInstruction, ExitProg
from .parse import add_debug, parse
from .lex import lex
from .tokens import Instruction

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

JMP_STR = "A jump instruction."


INSTR = 0
OPS = 1

def dump_flags(vm):
    for flag, val in vm.flags.items():
        add_debug("Flag = " + flag + "; val = " + str(val), vm)

def jump_to_label(label, source, vm):
    if label in vm.labels:
        ip = vm.labels[label]  # set i to line num of label
        vm.set_ip(ip)
        return (True, source, "")
    else:
        return (False, source, "Invalid label: " + label)

def exec(tok_lines, flavor, vm, last_instr):
    """
        Executes a single instruction at location reg[EIP] in tok_lines.
        Returns:
            success: was instruction valid?
            last_instr: any last_instr
            err_msg: if no success, what went wrong?
    """
    try:
        ip = vm.get_ip()
        curr_instr = None
        source = None
        if flavor == "mips":
            if ip // 4 >= len(tok_lines):
                raise InvalidInstruction("Past end of code.")

            (curr_instr, source) = tok_lines[ip // 4]
            vm.inc_ip()
        else:
            if ip >= len(tok_lines):
                raise InvalidInstruction("Past end of code.")

            (curr_instr, source) = tok_lines[ip]
            vm.inc_ip()
        last_instr = curr_instr[INSTR].f(curr_instr[1:], vm)
        return (True, source, "")
    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        add_debug("In FlowBreak", vm)
        dump_flags(vm)
        return jump_to_label(brk.label, source, vm)
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
            flavor: Intel or AT&T? 
            step: are we stepping through code or running continuously?
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
        #tok_lines = lex(code, vm)

        tok_lines = lex(code, flavor, vm)
        tok_lines = parse(tok_lines, flavor, vm)
    except Error as err:
        return (last_instr, err.msg)

    try:
        if not step:
            add_debug("Setting ip to 0", vm)
            vm.set_ip(0)   # instruction pointer reset for 'run'
            count = 0
            ip = vm.get_ip()
            if flavor == "mips":
                while vm.get_ip() // 4 < len(tok_lines) and count < MAX_INSTRUCTIONS:
                    (success, last_instr, error) = exec(tok_lines, flavor, vm, 
                                                        last_instr)
                    if not success:
                        return (last_instr, error)
                    count += 1
            else:
                while vm.get_ip() < len(tok_lines) and count < MAX_INSTRUCTIONS:
                    (success, last_instr, error) = exec(tok_lines, flavor, vm, 
                                                        last_instr)
                    if not success:
                        return (last_instr, error)
                    count += 1
        else:  # step through code
            count = 0
            ip = vm.get_ip()
            if flavor == "mips":
                ip = ip // 4
            if ip < len(tok_lines):
                (success, last_instr, error) = exec(tok_lines, flavor, vm,
                                                    last_instr)
                count += 1
            else:
                last_instr = "Reached end of executable code."
                # rewind:
                vm.set_ip(0)
            return (last_instr, error)
    except ExitProg as ep:
        last_instr = "Exiting program"

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (last_instr, error)
