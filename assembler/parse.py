"""
parse.py: creates parse tree.
"""

from random import randrange

from .errors import InvalidMemLoc, InvalidInstruction
from .errors import UnknownName, InvalidDataType, InvalidSection
from .errors import InvalidArgument, MissingData, InvalidDataVal, MissingComma
from .errors import MissingOpenParen, MissingCloseParen
from .errors import MissingCloseBrack, MissingOps, InvalidPc, MissingPc
from .errors import TooBigForSingle, TooBigForDouble
from .tokens import Address, Register, IntegerTok, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, Section, DataType
from .tokens import StringTok, Comma, DupTok, QuestionTok
from .tokens import OpenParen, CloseParen, OpenBracket, CloseBracket
from .tokens import PlusTok, MinusTok, ConstantSign
from .tokens import FloatTok
from .virtual_machine import MEM_SIZE

TOKENS = 0
CODE = 1
LINE_NUMBER = 2

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
    "REAL4": (1, MAX_BYTE),
    "REAL8": (1, MAX_BYTE),
    "DBL": (1, MAX_BYTE),
    "FL": (1, MAX_BYTE)
}

PARAM_TYPE = 1
PARAM_VAL = 0


def add_debug(s, vm):
    vm.debug += (s + "\n")


def minus_token(token_line, pos, line_num):
    """
    Negates the next token if minus token found

    Args:
        token_line: Line of code
        pos: Position of minus token
    """
    try:
        if isinstance(token_line[pos + 1], IntegerTok):
            token_line[pos + 1].negate_val()
        else:
            raise InvalidArgument("-", line_num)
    except Exception:
        raise InvalidArgument("-", line_num)


def register_token(token_line, pos, vm, line_num):
    if vm.flavor == "intel" or vm.flavor == "att":

        return (token_line[pos], pos + 1)
    elif (pos + 1 < len(token_line) and
          isinstance(token_line[pos + 1], OpenParen)):
        reg = None
        disp = None
        reg, disp, pos = get_address_mips(token_line, pos + 2, vm, line_num,
                                          token_line[pos])
        return (RegAddress(reg.get_nm(), vm, disp), pos)
    else:
        return (token_line[pos], pos + 1)


def number_token(token_line, pos, vm, line_num):
    """
    If token seen is an integer, determine by flavor whether
    to return the integer token or return an address token

    Args:
        token_line: Line of code
        pos: Position where integer token is seen
        vm: Virtual machine

    Returns:
        Integer or address token, next positon to look at
    """
    if vm.flavor == "intel":

        return (token_line[pos], pos + 1)
    elif (pos + 1 < len(token_line) and
          isinstance(token_line[pos + 1], OpenParen)):
        reg = None
        disp = None
        if vm.flavor == "att":
            reg, disp, pos = get_address_att(token_line, pos + 2,
                                             vm, line_num,
                                             token_line[pos].get_val(line_num))
        else:
            reg, disp, pos = get_address_mips(
                token_line, pos + 2,
                vm, line_num,
                token_line[pos].get_val(line_num))
        if reg:
            return (RegAddress(reg.get_nm(), vm, disp,
                               reg.get_multiplier()), pos)
        else:
            return (Address(hex(disp).split('x')[-1].upper(), vm), pos)
    elif vm.flavor == "att" and token_line[pos].con is False:
        mem_val = token_line[pos].get_val(line_num)
        return (Address(hex(mem_val).split('x')[-1].upper(), vm), pos + 1)
    else:
        return (token_line[pos], pos + 1)


def symbol_token(token_line, pos, vm, line_num):
    """
    If token seen is a symbol, determine by flavor whether
    to return the symbol token or return an address token

    Args:
        token_line: Line of code
        pos: Position where integer token is seen
        vm: Virtual machine

    Returns:
        Symbol or address token, next positon to look at
    """
    if vm.flavor != "mips_asm":
        return (Symbol(token_line[pos].get_nm(), vm), pos + 1)
    elif (pos + 1 < len(token_line) and
          isinstance(token_line[pos + 1], OpenParen)):
        reg, disp, pos = get_address_mips(token_line, pos + 2, vm, line_num,
                                          vm.symbols[token_line[pos].get_nm()])
        return (RegAddress(reg.get_nm(), vm, disp,
                           reg.get_multiplier()), pos)
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
    elif (isinstance(token_line[pos], OpenParen) and
          (flavor == "mips_asm" or flavor == "mips_mml")):
        return True
    elif isinstance(token_line[pos], OpenBracket) and flavor == "intel":
        return True
    else:
        return False


