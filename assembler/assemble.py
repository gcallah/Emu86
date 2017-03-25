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

def exec(tok_lines, gd, output, debug, labels):
    """
        Executes a single instruction at location gd.ip in tok_lines.
        Returns:
            success: was instruction valid?
            output: any output
            err_msg: if no success, what went wrong?
            debug: any debug info
    """
    curr_instr = tok_lines[gd.ip]
    gd.ip = gd.ip + 1
    try:
        output += curr_instr[INSTR].f(curr_instr[OPS], gd)
        return (True, output, "", debug)
    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        label = brk.label
        if label in labels:
            gd.ip = labels[label]  # set i to line num of label
            return (True, output, "", debug)
        else:
            return (False, output, "Invalid label: " + label, debug)
    except Error as err:
        return (False, output, err.msg, debug)

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
            Output, if any.
            Error, if any.
    """
    global debug
    debug = ''
    output = ''
    error = ''

    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    labels = None

    # break the code into tokens:
    try:
        (tok_lines, labels) = lex(code, gd)
    except Error as err:
        return (output, err.msg, debug)

    if not step:
        add_debug("Setting ip to 0")
        gd.ip = 0   # instruction pointer reset for 'run'
        count = 0
        while gd.ip < len(tok_lines) and count < MAX_INSTRUCTIONS:
            add_debug("ip = " + str(gd.ip))
            (success, output, error, debug) = exec(tok_lines, gd, 
                                                   output, debug, labels)
            if not success:
                return (output, error, debug)
            count += 1
    else:  # step through code
        add_debug("In step, ip = " + str(gd.ip))
        (success, output, error, debug) = exec(tok_lines, 
                                      gd, output, debug, labels)
        return (output, error, debug)

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded "
                 + str(MAX_INSTRUCTIONS))
    else:
        error = ''
    return (output, error, debug)
