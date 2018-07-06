"""
parse.py: creates parse tree.
"""

import re
import pdb
from random import randrange

from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName, InvalidDataType, InvalidSection
from .errors import InvalidArgument, MissingData, InvalidDataVal, MissingComma
from .errors import MissingOpenParen, MissingCloseParen, MissingOpenBrack
from .errors import MissingCloseBrack, MissingOps
from .tokens import Location, Address, Register, IntegerTok, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, Section, DataType
from .tokens import StringTok, Comma, OpenParen, CloseParen, DupTok, QuestionTok
from .tokens import OpenBracket, CloseBracket, PlusTok, MinusTok, ConstantSign
from .Intel.control_flow import Ret
from .virtual_machine import MEM_SIZE

TOKENS = 0
CODE = 1

SYM_RE = "([A-Za-z_][A-Za-z0-9_]*)"
sym_match = re.compile(SYM_RE)
LABEL_RE = SYM_RE + ":"
label_match = re.compile(LABEL_RE)

DATA_SECT = ".data"
TEXT_SECT = ".text"

DONT_INIT = "?"

MAX_BYTE = 255
MAX_SHORT = 65535
MAX_LONG = 4294967295

BYTES = 0
MAX_VAL = 1
dtype_info = {
    "DB": (1, MAX_BYTE),
    "DW": (MEM_SIZE / 16, MAX_SHORT),   # we should revisit this choice
    "DD": (MEM_SIZE / 8, MAX_LONG), 
}

PARAM_TYPE = 1
PARAM_VAL = 0

def add_debug(s, vm):
    vm.debug += (s + "\n")

def number_token(token_line, pos, flavor, vm):
    if flavor == "intel":
        return (token_line[pos], pos + 1)
    else:
        if pos + 1 < len (token_line):
            if isinstance(token_line[pos + 1], OpenParen):
                register, displacement, pos = get_address_att(token_line, 
                                              pos + 2, vm, 
                                              token_line[pos].get_val())
                if register: 
                    return (RegAddress(register.get_nm(), 
                                       vm, displacement, 
                                       register.get_multiplier()), pos)
                else:
                    return (Address(hex(displacement).split('x')[-1].upper(), 
                                    vm), pos)
            else:
                return (token_line[pos], pos + 1)
        else:
            return (token_line[pos], pos + 1)

def is_start_address(token_line, pos, flavor):
    if isinstance(token_line[pos], OpenParen) and flavor == "att":
        return True
    elif isinstance(token_line[pos], OpenParen) and flavor == "mips":
        return True
    elif isinstance(token_line[pos], OpenBracket) and flavor == "intel":
        return True
    else:
        return False

def get_data_type(token_line, pos):
    """
    Returns the data type

    Args:
        token_line: List of data tokens
        pos: Position of list

    Returns: 
        Data type of variable
    """
    if pos >= len(token_line):
        raise MissingData()
    elif isinstance(token_line[pos], DataType):
        if token_line[pos].get_nm() not in dtype_info:
            raise InvalidDataType(token_line[pos].get_nm())
        else:
            return token_line[pos].get_nm()
    else:
        raise InvalidDataType(token_line[pos].get_nm())

def get_DUP_value(token_line, pos):
    """
    Finds the value to duplicate if found

    Args:
        token_line: List of data tokens
        pos: Beginning position to parse for DUP

    Returns:
        Integer value to duplicate
    """
    NEED_OPEN_PAREN = 0
    NEED_VAL = 1
    NEED_CLOSE_PAREN = 2
    state = NEED_OPEN_PAREN
    dup_value = None
    while pos < len(token_line):
        if state == NEED_OPEN_PAREN: 
            if isinstance(token_line[pos], OpenParen):
                state = NEED_VAL
                pos += 1
            else:
                raise MissingOpenParen()
        elif state == NEED_VAL:
            if isinstance(token_line[pos], QuestionTok):
                dup_value = DONT_INIT
            elif isinstance(token_line[pos], MinusTok):
                try:
                    token_line[pos + 1].negate_val()
                    pos += 1
                except: 
                    raise InvalidDataVal("-")
            elif isinstance(token_line[pos], IntegerTok):
                dup_value = token_line[pos].get_val()
                state = NEED_CLOSE_PAREN
                pos += 1
            else:
                raise MissingData()
        elif state == NEED_CLOSE_PAREN:
            if isinstance(token_line[pos], CloseParen):
                pos += 1 
                break
            else: 
                raise MissingCloseParen()

    return (dup_value, pos)

