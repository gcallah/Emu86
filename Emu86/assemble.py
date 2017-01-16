"""
assemble.py
Executes assembly code typed in.
"""

import re

from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .arithmetic import add, sub, imul, idiv, inc, dec, shl
from .arithmetic import shr, notf, andf, orf, xor, neg
from .control_flow import jmp, Jmp, FlowBreak
from .data_mov import mov
from .parse import get_token, get_op, get_one_op, get_two_ops, SYMBOL_RE
from .tokens import Instruction

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

debug = ""


def add_debug(s):
    global debug
    debug += (s + "\n")

instructions = {
        # control flow:
        'JMP': jmp,
        # data movement:
        'MOV': mov,
        # arithmetic and logic:
        'ADD': add,
        'IMUL': imul,
        'IDIV': idiv,
        'SUB': sub,
        'AND': andf,
        'OR': orf,
        'XOR': xor,
        'SHL': shl,
        'SHR': shr,
        'NOT': notf,
        'INC': inc,
        'DEC': dec,
        'NEG': neg,
        }


def assemble(code, registers, memory, flags):
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            registers: current register values.
            memory: current memory values.
            flags: current values of flags.
        Returns:
            Output, if any.
            Error, if any.
    """
    global debug
    debug = ''

    code_pos = 0
    output = ''
    error = ''
    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    labels = {}
    lines = code.split("\n")
    # we will make two passes: one to set up labels,
    #  then one to actually perform instructions.
    for line_no, line in enumerate(lines):
        line = line.strip()
        p = re.compile(SYMBOL_RE + ":")
        label_match = re.search(p, line)
        if label_match is None:
            continue
        else:
            label = label_match.group(1)
            label = label.upper()
            labels[label] = line_no
            # now strip off the label:
            line = line.split(":", 1)[-1]
            lines[line_no] = line
    i = 0
    j = 0
    while i < len(lines) and j < MAX_INSTRUCTIONS:
        line = lines[i]
        i += 1
        j += 1
        add_debug("Got line of " + line)
        code_pos = 0
        try:
            # we only want one instruciton per line!
            outp = get_instruction(line, registers, memory, flags, code_pos)
            output += outp
        except FlowBreak as brk:
            label = brk.label
            if label in labels:
                i = labels[label]  # set i to line num of label
            else:
                return (output, "Invalid label: " + label, debug)
        except Error as err:
            return (output, err.msg, debug)
    if j == MAX_INSTRUCTIONS:
        error = "Possible infinite loop detected."
    else:
        error = ''
    return (output, error, debug)

def get_instruction(code, registers, memory, flags, code_pos):
    """
    We expect an instruction next.
        Args:
            code: code to interpret
            regsiters: current register values
            memory: current memory values
            flags: current flag values
            code_pos: where we are in code
        Returns:
            None
    """
    (token, code_pos) = get_token(code, code_pos)
    if token == '':
        return ''
    else:
        instr = Instruction(token, instructions)
        add_debug("Calling " + token)
        return instr.exec(code, registers, memory, code_pos)