def get_data_type(token_line, pos, line_num):
    """
    Returns the data type

    Args:
        token_line: List of data tokens
        pos: Position of list

    Returns:
        Data type of variable
    """
    if pos >= len(token_line):
        raise MissingData(line_num)
    elif isinstance(token_line[pos], DataType):
        if token_line[pos].get_nm() not in dtype_info:
            raise InvalidDataType(token_line[pos].get_nm(), line_num)
        else:
            return token_line[pos].get_nm()
    else:
        raise InvalidDataType(token_line[pos].get_nm(), line_num)


def get_data_token(token_line, pos, line_num):
    """
    Returns the data token found

    Args:
        token_line: Line of code
        pos: Position to find data token

    Returns:
        Data value, next position
    """
    if pos >= len(token_line):
        raise MissingData(line_num)
    if isinstance(token_line[pos], MinusTok):
        try:
            if isinstance(token_line[pos + 1], IntegerTok):
                token_line[pos + 1].negate_val()
                return get_data_token(token_line, pos + 1, line_num)
            else:
                raise InvalidDataVal("-", line_num)
        except Exception:
            raise InvalidDataVal("-", line_num)
    elif isinstance(token_line[pos], IntegerTok):
        return token_line[pos].get_val(line_num), pos + 1
    elif isinstance(token_line[pos], FloatTok):
        if (token_line[pos].get_type() == ".float" and
                token_line[pos].get_val(line_num) > float(2 ** 22)):
            raise TooBigForSingle(str(token_line[pos].get_val(line_num)),
                                  line_num)
        if (token_line[pos].get_type() == ".double" and
                token_line[pos].get_val(line_num) > float(2 * 10 ** 14)):
            raise TooBigForDouble(str(token_line[pos].get_val(line_num)),
                                  line_num)
        return token_line[pos].get_val(line_num), pos + 1
    elif isinstance(token_line[pos], QuestionTok):
        return DONT_INIT, pos + 1
    else:
        raise InvalidArgument(token_line[pos].get_nm(), line_num)


def get_DUP_value(token_line, pos, line_num):
    """
    Finds the value to duplicate if found

    Args:
        token_line: List of data tokens
        pos: Beginning position to parse for DUP

    Returns:
        Integer value to duplicate, next position
    """
    if isinstance(token_line[pos], OpenParen):
        pos += 1
    else:
        raise MissingOpenParen(line_num)
    dup_value, pos = get_data_token(token_line, pos, line_num)
    if isinstance(token_line[pos], CloseParen):
        return dup_value, pos + 1
    else:
        raise MissingCloseParen(line_num)


def is_str_termin(token_line, pos, line_num):
    if not isinstance(token_line[pos], IntegerTok):
        return False
    # check if following is an Integer with value of 0
    elif (token_line[pos].get_val(line_num) != 0):
        return False
    return True


NUM_STR_TOKS = 3
COMMA_POS = 1
TERM_POS = 2


def parse_string_token(token_line, pos, line_num):
    """
    Creates a list of the string token's ASCII values

    Args:
        token_line: List of data tokens
        pos: Position of string token

    Returns:
        List of ASCII values, followed by a 0
    """
    if len(token_line) < pos + NUM_STR_TOKS:
        raise MissingData(line_num)
    elif not isinstance(token_line[pos + COMMA_POS], Comma):
        raise MissingComma(line_num)
# is string terminated properly?
    elif not is_str_termin(token_line, pos + TERM_POS, line_num):
        raise InvalidDataVal(str(token_line[pos + TERM_POS].get_val(line_num)),
                             line_num)

    else:
        ascii_list = []
        for letter in token_line[pos].get_nm():
            if letter != "'":
                ascii_list.append(ord(letter))
        ascii_list.append(0)
        return (ascii_list, pos + 3)