def parse_string_token(token_line, pos):
    """
    Creates a list of the string token's ASCII values

    Args: 
        token_line: List of data tokens
        pos: Position of string token

    Returns:
        List of ASCII values, followed by a 0 
    """
    if pos + 2 >= len(token_line):
        raise MissingData()
    # check if following is an Integer
    elif not isinstance(token_line[pos + 1], Comma):
        raise MissingComma()

    elif not isinstance(token_line[pos + 2], IntegerTok):
        raise InvalidDataVal(str(token_line[pos + 2].get_val()))
    # check if following is an Integer with value of 0
    elif (isinstance(token_line[pos + 2], IntegerTok) and 
             token_line[pos + 2].get_val() != 0):
        raise InvalidDataVal(str(token_line[pos + 2].get_val()))
    else:
        ascii_list = []
        for letter in token_line[pos].get_nm():
            if letter != "'":
                ascii_list.append(ord(letter))
        ascii_list.append(0)
        return (ascii_list, pos + 3)

def parse_dup_token(token_line, data_type, pos):
    """
    Parses integer token followed by DUP token

    Args: 
        token_line: List of data tokens
        data_type: Data type of variable
        pos = Position of integer token

    Returns:
        List of duplicated values
    """
    dup_list = []
    duplicate = token_line[pos].get_val()
    value, pos = get_DUP_value(token_line, pos + 2)
    for times in range(duplicate):
        if value == DONT_INIT:
            dup_list.append(randrange(0, 
                     dtype_info[data_type][MAX_VAL]))
        else:
            dup_list.append(value)
    return (dup_list, pos)

def get_values(token_line, data_type, pos):
    """
    Creates a list of values for each variable

    Args:
        token_line: List of data tokens
        data_type: Data type of variable
        pos: Beginning pos to parse from

    Returns:
        List of integer values
    """
    values_list = []
    if pos >= len(token_line):
        raise MissingData()

    # negate integer value if minus sign found
    elif isinstance(token_line[pos], MinusTok):
        try:
            token_line[pos + 1].negate_val()
            values_list.append(token_line[pos + 1].get_val())
            return (values_list, pos + 2)
        except:
            raise InvalidDataVal(token_line[pos].get_nm())
    elif isinstance(token_line[pos], IntegerTok):
        if pos + 1 < len(token_line):
            # if DUP token found
            if isinstance(token_line[pos + 1], DupTok):
                dup_list, pos = parse_dup_token(token_line, data_type, pos)
                values_list.extend(dup_list)
                return (values_list, pos)
            # otherwise return int
            else:
                return ([token_line[pos].get_val()], pos + 1)
        else:
            return ([token_line[pos].get_val()], pos + 1)

    # if value is a string token
    elif isinstance(token_line[pos], StringTok):
        ascii_list, pos = parse_string_token(token_line, pos)
        values_list.extend(ascii_list)
        return (values_list, pos)
    elif isinstance(token_line[pos], QuestionTok):
        values_list.append(randrange(0, dtype_info[data_type][MAX_VAL]))
        return (values_list, pos + 1)
    else:
        raise InvalidDataVal(token_line[pos].get_nm())

def parse_data_token(token_line, vm, mem_loc):
    """
    Parses data tokens 

    Args:
        token_line: List of data tokens
        vm: Virtual machine
        mem_loc: Starting memory storage location
    """
    NEED_VAL = 0
    NEED_COMMA_OR_END = 1
    pos = 0
    symbol = ""
    data_vals = []
    if not isinstance(token_line[pos], NewSymbol):
        raise InvalidArgument(token_line[pos].get_nm())
    else:
        symbol = token_line[pos].get_nm()
    pos += 1
    data_type = get_data_type(token_line, pos)
    pos += 1
    state = NEED_VAL
    while True: 
        if state == NEED_VAL:
            val, pos = get_values(token_line, data_type, pos)
            data_vals.extend(val)
            state = NEED_COMMA_OR_END
        elif state == NEED_COMMA_OR_END:
            if pos >= len(token_line):
                break
            elif isinstance(token_line[pos], Comma):
                state = NEED_VAL
                pos += 1
            else:
                MissingComma()

    # store memory location 
    vm.symbols[symbol] = mem_loc
    add_debug("Symbol table now holds " + str(mem_loc), vm)
    for value in data_vals:
        vm.memory[hex(mem_loc).split('x')[-1].upper()] = value
        mem_loc += 1
    return mem_loc


