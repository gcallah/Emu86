"""
lex.py: performs lexical analysis
"""

import re
import pdb
from random import randrange
from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction, IntOutOfRng
from .errors import UnknownName, InvalidDataType, InvalidArgument, InvalidConVal
from .tokens import Location, Address, Register, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, Section, DupTok
from .tokens import QuestionTok, PlusTok, MinusTok, ConstantSign
from .tokens import DataType, StringTok, IntegerTok, OpenBracket, CloseBracket
from .tokens import Comma, OpenParen, CloseParen, FloatTok

SYM_RE = "([A-Za-z_][A-Za-z0-9_]*)"
sym_match = re.compile(SYM_RE)

FP_RE = "([0-9]+\.[0-9]+)"
fp_match = re.compile(FP_RE)

LABEL_RE = SYM_RE + ":"
label_match = re.compile(LABEL_RE)

DATA_SECT = ".data"
TEXT_SECT = ".text"

SEPARATORS = set([',', '(', ')', '[', ']', '+', '-'])

keywords_to_tokens = {
    "[": OpenBracket(), 
    "]": CloseBracket(),
    "(": OpenParen(),
    ")": CloseParen(),
    ",": Comma(),
    "+": PlusTok(),
    "-": MinusTok(),
    "?": QuestionTok()
}

def convert_hex_float(string):
    lst = string.split(".")
    int_part = int(lst[0], 16)
    float_part = float("." + lst[1])
    return int_part + float_part

def generate_reg_dict(vm, flavor):
    """
    Generates a dictionary
    Keys: register name 
    Values: Register token

    Args:
        vm: Virtual machine
        flavor: Flavor

    Returns: 
        A dictionary of (registers, register tokens)
    """
    registers = {}
    for reg in vm.registers:
        if flavor == "att":
            registers["%" + reg] = Register(reg, vm)
        else:
            registers[reg] = Register(reg, vm)
    return registers

def make_language_keys(vm, flavor):
    """
    Creates a dictionary of key terms

    Args: 
        vm: Virtual machine
        flavor: Assembly language

    Returns:
        A dictionary of key terms with associated tokens
    """
    language_keys = {}
    language_keys.update(keywords_to_tokens)
    language_keys.update(generate_reg_dict(vm, flavor))
    if flavor == "mips_asm" or flavor == "mips_mml":
        from .MIPS.key_words import key_words
        language_keys.update(key_words)
        return language_keys
    if flavor == "riscv": 
        from .RISCV.key_words import key_words
        language_keys.update(key_words)
    else:
        from .Intel.key_words import instructions
        language_keys.update(instructions)
        if flavor == "intel":
            from .Intel.key_words import intel_key_words
            language_keys.update(intel_key_words)
        else:
            from .Intel.key_words import att_key_words
            language_keys.update(att_key_words)
    return language_keys

def clean_list(lst):
    """
    Removes empty strings from a list of words

    Args:
        lst: List of words

    Returns:
        Cleaned list of words
    """
    while "" in lst:
        lst.remove("")

def split_code(code, flavor):
    """
    Splits code on regular expressions and on separators

    Args: 
        code: Line of code 

    Returns:
        A list of words
    """

    # split on regular expressions
    words = re.split("[ \t\r\n]+", code)
    index = 0

    # split on separator characters, such as commas
    while index < len(words):
        splitter = ""
        for character in words[index]:
            # determine the splitter
            if character in SEPARATORS and words[index] != character:
                splitter = character
                break
            # splitter specifically for AT&T
            elif (flavor == "att" and 
                     words[index] != "$" and 
                     character == "$"):
                splitter = "$"
                break
        # split if splitter is found
        if splitter != "":
            split_location = words[index].find(splitter)
            temp_words = [words[index][:split_location]]
            temp_words.append(splitter)
            temp_words.append(words[index][split_location + 1:])
            words = words[:index] + temp_words + words[index + 1:]
        else:
            index += 1

    # remove all empty strings from list that were made from splitting 
    # if splitter was first or last character
    clean_list(words)
    return words

