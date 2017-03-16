"""
assemble.py
Executes assembly code typed in.
"""

import re

from .control_flow import FlowBreak
from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .interrupts import nxt_key
from .parse import lex
from .tokens import Instruction

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

debug = ""


def add_debug(s):
    global debug
    debug += (s + "\n")


INSTR = 0
OPS = 1

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
        curr_instr = tok_lines[ip]
        ip += 1
        count += 1
        try:
            output += curr_instr[INSTR].f(curr_instr[OPS], gdata)
        except FlowBreak as brk:
            # we have hit one of the JUMP instructions: jump to that line.
            label = brk.label
            if label in labels:
                ip = labels[label]  # set i to line num of label
            else:
                return (output, "Invalid label: " + label, debug)
        except Error as err:
            return (output, err.msg, debug)
    if count == MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (output, error, debug)
