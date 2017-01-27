"""
assemble.py
Executes assembly code typed in.
"""

import re

from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .arithmetic import add, sub, imul, idiv, inc, dec, shl
from .arithmetic import shr, notf, andf, orf, xor, neg
from .control_flow import jmp, cmp, je, jne, Jmp, FlowBreak
from .control_flow import jg, jge, jl, jle
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
        'CMP': cmp,
        'JMP': jmp,
        'JE': je,
        'JNE': jne,
        # the next two instructions are just synonyms for the previous two.
        'JZ': je,
        'JNZ': jne,
        'JG': jg,
        'JGE': jge,
        'JL': jl,
        'JLE': jle,
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

    code_pos = 0
    output = ''
    error = ''
    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    labels = {}
    lines = code.split("\n")
    # we will make two passes: one to set up labels
    #  and strip out comments, and
    #  then one to actually perform instructions.
    for line_no, line in enumerate(lines):
        line = line.strip()

        # comments:
        comm_start = line.find(";")
        if comm_start >= 0:  # -1 means not found
            line = line[0:comm_start]
            lines[line_no] = line

        # labels:
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
        if len(line) <= 1:  # blank lines ok; just skip 'em
            continue
        code_pos = 0
        try:
            # we only want one instruction per line!
            outp = get_instruction(line, gdata, code_pos)
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

def get_instruction(code, gdata, code_pos):
    """
    We expect an instruction next.
        Args:
            code: code to interpret
            gdata:
                Contains:
                registers: current register values.
                memory: current memory values.
                flags: current values of flags.
            code_pos: where we are in code
        Returns:
            Output
    """
    (token, code_pos) = get_token(code, code_pos)
    if token == '':
        return ''
    else:
        instr = Instruction(token, instructions)
        add_debug("Calling " + token)
        return instr.exec(code, gdata, code_pos)