def get_address(token_line, pos, vm):
    """
    Converts a sublist of the tokenized instruction into 
    corresponding address token

    Args:
        token_line: List of instruction tokens
        pos: Beginning position in list
        vm: Virtual machine

    Returns: 
        Address token 
    """

    NEED_VAL = 0
    NEED_OP_OR_CLOSE_BRACK = 1
    if pos >= len(token_line):
        raise InvalidMemLoc("")
    state = NEED_VAL
    register = None
    displacement = 0
    closeBracket = False 
    args = 0
    # check other elements within bracket
    while True:
        if state == NEED_VAL:
            if pos >= len(token_line):
                raise MissingOps()
            # if Integer
            elif isinstance(token_line[pos], MinusTok):
                token_line[pos + 1].negate_val()
                pos += 1
            elif isinstance(token_line[pos], IntegerTok):
                args += 1
                if args > 2:
                    raise MissingCloseBrack()
                displacement += token_line[pos].get_val()
                pos += 1
                state = NEED_OP_OR_CLOSE_BRACK
            # if Register
            elif isinstance(token_line[pos], Register):
                args += 1
                if args > 2:
                    raise MissingCloseBrack()
                if register:
                    displacement = token_line[pos]
                else:
                    register = token_line[pos]
                pos += 1
                state = NEED_OP_OR_CLOSE_BRACK
            # if Symbol, ex: [x]
            elif isinstance(token_line[pos], NewSymbol):
                if token_line[pos].get_nm() in vm.symbols:
                    displacement += vm.symbols[token_line[pos].get_nm()]
                    pos += 1
                    state = NEED_OP_OR_CLOSE_BRACK
                else:
                    raise InvalidMemLoc(token_line[pos].get_nm())
            else:
                raise InvalidMemLoc(token_line[pos].get_nm())
        else: 
            if pos >= len(token_line):
                raise MissingCloseBrack()
            elif isinstance(token_line[pos], MinusTok):
                token_line[pos + 1].negate_val()
                pos += 1
                state = NEED_VAL
            elif isinstance(token_line[pos], PlusTok):
                pos += 1
                state = NEED_VAL
            elif isinstance(token_line[pos], CloseBracket):
                pos += 1
                return (register, displacement, pos)
            else:
                raise InvalidMemLoc(token_line[pos].get_nm())

def get_address_att(token_line, pos, vm, displacement = 0):
    """
    Converts a sublist of the tokenized instruction into 
    corresponding address token

    Args:
        token_line: List of instruction tokens
        pos: Beginning position in list
        vm: Virtual machine

    Returns: 
        Address token 
    """

    NEED_VAL = 0
    NEED_COMMA_OR_CLOSE_PAREN = 1
    if pos >= len(token_line):
        raise InvalidMemLoc("")
    state = NEED_VAL
    register = None
    closeParen = False 
    second_register = None
    count = 0 # can only have at most 2 registers!
    # check other elements within bracket
    while True:
        if state == NEED_VAL:
            if pos >= len(token_line):
                raise MissingOps()
            # if Integer
            elif isinstance(token_line[pos], IntegerTok):
                if register:
                    if register == token_line[pos - 2]:
                        register.set_multiplier(token_line[pos].get_val())
                    elif (second_register == token_line[pos - 2] and 
                          isinstance(second_register, Register)):
                        second_register.set_multiplier(token_line[pos].get_val())
                    else: 
                        raise InvalidArgument(token_line[pos].get_nm())
                else:
                    try:
                        if isinstance(token_line[pos + 1], CloseParen):
                            displacement += token_line[pos].get_val()
                            return (register, displacement, pos + 2)
                        else:
                            raise MissingCloseParen()
                    except:
                         raise MissingCloseParen()
                pos += 1
                state = NEED_COMMA_OR_CLOSE_PAREN
            # if Register
            elif isinstance(token_line[pos], Register):
                count += 1
                if count > 2:
                    raise InvalidMemLoc(token_line[pos].get_nm())
                else:
                    if register:
                        second_register = token_line[pos]
                    else:
                        register = token_line[pos]
                    pos += 1
                    state = NEED_COMMA_OR_CLOSE_PAREN
            # if Symbol, ex: [x]
            elif isinstance(token_line[pos], NewSymbol):
                if token_line[pos].get_nm() in vm.symbols:
                    displacement += vm.symbols[token_line[pos].get_nm()]
                    pos += 1
                    state = NEED_COMMA_OR_CLOSE_PAREN
                else:
                    raise InvalidMemLoc(token_line[pos].get_nm())
            else:
                raise InvalidMemLoc(token_line[pos].get_nm())
        else: 
            if pos >= len(token_line):
                raise MissingCloseParen()
            if isinstance(token_line[pos], Comma):
                pos += 1
                state = NEED_VAL
            elif isinstance(token_line[pos], CloseParen):
                if second_register:
                    return (register, [displacement, second_register], pos + 1)
                return (register, displacement, pos + 1)
            else:
                raise InvalidMemLoc(token_line[pos].get_nm())