def sep_line(code, i, flavor, data_sec, vm, language_keys):
    """
    Returns a list of tokens created 

    Args:
        code: Line of code 
        i: Line number of code
           Needed for determining label location
        flavor: AT&T or MIPS
        data_sec: Boolean, determines if we are in the data section
                  Needed to differentiate between label and symbol
        vm: Virtual machine
        key_words: Dictionary of key words for the flavor

    Returns:
        Tuple of the lexical analysis of the line
        The first member is the tokens and the second is the
        text of the code.
    """
    analysis = []
    words = split_code(code,flavor)

    for word in words:
# keyword:
        if word.upper() in language_keys:
            analysis.append(language_keys[word.upper()])
# section declaration:
        elif word[0] == ".":
            analysis.append(Section(word[1:]))
# string:
        elif word.find("'") != -1:
            analysis.append(StringTok(word))
# label / symbol:
        elif re.match(label_match, word) is not None:
            if flavor == "intel":
                vm.labels[word[:-1]] = i
            else:
                if data_sec:
                    analysis.append(NewSymbol(word[:-1], vm))
                else:
                    if flavor == "mips_asm" or flavor == "riscv":
                        vm.labels[word[:-1]] = i * 4
                    else:
                        vm.labels[word[:-1]] = i
        elif re.match(sym_match, word) is not None:

            analysis.append(NewSymbol(word, vm))
#Floating Points
        elif re.match(fp_match, word) is not None:
            if vm.base == "dec":
                #TODO: Screen shot to give me the floating point token class from token.py
                analysis.append(FloatTok(float(word)))
            else: #hexadecimal
                analysis.append(FloatTok(convert_hex_float(word)))
# Integers
        else:
            if vm.base == "dec":
                try:
                    if flavor == "att":
                        analysis.append(IntegerTok(int(word), False))
                    else:
                        analysis.append(IntegerTok(int(word)))
                except IntOutOfRng as err: 
                    raise IntOutOfRng(word)
                except:
                    raise InvalidArgument(word)
            else:
                try:
                    if flavor == "att":
                        analysis.append(IntegerTok(int(word, 16), False))
                    else:
                        analysis.append(IntegerTok(int(word, 16)))
                except IntOutOfRng as err: 
                    raise IntOutOfRng(word)
                except:
                    raise InvalidArgument(word)
    return (analysis, code)

def sep_line_mml(code, i, vm, language_keys):
    """
    Returns a list of tokens created 

    Args:
        code: Line of code 
        i: Line number of code
           Needed for determining label location
        flavor: AT&T or MIPS
        data_sec: Boolean, determines if we are in the data section
                  Needed to differentiate between label and symbol
        vm: Virtual machine
        key_words: Dictionary of key words for the flavor

    Returns:
        Tuple of the lexical analysis of the line
        The first member is the tokens and the second is the
        text of the code.
    """
    analysis = []
    words = split_code(code, vm.flavor)

    for word in words:
# keyword:
        if word.upper() in language_keys:
            analysis.append(language_keys[word.upper()])
# Integers
        else:
            try:
                analysis.append(IntegerTok(int(word, 16)))
            except IntOutOfRng as err: 
                raise IntOutOfRng(word)
            except:
                raise InvalidArgument(word)
    return (analysis, code)

def lex(code, flavor, vm):
    """
    Lexical phase: tokenizes the code.

    Args:
        code: The code to lexically analyze.
        flavor: Coding language
        vm: virtual machine

    Returns:
        tok_lines: the tokenized version
    """
    lines = code.split("\n")
    pre_processed_lines = []
    tok_lines = []  # this will hold the tokenized version of the code
    i = 0
    add_to_ip = True
    data_sec = False    #used for AT&T version
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
# create language-specific dictionary:
        language_keys = make_language_keys(vm, flavor)
        if flavor == "mips_mml":
            tok_lines.append(sep_line_mml(line, i, vm, language_keys))
        else:
            tok_lines.append(sep_line(line, i, flavor, data_sec, 
                                      vm, language_keys))
        if line == ".data":
            add_to_ip = False
            data_sec = True
            continue
        if line == ".text":
            add_to_ip = True
            data_sec = False
            continue

        # we count line numbers to store label jump locations:
        if add_to_ip:
            i += 1
    
    return tok_lines
