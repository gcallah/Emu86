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
    debug = ''
    output = ''
    error = ''
    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    # break the code into tokens:
    (tok_lines, labels) = lex(code, gdata)

    i = 0
    j = 0
    while i < len(tok_lines) and j < MAX_INSTRUCTIONS:
        curr_instr = tok_lines[i]
        i += 1
        j += 1
        try:
            # we only want one instruction per line!
            outp = curr_instr[INSTR].exec(curr_instr[OPS], gdata)
            output += outp
        except FlowBreak as brk:
            # we have hit one of the JUMP instructions: jump to that line.
            label = brk.label
            if label in labels:
                i = labels[label]  # set i to line num of label
            else:
                return (output, "Invalid label: " + label, debug)
        except Error as err:
            return (output, err.msg, debug)
    if j == MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (output, error, debug)
