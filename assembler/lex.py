"""
lex.py: performs lexical analysis
"""

import re
from .errors import IntOutOfRng, InvalidArgument
from .tokens import Register, NewSymbol, Section
from .tokens import QuestionTok, PlusTok, MinusTok
from .tokens import StringTok, IntegerTok, OpenBracket, CloseBracket
from .tokens import Comma, OpenParen, CloseParen, FloatTok

# for floating point to binary and back
import struct
import binascii

SYM_RE = "([A-Za-z_][A-Za-z0-9_]*)"
sym_match = re.compile(SYM_RE)

FP_RE = "([0-9]+\.[0-9]+)"  # noqa
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

# def convert_hex_float(string):
#     lst = string.split(".")
#     int_part = int(lst[0], 16)
#     float_part = float("." + lst[1])
#     return int_part + float_part


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


# to convert the ieee 754 hex back to the actual float value
def hex_to_float(h):
    h2 = h[2:]
    h2 = binascii.unhexlify(h2)
    return struct.unpack('>f', h2)[0]


# for double precision (64 bits) fps
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]   # noqa


def f_to_b64(value):
    if (value == 0):
        return "0"*64
    val = struct.unpack('q', struct.pack('d', value))[0]
    return getBin(val)


def b_to_f(value):
    if (value == "0"*64):
        return 0.0
    hx = hex(int(value, 2))
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]


def generate_reg_dict(vm):
    """
    Generates a dictionary
    Keys: register name
    Values: Register token

    Args:
        vm: Virtual machine

    Returns:
        A dictionary of (registers, register tokens)
    """
    registers = {}
    if vm.flavor != 'wasm':
        for reg in vm.registers:
            if vm.flavor == "att":
                registers["%" + reg] = Register(reg, vm)
            else:
                registers[reg] = Register(reg, vm)
    return registers


def generate_float_stack_dict(vm):
    """
    Generates a dictionary
    Keys: register name
    Values: Register token

    Args:
        vm: Virtual machine

    Returns:
        A dictionary of (registers, register tokens)
    """
    registers = {}

    # for i in range(8):
    #     registers['ST'+str(i)] = NewSymbol('ST'+str(i))
    for reg in vm.fp_stack_registers:
        registers[reg] = Register(reg, vm)

    return registers


def make_language_keys(vm):
    """
    Creates a dictionary of key terms

    Args:
        vm: Virtual machine

    Returns:
        A dictionary of key terms with associated tokens
    """
    language_keys = {}
    language_keys.update(keywords_to_tokens)

    language_keys.update(generate_reg_dict(vm))
    if vm.flavor == "mips_asm" or vm.flavor == "mips_mml":
        from .MIPS.key_words import key_words
        language_keys.update(key_words)
        return language_keys
    elif vm.flavor == "riscv":
        from .RISCV.key_words import key_words
        language_keys.update(key_words)
    elif vm.flavor == 'wasm':
        from .WASM.key_words import key_words
        language_keys.update(key_words)
    else:
        from .Intel.key_words import instructions
        language_keys.update(instructions)
        if vm.flavor == "intel":
            # language_keys.update(generate_float_stack_dict(vm, flavor))
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