def get_op(token_line, pos, flavor, vm):
    """
    Retrieves operand of instruction

    Args:
        token_line: List of the tokenized instruction
        pos: Beginning pos of list
        flavor: Coding language
        vm: Virtual machine

    Returns: 
        Operand token, position of next item in instruction
    """
    if pos >= len(token_line):
        raise MissingOps()
    elif isinstance(token_line[pos], Register):
        return (token_line[pos], pos + 1)
    elif isinstance(token_line[pos], ConstantSign):
        try:
            if isinstance(token_line[pos + 1], MinusTok):
                token_line[pos + 2].negate_val()
                if flavor == "intel":
                    return (token_line[pos + 2], pos + 3)
                elif flavor == "att":
                    return get_op(token_line, pos + 2, flavor, vm)
            elif isinstance(token_line[pos + 1], IntegerTok):
                return (token_line[pos + 1], pos + 2)
            else:
                raise InvalidArgument("$")
        except:
            raise InvalidArgument("$")
    elif isinstance(token_line[pos], MinusTok):
        try:
            token_line[pos + 1].negate_val()
            if flavor == "intel":
                return (token_line[pos + 1], pos + 2)
            else:
                return get_op(token_line, pos + 1, flavor, vm)
        except:
            raise InvalidArgument("-")
    elif isinstance(token_line[pos], IntegerTok):
        return number_token(token_line, pos, flavor, vm)
    elif isinstance(token_line[pos], NewSymbol):
        if token_line[pos].get_nm() in vm.labels:
            return (Label(token_line[pos].get_nm(), vm), pos + 1)
        elif token_line[pos].get_nm() in vm.symbols:
            return (Symbol(token_line[pos].get_nm(), vm), pos + 1)
    elif is_start_address(token_line, pos, flavor):
        pos += 1
        register = None
        displacement = 0
        if flavor == "intel":
            register, displacement, pos = get_address(token_line, pos, vm)
        elif flavor == "att" or flavor == "mips":
            register, displacement, pos = get_address_att(token_line, pos, vm)
        if register:
            return (RegAddress(register.get_nm(), vm, 
                               displacement, register.get_multiplier()), pos)
        else:
            if displacement >= 256 or displacement < 0:
                raise InvalidMemLoc(str(displacement))
            return (Address(hex(displacement).split('x')[-1].upper(), vm), 
                    pos)
    else:
        raise InvalidArgument(token_line[pos].get_nm())

def parse_exec_unit(token_line, flavor, vm):
    """
    Parses instruction

    Args:
        token_line: Tokenized instruction
        vm: Virtual machine

    Returns: 
        List of tokens: instruction, operand, operand
    """
    NEED_OP = 0
    NEED_COMMA_OR_END = 1
    pos = 0
    token_instruction = []
    if not isinstance(token_line[pos], Instruction):
        raise InvalidInstruction(token_line[pos].get_nm())
    token_instruction.append(token_line[pos])
    pos += 1 
    if isinstance(token_instruction[0], Ret):
        state = NEED_COMMA_OR_END
    else:
        state = NEED_OP
    while True:
        if state == NEED_OP:
            # get_op will throw excep if no op present
            op, pos = get_op(token_line, pos, flavor, vm)
            token_instruction.append(op)
            state = NEED_COMMA_OR_END
        elif state == NEED_COMMA_OR_END:
            if pos >= len(token_line):
                break  # end of tokens
            elif isinstance(token_line[pos], Comma): 
                pos += 1
                state = NEED_OP
            else:
                raise MissingComma()
    if flavor == 'att' and len(token_instruction) > 2:
        switch_vals = token_instruction[1], token_instruction[2]
        token_instruction[1] = switch_vals[1]
        token_instruction[2] = switch_vals[0]
    return token_instruction

def parse(tok_lines, flavor, vm):
    """
    Parses the analysis obtained from lexical analysis

    Args:
        tok_lines: Lines containing each line of code
        vm: Virtual machine

    Returns:
        A list of parsed instructions
    """
    parse_data = False
    parse_text = True
    token_instrs = []
    mem_loc = 0 
    for tokens in tok_lines:
        if isinstance(tokens[0][TOKENS], Section):
            if tokens[0][TOKENS].get_nm() == "data":
                parse_data = True
                parse_text = False
                continue
            elif tokens[0][TOKENS].get_nm() == "text":
                parse_text = True
                parse_data = False
                continue
            else: 
                raise InvalidSection(tokens[0][TOKENS].get_nm())
        if parse_data and vm.get_ip() == 0:
            mem_loc = parse_data_token(tokens[0], vm, mem_loc)
        elif parse_text:
            token_instrs.append((parse_exec_unit(tokens[0], flavor, vm), 
                                 tokens[1]))
    return token_instrs
