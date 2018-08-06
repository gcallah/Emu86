"""
parse.py: creates parse tree.
"""

import re
import pdb
from random import randrange

from .lex import DONT_INIT
from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName, InvalidDataType, InvalidSection
from .errors import InvalidArgument, MissingData, InvalidDataVal, MissingComma
from .errors import MissingOpenParen, MissingCloseParen, MissingOpenBrack
from .errors import MissingCloseBrack, MissingOps, InvalidPc, MissingPc
from .tokens import Location, Address, Register, IntegerTok, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, Section, DataType
from .tokens import StringTok, Comma, OpenParen, CloseParen, DupTok, QuestionTok
from .tokens import OpenBracket, CloseBracket, PlusTok, MinusTok, ConstantSign
from .Intel.control_flow import Ret
from .MIPS.interrupts import Syscall
from .virtual_machine import MEM_SIZE

TOKENS = 0
CODE = 1

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
    """
    If token seen is an integer, determine by flavor whether 
    to return the integer token or return an address token

    Args:
        token_line: Line of code
        pos: Position where integer token is seen
        flavor: Assembly language
        vm: Virtual machine

    Returns:
        Integer or address token, next positon to look at
    """
    if flavor == "intel":
        return (token_line[pos], pos + 1)
    elif (pos + 1 < len(token_line) and 
          isinstance(token_line[pos + 1], OpenParen)):
        reg = None
        disp = None
        if flavor == "att":
            reg, disp, pos = get_address_att(token_line, 
                                             pos + 2, vm, 
                                             token_line[pos].get_val())
        else:
            reg, disp, pos = get_address_mips(token_line, 
                                              pos + 2, vm, 
                                              token_line[pos].get_val())
        if reg: 
            return (RegAddress(reg.get_nm(), 
                               vm, disp, 
                               reg.get_multiplier()), pos)
        else:
            return (Address(hex(disp).split('x')[-1].upper(), 
                            vm), pos)
    else:
        return (token_line[pos], pos + 1)

def symbol_token(token_line, pos, flavor, vm):
    """
    If token seen is a symbol, determine by flavor whether 
    to return the symbol token or return an address token

    Args:
        token_line: Line of code
        pos: Position where integer token is seen
        flavor: Assembly language
        vm: Virtual machine

    Returns:
        Symbol or address token, next positon to look at
    """
    if flavor != "mips":
        return (Symbol(token_line[pos].get_nm(), vm), pos + 1)
    elif (pos + 1 < len (token_line) and 
          isinstance(token_line[pos + 1], OpenParen)):
        reg, disp, pos = get_address_att(token_line, 
                                      pos + 2, vm, 
                                      vm.symbols[token_line[pos].get_nm()])
        if reg: 
            return (RegAddress(reg.get_nm(), 
                               vm, disp, 
                               reg.get_multiplier()), pos)
        else:
            return (Address(hex(disp).split('x')[-1].upper(), 
                            vm), pos)
    else:
        return (Symbol(token_line[pos].get_nm(), vm), pos + 1)

def is_start_address(token_line, pos, flavor):
    """ 
    Determines at current location if there is an address

    Args:
        token_line: Line of code
        pos: Position of possible address
        flavor: Assembly langauge

    Returns:
        True if address seen, False otherwise
    """
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

def is_str_termin(token_line, pos):
    if not isinstance(token_line[pos], IntegerTok):
        return False
    # check if following is an Integer with value of 0
    elif (token_line[pos].get_val() != 0):
        return False
    return True

NUM_STR_TOKS = 3
COMMA_POS = 1
TERM_POS = 2

def parse_string_token(token_line, pos):
    """
    Creates a list of the string token's ASCII values

    Args: 
        token_line: List of data tokens
        pos: Position of string token

    Returns:
        List of ASCII values, followed by a 0 
    """
    if len(token_line) < pos + NUM_STR_TOKS:
        raise MissingData()
    elif not isinstance(token_line[pos + COMMA_POS], Comma):
        raise MissingComma()
# is string terminated properly?
    elif not is_str_termin(token_line, pos + TERM_POS):
        raise InvalidDataVal(str(token_line[pos + TERM_POS].get_val()))

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
    Creates a list of values for each variable when it is declared.

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

