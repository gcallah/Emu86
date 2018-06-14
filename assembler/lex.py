"""
lex.py: performs lexical analysis
"""

import re
import pdb
from random import randrange
from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName, InvalidDataType
from .parse import instructions, dtype_info, DONT_INIT, sym_match, label_match
from .tokens import Location, Address, Register, IntOp, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, SymbolAddress
from .arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .arithmetic import Shr, Notf, Andf, Orf, Xor, Neg
from .control_flow import Cmpf, Je, Jne, Jmp, FlowBreak, Call, Ret
from .control_flow import Jg, Jge, Jl, Jle
from .data_mov import Mov, Pop, Push, Lea
from .interrupts import Interrupt
from .virtual_machine import MEM_SIZE


DATA_SECT = ".data"
TEXT_SECT = ".text"

DELINSIDERS = set([' ', ',', '(', ')', '\n', '\r', '\t',])

def sep_line (code, i, vm):
    """
    Returns a list of tokens created 

    Args:
        code: Line of code 
        i: Line number of code
           Needed for determining label location
        vm: Virtual machine

    Returns:
        Tuple of the lexical analysis of the line
    """
    analysis = []
    index = 0
    start = 0
    end = 1
    while end <= len(code):
        if code[start] in DELINSIDERS:
            start += 1
            end += 1
        else: 
            if end != len(code) and code[end] not in DELINSIDERS:
                end += 1
            else:
                word = code[start:end].strip(" ,\n\t\r")
                if word == ".data":
                    analysis.append(DATA_SECT)
                elif word == ".text":
                    analysis.append(TEXT_SECT)
                elif word in dtype_info:
                    analysis.append (word)
                elif word.upper() in instructions:
                    analysis.append(instructions[word.upper()])
                elif word.upper() in vm.registers:
                    analysis.append(Register(word.upper(), vm))
                elif word.find("[") != -1:
                    first_brack = word.find("[")
                    last_brack = word.find("]")
                    plus_sign = word.find("+")
                    address = word[first_brack + 1:last_brack]
                    if plus_sign != -1 and plus_sign < last_brack:
                        address = word[first_brack + 1:plus_sign]
                    if first_brack == 0:
                        if address.upper() in vm.registers:
                            if plus_sign == -1:
                                analysis.append(RegAddress(address.upper(), vm))
                            else:
                                analysis.append(RegAddress(address.upper(), 
                                                vm, int(word[plus_sign + 1:
                                                                 last_brack])))
                        elif address in vm.memory: 
                            analysis.append(Address(address, vm))
                        else:
                            raise InvalidMemLoc(address)
                    else:
                        if re.search(sym_match, word[:first_brack]):
                            if address.upper() in vm.registers:
                                analysis.append(SymbolAddress(word[:first_brack],
                                                Register(address.upper(), vm)))
                            else:
                                analysis.append(SymbolAddress(word[:first_brack], int(address)))
                elif word == "DUP":
                    analysis.append(word)
                elif re.search(label_match, word) is not None:
                    vm.labels[word[:word.find(":")]] = i
                elif re.search(sym_match, word) is not None:
                    if word in vm.labels:
                        analysis.append(Label(word, vm))
                    else:
                        analysis.append(NewSymbol(word, vm))
                elif word.find("'") != -1:
                    analysis.append(word)
                elif word == DONT_INIT:
                    analysis.append (DONT_INIT)
                else:
                    try:
                        analysis.append(IntOp(int(word)))
                    except Exception:
                        raise InvalidOperand(word)
                start = end + 1 
                end = start + 1
    return (analysis, code)


def lex(code, vm):
    """
    Lexical phase: tokenizes the code.
    Args:
        code: The code to lexically analyze.
        vm: virtual machine

    Returns:
        tok_lines: the tokenized version
    """
    lines = code.split("\n")
    pre_processed_lines = []
    tok_lines = []  # this will hold the tokenized version of the code
    i = 0
    add_to_i = True
    for line in lines:
        # comments:
        comm_start = line.find(";")
        if comm_start > 0:  # -1 means not found
            line = line[0:comm_start]
        elif comm_start == 0:  # the whole line is a comment
            continue

        # strip AFTER comments to handle blanks between code and ;
        line = line.strip()
        if len(line) == 0:  # blank lines ok; just skip 'em
            continue
            
        pre_processed_lines.append(line)

    # we've stripped extra whitespace, comments, and labels: 
    # now perform lexical analysis
    for line in pre_processed_lines:
        tok_lines.append(sep_line(line, i, vm))
        if line == ".data":
            add_to_i = False
            continue
        if line == ".text":
            add_to_i = True
            continue
        # we count line numbers to store label jump locations:
        if add_to_i:
            i += 1
    return tok_lines

