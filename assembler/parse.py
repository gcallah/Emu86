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
from .tokens import RegAddress, Label, NewSymbol, SymAddress, Section, DataType
from .tokens import StringTok, Comma, OpenParen, CloseParen, DupTok, QuestionTok
from .tokens import OpenBracket, CloseBracket, PlusTok, MinusTok
from .arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .arithmetic import Shr, Notf, Andf, Orf, Xor, Neg
from .control_flow import Cmpf, Je, Jne, Jmp, FlowBreak, Call, Ret
from .control_flow import Jg, Jge, Jl, Jle
from .data_mov import Mov, Pop, Push, Lea
from .interrupts import Interrupt
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

je = Je('JE')
jne = Jne('JNE')
jg = Jg ('JG')
jl = Jl ('JL')
instructions = {
        # interrupts:
        'INT': Interrupt('INT'),
        # control flow:
        'CMP': Cmpf('CMP'),
        'JMP': Jmp('JMP'),
        je.get_nm(): je,
        jne.get_nm(): jne,
        # the next two instructions are just synonyms for the previous two.
        'JZ': je,
        'JNZ': jne,
        jg.get_nm(): jg,
        jl.get_nm(): jl,
        # JNLE synonymous to JG, JNGE synonymous to JL
        'JNLE': jg,
        'JNGE': jl,
        'JGE': Jge('JGE'),
        'JLE': Jle('JLE'),
        'CALL': Call('CALL'),
        'RET' : Ret('RET'),
        # data movement:
        'MOV': Mov('MOV'),
        'PUSH': Push('PUSH'),
        'POP': Pop('POP'),
        'LEA': Lea('LEA'),
        # arithmetic and logic:
        'ADD': Add('ADD'),
        'SUB': Sub('SUB'),
        'IMUL': Imul('IMUL'),
        'IDIV': Idiv('IDIV'),
        'AND': Andf('AND'),
        'OR': Orf('OR'),
        'XOR': Xor('XOR'),
        'SHL': Shl('SHL'),
        'SHR': Shr('SHR'),
        'NOT': Notf('NOT'),
        'INC': Inc('INC'),
        'DEC': Dec('DEC'),
        'NEG': Neg('NEG'),
        }

BYTES = 0
MAX_VAL = 1
dtype_info = {
    "DB": (1, MAX_BYTE),
    "DW": (MEM_SIZE / 16, MAX_SHORT),   # we should revisit this choice
    "DD": (MEM_SIZE / 8, MAX_LONG)
}

PARAM_TYPE = 1
PARAM_VAL = 0

def add_debug(s, vm):
    vm.debug += (s + "\n")

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
                    pos += 2
                    state = NEED_CLOSE_PAREN
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


def get_Values(token_line, data_type, pos):
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
                duplicate = token_line[pos].get_val()
                value, pos = get_DUP_value(token_line, pos + 2)
                for times in range(duplicate):
                    if value == DONT_INIT:
                        values_list.append(randrange(0, 
                                 dtype_info[data_type][MAX_VAL]))
                    else:
                        values_list.append(value)
                return (values_list, pos)
            # otherwise return int
            else:
                return ([token_line[pos].get_val()], pos + 1)

        else:
            return ([token_line[pos].get_val()], pos + 1)

    # if value is a string token
    elif isinstance(token_line[pos], StringTok):
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
            for letter in token_line[pos].get_nm():
                if letter != "'":
                    values_list.append(ord(letter))
            values_list.append(0)
            return (values_list, pos + 3)

    elif isinstance(token_line[pos], QuestionTok):
        values_list.append(randrange(0, 
                                 dtype_info[data_type][MAX_VAL]))
        return (values_list, pos + 1)

    else:
        raise InvalidDataVal(token_line[pos].get_nm())

