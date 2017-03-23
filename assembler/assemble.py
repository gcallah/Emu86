"""
assemble.py
Executes assembly code typed in.
"""

import re

from .control_flow import FlowBreak
from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .parse import lex
from .tokens import Instruction

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

debug = ""


def add_debug(s):
    global debug
    debug += (s + "\n")


INSTR = 0
OPS = 1

def exec(tok_lines, ip, gdata, output, debug):
    """
        Executes a single instruction at location ip in tok_lines.
        Returns:
            success: was instruction valid?
            ip: where are we now?
            output: any output
            err_msg: if no success, what went wrong?
            debug: any debug info
    """
    curr_instr = tok_lines[ip]
    ip = ip + 1
    try:
        output += curr_instr[INSTR].f(curr_instr[OPS], gdata)
        return (True, ip, output, "", debug)
    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        label = brk.label
        if label in labels:
            ip = labels[label]  # set i to line num of label
            return (True, ip, output, "", debug)
        else:
            return (False, ip, output, "Invalid label: " + label, debug)
    except Error as err:
        return (False, ip, output, err.msg, debug)

def assemble(code, gdata):
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            gdata:
                Contains:
                registers: current register values.
                memory: current memory values.
                flags: current values of flags.
        Returns:
            Output, if any.
            Error, if any.
    """
    global debug
    global nxt_key
    debug = ''
    output = ''
    error = ''
    nxt_key = 0

    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    # break the code into tokens:
    (tok_lines, labels) = lex(code, gdata)

    ip = 0   # instruction pointer
    count = 0
    while ip < len(tok_lines) and count < MAX_INSTRUCTIONS:
        (success, ip, output, error, debug) = exec(tok_lines, ip, gdata, output, debug)
        if not success:
            return (output, err.msg, debug)
        count += 1
    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (output, error, debug)