def parse_dup_token(token_line, data_type, pos, line_num):
    """
    Parses integer token followed by DUP token

    Args:
        token_line: List of data tokens
        data_type: Data type of variable
        pos = Position of integer token

    Returns:
        List of duplicated values
    """
    dup_list = None
    duplicate = token_line[pos].get_val(line_num)
    value, pos = get_DUP_value(token_line, pos + 2, line_num)
    if value == DONT_INIT:
        dup_list = [randrange(0, dtype_info[data_type][MAX_VAL])] * duplicate
    else:
        dup_list = [value] * duplicate
    return (dup_list, pos)


def get_values(token_line, data_type, pos, values_list, line_num):
    """
    Creates a list of values for each variable when it is declared.

    Args:
        token_line: List of data tokens
        data_type: Data type of variable
        pos: Beginning pos to parse from
        values_list: List of values

    Returns:
        List of integer values
    """
    if pos >= len(token_line):
        raise MissingData(line_num)
    elif isinstance(token_line[pos], StringTok):
        ascii_list, pos = parse_string_token(token_line, pos, line_num)
        values_list.extend(ascii_list)
    else:
        first_data, pos = get_data_token(token_line, pos, line_num)
        if first_data == DONT_INIT:
            values_list.append(randrange(0, dtype_info[data_type][MAX_VAL]))
        else:
            values_list.append(first_data)
    if pos >= len(token_line):
        return values_list, pos
    else:
        next_term = token_line[pos]
        if isinstance(next_term, DupTok):
            values_list.pop()
            dup_list, pos = parse_dup_token(token_line, data_type,
                                            pos - 1, line_num)
            values_list.extend(dup_list)
            try:
                next_term = token_line[pos]
            except Exception:
                return values_list, pos
        if isinstance(next_term, Comma):
            return get_values(token_line, data_type, pos + 1,
                              values_list, line_num)
        else:
            raise InvalidDataVal(token_line[pos].get_nm(), line_num)


def parse_data_token(token_line, vm, mem_loc, line_num):
    """
    Parses data tokens, assigns each value to a memory location

    Args:
        token_line: List of data tokens
        vm: Virtual machine
        mem_loc: Starting memory storage location

    Returns:
        Returns the next memory location to be used
    """
    pos = 0
    symbol = ""
    data_vals = []
    if not isinstance(token_line[pos], NewSymbol):
        raise InvalidArgument(token_line[pos].get_nm(), line_num)
    else:
        symbol = token_line[pos].get_nm()
    data_type = get_data_type(token_line, pos + 1, line_num)
    pos += 2
    data_vals, pos = get_values(token_line, data_type, pos,
                                data_vals, line_num)

    # store memory location
    vm.symbols[symbol] = mem_loc
    add_debug("Symbol table now holds " + str(mem_loc), vm)
    for value in data_vals:
        if vm.get_data_init() == "on":
            vm.memory[hex(mem_loc).split('x')[-1].upper()] = value
        if vm.flavor == "mips_asm" or vm.flavor == "riscv":
            mem_loc += 4
        else:
            mem_loc += 1
    return mem_loc


def get_term(token_line, pos, vm, line_num):
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
            return get_term(token_line, pos + 1, vm, line_num)
        except Exception:
            raise InvalidArgument(token_line[pos].get_nm(), line_num)
    # integer or register term
    elif (isinstance(token_line[pos], IntegerTok) or
          isinstance(token_line[pos], Register)):
        return (token_line[pos], pos)
    # symbol term
    elif isinstance(token_line[pos], NewSymbol):
        if token_line[pos].get_nm() in vm.symbols:
            return (Symbol(token_line[pos].get_nm(), vm), pos)
        else:
            raise InvalidMemLoc(token_line[pos].get_nm(), line_num)
    else:
        raise InvalidMemLoc(token_line[pos].get_nm(), line_num)


REG = 0
DISP_VAL = 1
POSITION = 2