def parse_data_token(token_line, vm):
    """
    Parses data tokens 

    Args:
        token_line: List of data tokens
        vm: Virtual machine
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
            val, pos = get_Values(token_line, data_type, pos)
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

    # if length of list is 1, only store the value
    if len(data_vals) == 1:
        vm.symbols[symbol] = data_vals[0]
        add_debug("Symbol table now holds " + 
                      str(vm.symbols[symbol]), vm)

    # otherwise, store the list 
    else:
        vm.symbols[symbol] = data_vals
        debug_string = "Symbol table now holds "
        for int_values in vm.symbols[symbol]:
            debug_string += str(int_values) + ","
        add_debug(debug_string, vm)  


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
    register = None
    displacement = 0
    if isinstance(token_line[pos], IntegerTok):
        displacement = token_line[pos].get_val()
    elif isinstance(token_line[pos], Register):
        register = token_line[pos]
    else:
        raise InvalidMemLoc(token_line[pos].get_nm())
    pos += 1
    closeBracket = False 
    # check other elements within bracket
    while pos < len(token_line):
        if isinstance(token_line[pos], IntegerTok):
            if isinstance(token_line[pos - 1], PlusTok):
                displacement += token_line[pos].get_val()
                pos += 1
            elif isinstance(token_line[pos - 1], MinusTok):
                displacement -= token_line[pos].get_val()
                pos += 1
            else:
                raise InvalidMemLoc(str(token_line[pos].get_val()))
        elif (isinstance(token_line[pos], PlusTok) or 
              isinstance(token_line[pos], MinusTok)):
            if (isinstance(token_line[pos - 1], IntegerTok) or
                isinstance(token_line[pos - 1], Register)):
                pos += 1
                continue
            else:
                raise InvalidArgument("+")
        elif isinstance(token_line[pos], Register):
            if isinstance(token_line[pos - 1], PlusTok):
                if register:
                    displacement += token_line[pos].get_val()
                else:
                    register = token_line[pos]
                pos += 1
            elif isinstance(token_line[pos - 1], MinusTok):
                if register:
                    displacement -= token_line[pos].get_val()
                else:
                    register = token_line[pos]
                pos += 1
            else:
                raise InvalidMemLoc(token_line[pos].get_nm())
        elif isinstance(token_line[pos], CloseBracket):
            if (isinstance(token_line[pos - 1], IntegerTok) or
                isinstance(token_line[pos - 1], Register)):
                closeBracket = True
                pos += 1
                break
        else:
            raise InvalidMemLoc(token_line[pos].get_nm())
    if closeBracket:
        return (register, displacement, pos)
    else:
        raise MissingCloseBrack()

def get_op(token_line, pos, vm):
    """
    Retrieves operand of instruction

    Args:
        token_line: List of the tokenized instruction
        pos: Beginning pos of list
        vm: Virtua machine

    Returns: 
        Operand token, position of next item in instruction
    """
    if pos >= len(token_line):
        raise MissingOps()
    if (isinstance(token_line[pos], Register) or 
        isinstance(token_line[pos], IntegerTok)):
        return (token_line[pos], pos + 1)
    elif isinstance(token_line[pos], MinusTok):
# return minus_tok()
        try:
            token_line[pos + 1].negate_val()
            return (token_line[pos + 1], pos + 2)
        except:
            raise InvalidArgument()
    elif isinstance(token_line[pos], OpenBracket):
# return open_bracket()
        pos += 1
        register, displacement, pos = get_address(token_line, pos, vm)
        if register:
            return (RegAddress(register.get_nm(), vm, displacement), pos)
        else:
            return (Address(str(displacement), vm), pos)

    elif isinstance(token_line[pos], NewSymbol):
# what about functions for each if / elif in this function?
# return new_symbol()
        if token_line[pos].get_nm() in vm.labels:
            return (Label(token_line[pos].get_nm(), vm), pos + 1)
        elif token_line[pos].get_nm() not in vm.symbols:
            raise UnknownName(token_line[pos].get_nm())
        else:
            symbol = token_line[pos].get_nm()
            pos += 1 
            if pos < len(token_line):
                if isinstance(token_line[pos], OpenBracket):
                    pos += 1
                    register, displacement, pos = get_address(token_line, 
                                                              pos, vm)
                    if register:
                        return (Symbol(symbol, vm, register), pos)
                        
                    return (Symbol(symbol, vm, displacement), pos)
                else:
                    if isinstance(vm.symbols[symbol], list):
                        return (Symbol(symbol, vm, 0), pos)
                    else:
                        return (Symbol(symbol, vm), pos)
            else:
                if isinstance(vm.symbols[symbol], list):
                    return (Symbol(symbol, vm, 0), pos)
                else:
                    return (Symbol(symbol,vm), pos)
    else:
        raise InvalidArgument(token_line[pos].get_nm())

def parse_exec_unit(token_line, vm):
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
            op, pos = get_op(token_line, pos, vm)
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
    return token_instruction




def parse(tok_lines, vm):
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
            parse_data_token(tokens[0], vm)
        elif parse_text:
            token_instrs.append((parse_exec_unit(tokens[0], vm), 
                                 tokens[1]))
    return token_instrs