def split_code(code, vm):
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
            elif (vm.flavor == "att" and
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


def sep_line(code, line_num, i, data_sec, vm, language_keys):
    """
    Returns a list of tokens created

    Args:
        code: Line of code
        line_num: Line number of code, including the data section
        i: Line number of code
           Needed for determining label location
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
    words = split_code(code, vm)
    # for i in range(len(words)):  #fixes parsing error with negative floats
    #     if words[i]=='-':
    #         words[i+1]='-'+words[i+1]
    # words = [x for x in words if x!='-']
    data_type = None
    for word in words:
        # keyword:
        if word.upper() in language_keys:
            analysis.append(language_keys[word.upper()])
            data_type = word
        # section declaration:
        elif word[0] == ".":
            analysis.append(Section(word[1:]))
        # string:
        elif word.find("'") != -1:
            analysis.append(StringTok(word))
        # label / symbol:
        elif re.match(label_match, word) is not None:
            if vm.flavor == "intel":
                vm.labels[word[:-1]] = i
            else:
                if data_sec:
                    analysis.append(NewSymbol(word[:-1], vm))
                else:
                    if vm.flavor == "mips_asm" or vm.flavor == "riscv":
                        vm.labels[word[:-1]] = i * 4
                    else:
                        vm.labels[word[:-1]] = i
        elif re.match(sym_match, word) is not None:
            analysis.append(NewSymbol(word, vm))
        # Floating Points
        elif re.match(fp_match, word) is not None:
            # default is float (single precision) if user doesnt say
            if (data_type != ".float" and data_type != ".double" and
                    data_type != "REAL4" and data_type != "REAL8"):
                data_type = ".float"
            if vm.base == "dec":
                # TODO: Screen shot to give me the
                # floating point token class from token.py
                analysis.append(FloatTok(data_type=data_type, val=float(word)))
            else:   # hexadecimal

                if data_type == ".float":

                    analysis.append(FloatTok(data_type=data_type,
                                             val=float_to_hex(float(word))))
                elif data_type == ".double":
                    analysis.append(FloatTok(data_type=data_type,
                                             val=f_to_b64(float(word))))
        # Integers
        else:
            if vm.base == "dec":
                try:
                    if vm.flavor == "att":
                        analysis.append(IntegerTok(int(word), False))
                    else:
                        analysis.append(IntegerTok(int(word)))
                except IntOutOfRng:
                    raise IntOutOfRng(word, line_num)
                except Exception:
                    raise InvalidArgument(word, line_num)
            else:
                try:
                    if vm.flavor == "att":
                        analysis.append(IntegerTok(int(word, 16), False))
                    else:
                        analysis.append(IntegerTok(int(word, 16)))
                except IntOutOfRng:
                    raise IntOutOfRng(word, line_num)
                except Exception:
                    raise InvalidArgument(word, line_num)
    return (analysis, code, line_num)


def sep_line_mml(code, line_num, i, vm, language_keys):
    """
    Returns a list of tokens created

    Args:
        code: Line of code
        line_num: Line number of code, including the data section
        i: Line number of code
           Needed for determining label location
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
    words = split_code(code, vm)

    for word in words:
        # keyword
        if word.upper() in language_keys:
            analysis.append(language_keys[word.upper()])
    # Integers
        else:
            try:
                analysis.append(IntegerTok(int(word, 16)))
            except IntOutOfRng:
                raise IntOutOfRng(word, line_num)
            except Exception:
                raise InvalidArgument(word, line_num)
    return (analysis, code, line_num)


def sep_line_wasm(code, line_num, i, vm, language_keys):
    """
    Returns a list of tokens created

    Args:
        code: Line of code
        line_num: Line number of code, including the data section
        i: Line number of text code
           Needed for determining label location
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
    words = split_code(code, vm)

    for word in words:
        # keyword
        if word in language_keys:
            analysis.append(language_keys[word])
        # variable symbol
        elif re.match(sym_match, word) is not None:
            analysis.append(NewSymbol(word, vm))
    # Integers
        else:
            try:
                analysis.append(IntegerTok(int(word)))
            except IntOutOfRng:
                raise IntOutOfRng(word, line_num)
            except Exception:
                raise InvalidArgument(word, line_num)
    return (analysis, code, line_num)


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
    add_to_ip = True
    data_sec = False    # used for AT&T version
    for index in range(len(lines)):
        line = lines[index]
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

        # index starts at 0, line numbers start at 1
        pre_processed_lines.append([line, index + 1])

    # we've stripped extra whitespace, comments, and labels:
    # now perform lexical analysis
    for line, line_num in pre_processed_lines:
        # create language-specific dictionary:
        language_keys = make_language_keys(vm)
        if vm.flavor == "mips_mml":
            tok_lines.append(sep_line_mml(line, line_num, i,
                                          vm, language_keys))
        elif vm.flavor == "wasm":
            tok_lines.append(sep_line_wasm(line, line_num, i,
                                           vm, language_keys))
        else:
            tok_lines.append(sep_line(line, line_num, i, data_sec,
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