def get_expr_intel(token_line, pos, vm, line_num, reg):
    """
    Returns the register and the evaluated expression

    Args:
        token_line: Line of code
        pos: Position of address expression
        vm: Virtual machine

    Returns:
        Register token, displacement, next position
    """
    if len(token_line) < pos + 2:
        return MissingOps(line_num)
    left, pos = get_term(token_line, pos, vm, line_num)
    if isinstance(left, Register):
        reg = left
    next_term = token_line[pos + 1]
    if isinstance(next_term, PlusTok):
        next_val_pos = get_expr_intel(token_line, pos + 2, vm, line_num, reg)
        return (next_val_pos[REG],
                left.get_val(line_num) + next_val_pos[DISP_VAL],
                next_val_pos[POSITION])
    elif isinstance(next_term, MinusTok):
        next_val_pos = get_expr_intel(token_line, pos + 2, vm, line_num, reg)
        return (next_val_pos[REG],
                left.get_val(line_num) - next_val_pos[DISP_VAL],
                next_val_pos[POSITION])
    else:
        return (reg, left.get_val(line_num), pos + 1)


SEC_REG = 0


def get_expr_att(token_line, pos, vm, line_num, reg, disp_list):
    """
    Returns address expression for AT&T

    Args:
        token_line: Line of code
        pos: Position of address
        vm: Virtual machine
        disp_list: List of displacements

    Returns:
        Register token, displacement(s), next position
    """
    if len(token_line) < pos + 2:
        return MissingOps(line_num)
    left, pos = get_term(token_line, pos, vm, line_num)

    # Retrieved Register Term
    if isinstance(left, Register) and reg is None:
        reg = left
    elif isinstance(left, Register) and disp_list[SEC_REG] is None:
        disp_list[SEC_REG] = left

    # at most two registers allowed
    elif isinstance(left, Register):
        raise InvalidMemLoc(token_line[pos].get_nm(), line_num)

    # Retrieved Integer term
    elif isinstance(left, IntegerTok):
        if token_line[pos - 2] == reg:
            reg.set_multiplier(left.get_val(line_num))
        elif token_line[pos - 2] == disp_list[SEC_REG]:
            disp_list[SEC_REG].set_multiplier(left.get_val(line_num))
        else:
            disp_list.append(left.get_val(line_num))

    # Retrieved Symbol term
    else:
        disp_list.append(vm.symbols[token_line[pos].get_nm()])
    next_term = token_line[pos + 1]
    if isinstance(next_term, Comma):
        return get_expr_att(token_line, pos + 2, vm, line_num, reg, disp_list)
    else:
        return (reg, disp_list, pos + 1)


def get_expr_mips(token_line, pos, vm, line_num):
    """
    Returns address expression for MIPS

    Args:
        token_line: Line of code
        pos: Position of address
        vm: Virtual machine

    Returns:
        Token term, next position
    """

    if pos >= len(token_line):
        raise MissingOps(line_num)
    left, pos = get_term(token_line, pos, vm, line_num)
    if isinstance(left, Register):
        return (left, pos + 1)
    else:
        raise InvalidMemLoc(left.get_nm(), line_num)


def get_address_intel(token_line, pos, vm, line_num):
    """
    Converts a sublist of the tokenized instruction into
    corresponding address token

    Args:
        token_line: List of instruction tokens
        pos: Beginning position in list
        vm: Virtual machine

    Returns:
        Register token, displacement, next position
    """

    if pos >= len(token_line):
        raise InvalidMemLoc("", line_num)
    reg = None
    disp = 0
    reg, disp, pos = get_expr_intel(token_line, pos, vm, line_num, reg)
    if pos >= len(token_line):
        raise MissingCloseBrack(line_num)
    elif isinstance(token_line[pos], CloseBracket):
        return (reg, disp, pos + 1)
    else:
        raise InvalidMemLoc(token_line[pos].get_nm(), line_num)


def get_address_att(token_line, pos, vm, line_num, disp=0):
    """
    Converts a sublist of the tokenized instruction into
    corresponding address token for AT&T

    Args:
        token_line: List of instruction tokens
        pos: Beginning position in list
        vm: Virtual machine
        Disp: Numeric displacement

    Returns:
        Register token, displacement(s), next position
    """
    if pos >= len(token_line):
        raise InvalidMemLoc("", line_num)
    reg = None
    reg, disp_list, pos = get_expr_att(token_line, pos, vm,
                                       line_num, reg, [None])
    if pos >= len(token_line):
        raise MissingCloseParen(line_num)
    elif isinstance(token_line[pos], CloseParen):
        if len(disp_list) > 1:
            for values in range(1, len(disp_list)):
                disp += disp_list[values]
        if disp_list[0] is None:
            return (reg, disp, pos + 1)
        return (reg, [disp_list[0], disp], pos + 1)
    else:
        raise InvalidMemLoc(token_line[pos].get_nm(), line_num)