def parse_data_token(token_line, vm, flavor, mem_loc):
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
        if vm.get_data_init() == "on":
            vm.memory[hex(mem_loc).split('x')[-1].upper()] = value
        if flavor == "mips":
            mem_loc += 4
        else:
            mem_loc += 1
    return mem_loc

def get_term(token_line, pos, vm):
    """
    Returns the next term of the expression

    Args:
        token_line: Line of code
        pos: Position of next term to be found
        vm: Virtual machine

    Returns:
        Next term token, position of token
    """
    # call function again to get the negated term
    if isinstance(token_line[pos], MinusTok):
        try:
            token_line[pos + 1].negate_val()
            return get_term(token_line, pos + 1, vm)
        except:
            raise InvalidArgument(token_line[pos].get_nm())
    # integer or register term
    elif (isinstance(token_line[pos], IntegerTok) or 
          isinstance(token_line[pos], Register)):
        return (token_line[pos], pos)
    # symbol term
    elif isinstance(token_line[pos], NewSymbol):
        if token_line[pos].get_nm() in vm.symbols:
            return (Symbol(token_line[pos].get_nm(), vm), pos)
        else:
            raise InvalidMemLoc(token_line[pos].get_nm())
    else:
        raise InvalidMemLoc(token_line[pos].get_nm())

REG = 0
DISP_VAL = 1
POSITION = 2

def get_expression(token_line, pos, vm, reg):
    """
    Returns the register and the evaluated expression 

    Args:
        token_line: Line of code
        pos: Position of address expression
        vm: Virtual machine

    Returns:
        Found register, integer value of expression, next position
    """
    if len(token_line) < pos + 2:
        return MissingOps
    left, pos = get_term(token_line, pos, vm)
    if isinstance(left, Register):
        reg = left
    next_term = token_line[pos + 1]
    if isinstance(next_term, PlusTok):
        next_val_pos = get_expression(token_line, pos + 2, vm, reg)
        return (next_val_pos[REG], left.get_val() + next_val_pos[DISP_VAL],
                next_val_pos[POSITION])
    elif isinstance(next_term, MinusTok):
        next_val_pos = get_expression(token_line, pos + 2, vm, reg)
        return (next_val_pos[REG], left.get_val() - next_val_pos[DISP_VAL],
                next_val_pos[POSITION])
    else:
        return (reg, left.get_val(), pos + 1)

def get_expr_mips(token_line, pos, vm):
    """
    Returns address expression for MIPS

    Args:
        token_line: Line of code
        pos: Position of address
        vm: Virtual machine

    Returns:
        Expression, next position
    """

    if pos >= len(token_line):
        raise MissingOps()
    left, pos = get_term(token_line, pos, vm)
    if isinstance(left, Register) or isinstance(left, IntegerTok):
        return (left, pos + 1)
    else:
        raise InvalidMemLoc(left.get_nm())

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

    if pos >= len(token_line):
        raise InvalidMemLoc("")
    reg = None
    disp = 0
    reg, disp, pos = get_expression(token_line, pos, vm, reg)
    if pos >= len(token_line):
        raise MissingCloseBrack()
    elif isinstance(token_line[pos], CloseBracket):
        pos += 1
        return (reg, disp, pos)
    else:
        raise InvalidMemLoc(token_line[pos].get_nm())

def get_address_att(token_line, pos, vm, disp = 0):
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
    reg = None
    closeParen = False 
    sec_reg = None
    count = 0 # can only have at most 2 regs!
    # check other elements within bracket
    while True:
        if state == NEED_VAL:
            if pos >= len(token_line):
                raise MissingOps()
            # if Integer
            elif isinstance(token_line[pos], IntegerTok):
                if reg:
                    if reg == token_line[pos - 2]:
                        reg.set_multiplier(token_line[pos].get_val())
                    elif (sec_reg == token_line[pos - 2] and 
                          isinstance(sec_reg, Register)):
                        sec_reg.set_multiplier(token_line[pos].get_val())
                    else: 
                        raise InvalidArgument(token_line[pos].get_nm())
                else:
                    try:
                        if isinstance(token_line[pos + 1], CloseParen):
                            disp += token_line[pos].get_val()
                            return (reg, disp, pos + 2)
                        else:
                            raise MissingCloseParen()
                    except:
                         raise MissingCloseParen()
                pos += 1
                state = NEED_COMMA_OR_CLOSE_PAREN
            # if reg
            elif isinstance(token_line[pos], Register):
                count += 1
                if count > 2:
                    raise InvalidMemLoc(token_line[pos].get_nm())
                else:
                    if reg:
                        sec_reg = token_line[pos]
                    else:
                        reg = token_line[pos]
                    pos += 1
                    state = NEED_COMMA_OR_CLOSE_PAREN
            # if Symbol, ex: (x)
            elif isinstance(token_line[pos], NewSymbol):
                if token_line[pos].get_nm() in vm.symbols:
                    disp += vm.symbols[token_line[pos].get_nm()]
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
                if sec_reg:
                    return (reg, [disp, sec_reg], pos + 1)
                return (reg, disp, pos + 1)
            else:
                raise InvalidMemLoc(token_line[pos].get_nm())

