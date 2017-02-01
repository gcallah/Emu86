"""
parse.py: creates parse tree.
"""

import re

from .errors import *  # import * OK here:
                       # these are *our* errors, after all!
from .tokens import Location, Address, Register, IntOp, Symbol, Instruction
from .arithmetic import add, sub, imul, idiv, inc, dec, shl
from .arithmetic import shr, notf, andf, orf, xor, neg
from .control_flow import jmp, cmp, je, jne, Jmp, FlowBreak
from .control_flow import jg, jge, jl, jle
from .data_mov import mov


SYMBOL_RE = "^([A-Za-z]+)"
sym_match = re.compile(SYMBOL_RE)

DELIMITERS = set([' ', ',', '\n', '\r', '\t',])

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


def get_token(code, code_pos):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    token = ''
    if code_pos <= len(code):
        count = 0
        for char in code[code_pos:]:  # eat leading delimiters
            if char in DELIMITERS:
                count += 1
            else:
                break
        code_pos += count

        if code_pos <= len(code):
            count = 0
            for char in code[code_pos:]:
                count += 1
                if char not in DELIMITERS:
                    token = token + char
                else:
                    break
            code_pos += count

    token = token.upper()  # for now, a simple-minded way to allow input in
                           # either case!
    return (token, code_pos)

def get_op(token, gdata):
    """
    Returns int value of operand: direct int or reg val
    Args:
        op: operand to evaluate
    Returns:
        int value
    """

    int_val = 0

    if not token:
        return None
    elif token in gdata.registers:
        return Register(token, gdata.registers)
    elif token[0] == '[' and token[len(token) - 1] == ']':
        address = token[1:len(token) - 1]
        if address in gdata.memory:
            return Address(token[1:len(token) - 1], gdata.memory)
        else:
            raise InvalidAddress(address)
    elif token.isalpha():
        return Symbol(token)
    else:
        try:
            int_val = int(token)
        except Exception:
            raise InvalidOperand(token)
        return IntOp(int_val)

def get_instr(code, code_pos):
    """
    Get an instruction from the code text.
    Args:
        code: the code!
        code_pos: where we are in reading the code.
    Returns:
        a tuple of the instruction found and the new code_pos.
        (Throws an exception if the token is not an instruction.)
    """
    (token, code_pos) = get_token(code, code_pos)
    instr = Instruction(token, instructions)
    return (instr, code_pos)

def get_ops(code, code_pos, gdata):
    """
    """
    ops = []
    while code_pos < len(code):
        (token, code_pos) = get_token(code, code_pos)
        op = get_op(token, gdata)
        ops.append(op)

    return (ops, code_pos)

def lex(code, gdata):
    """
    Lexical phase: tokenizes the code.
    Args:
        code: The code.
    Returns:
        tok_lines: the tokenized version
        labels: jump locations for code labels
    """
    code_pos = 0
    labels = {}
    lines = code.split("\n")
    tok_lines = []  # this will hold the tokenized version of the code
    i = 0
    for line in lines:
        code_pos = 0   # reset each line!
        line = line.strip()
        if len(line) == 0:  # blank lines ok; just skip 'em
            continue

        # comments:
        comm_start = line.find(";")
        if comm_start > 0:  # -1 means not found
            line = line[0:comm_start]
        elif comm_start == 0:  # the whole line is a comment
            continue

        # labels:
        p = re.compile(SYMBOL_RE + ":")
        label_match = re.search(p, line)
        if label_match is not None:
            label = label_match.group(1)
            label = label.upper()
            labels[label] = i
            # now strip off the label:
            line = line.split(":", 1)[-1]
        # we've stripped extra whitespace, comments, and labels: now store
        # line:
        lines[i] = line
        # now tokenize!
        this_line = []
        (instr, code_pos) = get_instr(line, code_pos)
        this_line.append(instr)
        (ops, code_pos) = get_ops(line, code_pos, gdata)
        this_line.append(ops)
        tok_lines.append(this_line)
        i += 1
    return (tok_lines, labels)