def get_address_mips(token_line, pos, vm, line_num, disp=0):
    """
    Converts a sublist of the tokenized instruction into
    corresponding address token for MIPS

    Args:
        token_line: List of instruction tokens
        pos: Beginning position in list
        vm: Virtual machine

    Returns:
        Register token, displacement, next position
    """

    if pos >= len(token_line):
        raise InvalidMemLoc("", line_num)
    reg, pos = get_expr_mips(token_line, pos, vm, line_num)
    if pos >= len(token_line):
        raise MissingCloseParen(line_num)
    elif isinstance(token_line[pos], CloseParen):
        return (reg, disp, pos + 1)
    else:
        raise InvalidMemLoc(token_line[pos].get_nm(), line_num)


def get_address_location(token_line, pos, vm, line_num):
    """
    Retrieves address at current position in code
    Retrieves address by coding language

    Args:
        token_line: List of the tokenized instruction
        pos: Beginning pos of list
        vm: Virtual machine

    Returns:
        RegAddress or Address token,
        position of next item in instruction
    """
    reg = None
    disp = 0
    if vm.flavor == "intel":
        reg, disp, pos = get_address_intel(token_line, pos, vm, line_num)
    elif vm.flavor == "att":
        reg, disp, pos = get_address_att(token_line, pos, vm, line_num)
    else:
        reg, disp, pos = get_address_mips(token_line, pos, vm, line_num)
    if reg:
        return (RegAddress(reg.get_nm(), vm,
                           disp, reg.get_multiplier()), pos)
    else:
        # eliminates negative memory locations
        if disp < 0:
            raise InvalidMemLoc(str(disp), line_num)
        return (Address(hex(disp).split('x')[-1].upper(), vm), pos)


def check_constant(token_line, pos, line_num):
    """
    Checks if the following token after constant token is valid

    Args:
        token_line: Line of code
        pos: Position of constant token

    Returns:
        True if valid, False otherwise
    """
    try:
        if (not isinstance(token_line[pos + 1], MinusTok) and
                not isinstance(token_line[pos + 1], IntegerTok)):
            return False
        if isinstance(token_line[pos + 1], IntegerTok):
            token_line[pos + 1].con = True
        else:
            try:
                token_line[pos + 2].con = True
            except Exception:
                raise InvalidArgument("-", line_num)
        return True
    except Exception:
        raise InvalidArgument("$", line_num)


def get_op(token_line, pos, vm, line_num):
    """
    Retrieves operand of instruction

    Args:
        token_line: List of the tokenized instruction
        pos: Beginning pos of list
        vm: Virtual machine

    Returns:
        Operand token, position of next item in instruction
    """
    if pos >= len(token_line):
        raise MissingOps(line_num)

# Register
    elif isinstance(token_line[pos], Register):
        return register_token(token_line, pos, vm, line_num)

# Floating Point Token
    elif isinstance(token_line[pos], FloatTok):
        return token_line[pos], pos+1

# Constant Token
    elif isinstance(token_line[pos], ConstantSign):
        if vm.flavor == "att" and check_constant(token_line, pos, line_num):
            return get_op(token_line, pos + 1, vm, line_num)
        else:
            raise InvalidArgument("$", line_num)

# Minus Token
    elif isinstance(token_line[pos], MinusTok):
        minus_token(token_line, pos, line_num)
        return get_op(token_line, pos + 1, vm, line_num)

# Integer Token
    elif isinstance(token_line[pos], IntegerTok):
        return number_token(token_line, pos, vm, line_num)

# Symbol/Label Token
    elif isinstance(token_line[pos], NewSymbol):
        if vm.flavor == "wasm":
            return token_line[pos], pos + 1
        else:
            if token_line[pos].get_nm() in vm.labels:
                return (Label(token_line[pos].get_nm(), vm), pos + 1)
            elif token_line[pos].get_nm() in vm.symbols:
                return symbol_token(token_line, pos, vm, line_num)
            elif vm.flavor == 'intel' and token_line[pos].get_nm()[:2] == "ST":
                return token_line[pos], pos + 1
            else:
                raise UnknownName(token_line[pos].get_nm(), line_num)

