"""
assemble.py
Executes assembly code typed in.
"""

import re

from .control_flow import FlowBreak
from .errors import Error, InvalidInstruction
from .parse import lex
from .tokens import Instruction

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

JMP_STR = "A jump instruction."


def add_debug(s, gd):
    gd.debug += (s + "\n")


INSTR = 0
OPS = 1

def dump_flags(gd):
    for flag, val in gd.flags.items():
        add_debug("Flag = " + flag + "; val = " + str(val), gd)

def exec(tok_lines, gd, last_instr, labels):
    """
        Executes a single instruction at location reg[EIP] in tok_lines.
        Returns:
            success: was instruction valid?
            last_instr: any last_instr
            err_msg: if no success, what went wrong?
    """
    try:
        ip = gd.get_ip()
        if ip >= len(tok_lines):
            raise InvalidInstruction("Past end of code.")

        curr_instr = tok_lines[ip]
        gd.inc_ip()
        last_instr = curr_instr[INSTR].f(curr_instr[OPS], gd)
        return (True, last_instr, "")
    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        add_debug("In FlowBreak", gd)
        dump_flags(gd)
        label = brk.label
        if label in labels:
            ip = labels[label]  # set i to line num of label
            gd.set_ip(ip)
            return (True, JMP_STR, "")
        else:
            return (False, JMP_STR, "Invalid label: " + label)
    except Error as err:
        return (False, last_instr, err.msg)

def assemble(code, gd, step=False):
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            gd:
                Contains:
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

    labels = None
    tok_lines = None

    # break the code into tokens:
    try:
        (tok_lines, labels) = lex(code, gd)
    except Error as err:
        return (last_instr, err.msg)

    if not step:
        add_debug("Setting ip to 0", gd)
        gd.set_ip(0)   # instruction pointer reset for 'run'
        count = 0
        while gd.get_ip() < len(tok_lines) and count < MAX_INSTRUCTIONS:
            (success, last_instr, error) = exec(tok_lines, gd, 
                                                last_instr, labels)
            if not success:
                return (last_instr, error)
            count += 1
    else:  # step through code
        ip = gd.get_ip()
        add_debug("Next key = " + str(gd.nxt_key), gd)
        add_debug("Ret str = " + str(gd.ret_str), gd)
        if ip < len(tok_lines):
            (success, last_instr, error) = exec(tok_lines, gd,
                                                last_instr, labels)
        else:
            last_instr = "Reached end of executable code."
            # rewind:
            gd.set_ip(0)
        return (last_instr, error)

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (last_instr, error)