def get_address_mips(token_line, pos, vm, disp = 0):
    """
    Converts a sublist of the tokenized instruction into 
    corresponding address token for MIPS

    Args:
        token_line: List of instruction tokens
        pos: Beginning position in list
        vm: Virtual machine

    Returns: 
        Address token 
    """

    if pos >= len(token_line):
        raise InvalidMemLoc("")
    reg = None
    int_disp = 0
    value, pos = get_expr_mips(token_line, pos, vm)
    if isinstance(value, IntegerTok):
        int_disp += value.get_val()
    else:
        reg = value
    if pos >= len(token_line):
        raise MissingCloseParen()
    elif isinstance(token_line[pos], CloseParen):
        return (reg, disp, pos + 1)
    else:
        raise InvalidMemLoc(token_line[pos].get_nm())

def get_address_location(token_line, pos, flavor, vm):
    """
    Retrieves address at current position in code 
    Retrieves address by coding language

    Args:
        token_line: List of the tokenized instruction
        pos: Beginning pos of list
        flavor: Coding language
        vm: Virtual machine

    Returns: 
        RegAddress or Address token, 
        position of next item in instruction
    """
    reg = None
    disp = 0
    if flavor == "intel":
        reg, disp, pos = get_address(token_line, pos, vm)
    elif flavor == "att":
        reg, disp, pos = get_address_att(token_line, pos, vm)
    else: 
        reg, disp, pos = get_address_mips(token_line, pos, vm)
    if reg:
        return (RegAddress(reg.get_nm(), vm, 
                           disp, reg.get_multiplier()), pos)
    else:
        # eliminates negative memory locations
        if disp < 0:
            raise InvalidMemLoc(str(disp))
        return (Address(hex(disp).split('x')[-1].upper(), vm), 
                pos)

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
        if flavor != "att":
            raise InvalidArgument("$")
        else:
            try: 
                if isinstance(token_line[pos + 1], MinusTok):
                    token_line[pos + 2].negate_val()
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
            return symbol_token(token_line, pos, flavor, vm)
        else:
            raise UnknownName(token_line[pos].get_nm())
    elif is_start_address(token_line, pos, flavor):
        return get_address_location (token_line, pos + 1, flavor, vm)
    else:
        raise InvalidArgument(token_line[pos].get_nm())

def get_mips_pc(token_line, pos):
    """
    Returns the PC counter of the instruction

    Args:
        token_line: Line of code
        pos: Position of PC counter

    Returns:
        Integer token of PC counter value
    """
    if not isinstance(token_line[pos], IntegerTok):
        raise MissingPC()
    elif token_line[pos].get_val() % 4 != 0:
        raise InvalidPc(str(token_line[pos].get_val()))
    else:
        return token_line[pos]

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
    if flavor == "mips":
        token_instruction.append(get_mips_pc(token_line, pos))
        pos += 1
    if not isinstance(token_line[pos], Instruction):
        raise InvalidInstruction(token_line[pos].get_nm())
    token_instruction.append(token_line[pos])
    pos += 1 
    if isinstance(token_line[-1], Ret):
        state = NEED_COMMA_OR_END
    elif isinstance(token_line[-1], Syscall):
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
    ip_init = None
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
        if parse_data:
            mem_loc = parse_data_token(tokens[0], vm, flavor, mem_loc)
        elif parse_text:
            vm.set_data_init("off")
            parsed_unit = parse_exec_unit(tokens[0], flavor, vm)
            token_instrs.append((parsed_unit, tokens[1]))
            if flavor == "mips" and ip_init == None:
                ip_init = token_instrs[0][TOKENS][0].get_val()
                vm.start_ip = ip_init
    return token_instrs