# Address Token
    elif is_start_address(token_line, pos, vm.flavor):
        return get_address_location(token_line, pos + 1, vm, line_num)
    else:
        raise InvalidArgument(token_line[pos].get_nm(), line_num)


def get_op_list(token_line, pos, vm, op_lst, line_num):
    """
    Returns a list of ops

    Args:
        token_line: Line of code
        pos: Starting position to retrieve op
        vm: Virtual machine
        op_lst: List of ops

    Returns:
        A list of ops, next position
    """
    op, pos = get_op(token_line, pos, vm, line_num)
    op_lst.append(op)
    if pos >= len(token_line):
        return op_lst, pos
    else:
        next_op = token_line[pos]
        if isinstance(next_op, Comma):
            return get_op_list(token_line, pos + 1, vm, op_lst, line_num)
        else:
            raise MissingComma(line_num)


def get_pc(token_line, pos, line_num):
    """
    Returns the PC counter of the instruction

    Args:
        token_line: Line of code
        pos: Position of PC counter

    Returns:
        Integer token of PC counter value
    """
    if not isinstance(token_line[pos], IntegerTok):
        raise MissingPc(line_num)
    elif token_line[pos].get_val(line_num) % 4 != 0:
        raise InvalidPc(str(token_line[pos].get_val(line_num)), line_num)
    else:
        return token_line[pos]


def parse_exec_unit(token_line, vm, line_num):
    """
    Parses instruction

    Args:
        token_line: Tokenized instruction
        vm: Virtual machine

    Returns:
        List of tokens: instruction, operand(s)
        If MIPS: PC, instruction, operand(s)
    """
    pos = 0
    token_instruction = []
    op_lst = []
    # retrieve PC counter
    if (vm.flavor == "mips_asm" or vm.flavor == "mips_mml" or
            vm.flavor == "riscv"):
        token_instruction.append(get_pc(token_line, pos, line_num))
        pos += 1

    # retrieve instruction
    if not isinstance(token_line[pos], Instruction):
        raise InvalidInstruction(token_line[pos].get_nm(), line_num)
    token_instruction.append(token_line[pos])
    pos += 1

    # retrieve ops
    if pos < len(token_line):
        op_lst, pos = get_op_list(token_line, pos, vm, op_lst, line_num)
    token_instruction.extend(op_lst)
    # switch ops if flavor is AT&T
    if vm.flavor == 'att' and len(token_instruction) > 2:
        switch_vals = token_instruction[1], token_instruction[2]
        token_instruction[1] = switch_vals[1]
        token_instruction[2] = switch_vals[0]

    return token_instruction


def parse(tok_lines, vm, web):
    """
    Parses the analysis obtained from lexical analysis

    Args:
        tok_lines: Lines containing each line of code
        vm: Virtual machine
        web: Boolean indicating whether source is from the website
             or from kernel

    Returns:
        A list of parsed instructions
    """
    parse_data = False
    parse_text = True
    token_instrs = []
    mem_loc = 0
    ip_init = None
    for line in tok_lines:
        tokens = line[TOKENS]
        line_num = line[LINE_NUMBER]
        if isinstance(tokens[0], Section):
            if tokens[0].get_nm() == "data":
                parse_data = True
                parse_text = False
                if not web:
                    vm.set_data_init("on")
                    vm.re_init()
                continue
            elif tokens[0].get_nm() == "text":
                parse_text = True
                parse_data = False
                continue
            else:
                raise InvalidSection(tokens[0].get_nm(), line_num)
        if parse_data:
            mem_loc = parse_data_token(tokens, vm, mem_loc, line_num)
        elif parse_text:
            vm.set_data_init("off")
            parsed_unit = parse_exec_unit(tokens, vm, line_num)
            token_instrs.append((parsed_unit, line[CODE], line_num))
            if (vm.flavor == "mips_asm" or
                vm.flavor == "mips_mml" or
                    vm.flavor == "riscv") and ip_init is None:
                ip_init = token_instrs[0][TOKENS][0].get_val(line_num)
                vm.start_ip = ip_init
    return token_instrs
