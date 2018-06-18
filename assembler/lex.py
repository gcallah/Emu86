"""
lex.py: performs lexical analysis
"""

import re
import pdb
from random import randrange
from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName, InvalidDataType, InvalidArgument
from .parse import instructions, dtype_info, DONT_INIT, sym_match, label_match
from .tokens import Location, Address, Register, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, SymAddress, Section, DupTok
from .tokens import QuestionTok, PlusTok
from .tokens import DataType, StringTok, IntegerTok, OpenBracket, CloseBracket
from .tokens import Comma, OpenParen, CloseParen
from .arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .arithmetic import Shr, Notf, Andf, Orf, Xor, Neg
from .control_flow import Cmpf, Je, Jne, Jmp, FlowBreak, Call, Ret
from .control_flow import Jg, Jge, Jl, Jle
from .data_mov import Mov, Pop, Push, Lea
from .interrupts import Interrupt
from .virtual_machine import MEM_SIZE


DATA_SECT = ".data"
TEXT_SECT = ".text"

DELIMITERS = set([' ', '(', ')', '\n', '\r', '\t', ','])
SEPARATORS = set([',', '(', ')', '\n', '\r', '\t', '[', ']', '+'])

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

    words = code.split(" ")
    while index < len(words):
        words[index].strip(" \t\r\n")
        splitter = ""
        for character in words[index]:
            if character in SEPARATORS and words[index] != character:
                splitter = character
                break
        if splitter != "":
            split_location = words[index].find(splitter)
            temp_words = [words[index][:split_location]]
            temp_words.append(splitter)
            temp_words.append(words[index][split_location + 1:])
            words = words[:index] + temp_words + words[index + 1:]
        else:
            index += 1

    for word in words:
        if word != "" and word not in "\n\t\r":
            if word[0] == ".":
                analysis.append(Section(word[1:]))
            elif word in dtype_info:
                analysis.append(DataType(word))
            elif word.upper() in instructions:
                analysis.append(instructions[word.upper()])
            elif word.upper() in vm.registers:
                analysis.append(Register(word.upper(), vm))
            elif word == "[":
                analysis.append(OpenBracket())
            elif word == "(":
                analysis.append(OpenParen())
            elif word == "]":
                analysis.append(CloseBracket())
            elif word == ")":
                analysis.append(CloseParen())
            elif word == ",":
                analysis.append(Comma())
            elif word == "+":
                analysis.append(PlusTok())
            elif word == "DUP":
                analysis.append(DupTok(word))
            elif word.find("'") != -1:
                analysis.append(StringTok(word))
            elif word == DONT_INIT:
                analysis.append(QuestionTok())
            elif re.search(label_match, word) is not None:
                vm.labels[word[:word.find(":")]] = i
            elif re.search(sym_match, word) is not None:
                analysis.append(NewSymbol(word, vm))
            else:
                try:
                    analysis.append(IntegerTok(int(word)))
                except Exception:
                    raise InvalidArgument(word)
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

