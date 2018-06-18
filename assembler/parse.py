"""
parse.py: creates parse tree.
"""

import re
import pdb
from random import randrange

from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName, InvalidDataType, InvalidSection
from .errors import InvalidArgument, MissingData, InvalidDataVal, MissingComma
from .tokens import Location, Address, Register, IntegerTok, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, SymAddress, Section, DataType
from .tokens import StringTok, Comma, OpenParen, CloseParen, DupTok, QuestionTok
from .tokens import OpenBracket, CloseBracket, PlusTok
from .arithmetic import Add, Sub, Imul, Idiv, Inc, Dec, Shl
from .arithmetic import Shr, Notf, Andf, Orf, Xor, Neg
from .control_flow import Cmpf, Je, Jne, Jmp, FlowBreak, Call, Ret
from .control_flow import Jg, Jge, Jl, Jle
from .data_mov import Mov, Pop, Push, Lea
from .interrupts import Interrupt
from .virtual_machine import MEM_SIZE


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

def convert_string_to_ascii (values):
    """
    Converts a string into a string of its ASCII values

    Args:
        values: String of values of a parameter

    Returns:
        String of values of ASCII values if a string is present
    """
    if values.find("'") != -1:
        val_string = ""
        begin_index = values.find("'")
        end_index = values.find("'", begin_index + 1)
        for index in range(begin_index + 1, end_index):
            val_string += str(ord(values[index]))
            if index != end_index - 1:
                val_string += ","
        val_string += values[end_index + 1:]
        values = val_string
    return values

def store_values_dup (values, data_type):
    """
    Converts the string of data that uses the term DUP into 
    a string of integers without the term DUP 

    Args:
        values: The values of the variable
        data_type: The data type of the variable

    Returns: 
        String of values without term DUP 
    """
    if values.find("DUP") != -1:
        try:
            position = 0
            count = 0
            values_list_before = ""
            if values.find(",") != -1:
                for pos in range(len(values)):
                    if (values[pos] == ","):
                        position = pos
                values_list_before = values[:position + 1]
                count = int(values[position + 1:values.find("DUP")])
            else:
                count = int(values[:values.find("DUP")])
            values_list_after = ""
            for counter in range(count):
                # if values[values.find("(") + 1:
                #           values.find(")")] == DONT_INIT:
                if values[values.find("DUP") + 1:] == DONT_INIT: 
                    values_list_after += str(randrange(0, 
                                       dtype_info[data_type][MAX_VAL]))
                else:
                    try:
                        values_list_after += values[values.find("DUP") + 3:]
                    except Exception:
                        raise InvalidDataVal(values)

                if counter != count - 1:
                    values_list_after += ","
            values = values_list_before + values_list_after
            return values
        except Exception:
            raise InvalidDataVal(values)
    return values

def store_values_array(values, data_type):
    """
    Returns the array made from the string values

    Args:
        values: Values of the variable 
        data-type: The data type of the variable

    Returns: 
        List of integer values 
    """
    if values.find(",") != -1:
        values_list = values.split(",")
        for index in range(len(values_list)):
            if values_list[index] == DONT_INIT:
                values_list[index] = randrange(0, dtype_info[data_type]
                                                            [MAX_VAL])
            else: 
                try:
                    values_list[index] = int(values_list[index])
                except Exception:
                    raise InvalidDataVal(values)
        return values_list

def get_data_type(token_line, pos):
    if pos >= len(token_line):
        raise MissingData()
    elif isinstance(token_line[pos], DataType):
        if token_line[pos].get_nm() not in dtype_info:
            raise InvalidDataType(token_line[pos].get_nm())
        else:
            return token_line[pos].get_nm()
    else:
        raise InvalidDataType(token_line[pos].get_nm())

def check_data_values(token_line, pos):
    data_okay = True
    # first check the very first data element
    if (not isinstance(token_line[pos], IntegerTok) and 
        not isinstance(token_line[pos], StringTok) and 
        not isinstance(token_line[pos], QuestionTok)):
        data_okay = False
        raise InvalidArgument(token_line[pos].get_nm())
    pos += 1

    # check others afer first element
    while pos < len(token_line):

        # if comma 
        if isinstance(token_line[pos], Comma):
            if pos == len(token_line) - 1:
                data_okay = False
                raise InvalidArgument(",")
            else: 
                if (not isinstance(token_line[pos - 1], IntegerTok) and 
                    not isinstance(token_line[pos - 1], StringTok) and 
                    not isinstance(token_line[pos - 1], QuestionTok) and 
                    not isinstance(token_line[pos - 1], CloseParen)):
                    data_okay = False
                    raise InvalidArgument(",")
                else:
                    pos += 1

        # if DUP
        elif isinstance(token_line[pos], DupTok):
            if not isinstance(token_line[pos - 1], IntegerTok):
                data_okay = False
                raise InvalidArgument("DUP")
            else:
                pos += 1

        # if open parenthesis
        elif isinstance(token_line[pos], OpenParen):
            if not isinstance(token_line[pos - 1], DupTok):
                data_okay = False
                raise InvalidArgument("(")
            else:
                pos += 1

        # if close parenthesis
        elif isinstance(token_line[pos], CloseParen):
            if (not isinstance(token_line[pos - 2], OpenParen) and 
                not isinstance(token_line[pos - 1], IntegerTok) and 
                not isinstance(token_line[pos - 1], StringTok) and 
                not isinstance(token_line[pos - 1], QuestionTok)):
                data_okay = False
                raise InvalidArgument("(")
            else:
                pos += 1

        # if ?
        elif isinstance(token_line[pos], QuestionTok):
            if (not isinstance(token_line[pos - 1], Comma) and
                not isinstance(token_line[pos - 1], OpenParen)):
                data_okay = False
                raise InvalidArgument("?")
            else:
                pos += 1

        # if integer
        elif isinstance(token_line[pos], IntegerTok):

            # if not 0 but follows a string
            if (isinstance(token_line[pos - 2], StringTok) and 
                isinstance(token_line[pos - 1], Comma) and 
                token_line[pos].get_val() != 0):
                data_okay = False
                raise InvalidDataVal(str(token_line[pos].get_val()))

            elif (not isinstance(token_line[pos - 1], Comma) and
                not isinstance(token_line[pos - 1], OpenParen)):
                data_okay = False
                raise InvalidArgument(str(token_line[pos].get_val()))
            else:
                pos += 1

        # if string 
        elif isinstance(token_line[pos], StringTok):
            if not isinstance(token_line[pos - 1], Comma):
                data_okay = False
                raise InvalidDataVal(token_line[pos].get_val())
            else:
                pos += 1

        else:
            raise InvalidDataVal(token_line[pos].get_val())

    return data_okay


def get_data_values(token_line, pos):
    if pos >= len(token_line):
        raise MissingData()
    else:
        if check_data_values(token_line, pos):
            values_list = []
            while pos < len(token_line):
                if isinstance(token_line[pos], IntegerTok):
                    values_list.append(str(token_line[pos].get_val()))
                elif (not isinstance(token_line[pos], OpenParen) and
                    not isinstance(token_line[pos], CloseParen)):
                    values_list.append(token_line[pos].get_nm())
                pos += 1
            return "".join(values_list)

def parse_data_token(token_line, vm):
    pos = 0
    symbol = ""
    if not isinstance(token_line[pos], NewSymbol):
        raise InvalidArgument(token_line[pos].get_nm())
    else:
        symbol = token_line[pos].get_nm()
    pos += 1
    data_type = get_data_type(token_line, pos)
    pos += 1
    val = get_data_values(token_line, pos)
    val = convert_string_to_ascii(val);
    val = store_values_dup(val, data_type);

    # convert string of numbers to a list
    if val.find (",") != -1:
        vm.symbols[symbol] = store_values_array (val, data_type)  
        debug_string = "Symbol table now holds "
        for int_values in vm.symbols[symbol]:
            debug_string += str(int_values) + ","
        add_debug(debug_string, vm)  

    # if not a list and just a value
    else:
        if val == DONT_INIT:
            vm.symbols[symbol] = randrange(0, 
                                 dtype_info[data_type][MAX_VAL])
            add_debug("Symbol table now holds " + 
                      str(vm.symbols[symbol]), vm)
        else: 
            try:
                vm.symbols[symbol] = int(val)
                add_debug("Symbol table now holds " + 
                          str(vm.symbols[symbol]), vm)
            except:
                raise InvalidDataVal(val)

def get_address(token_line, pos, vm):
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
            else:
                raise InvalidMemLoc(str(token_line[pos].get_val()))
        elif isinstance(token_line[pos], PlusTok):
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
        raise InvalidMemLoc("")

def get_op(token_line, pos, vm):
    if (isinstance(token_line[pos], Register) or 
        isinstance(token_line[pos], IntegerTok)):
        return (token_line[pos], pos + 1)
    elif isinstance(token_line[pos], OpenBracket):
        pos += 1
        register, displacement, pos = get_address(token_line, pos, vm)
        if register:
            return (RegAddress(register.get_nm(), vm, displacement), pos)
        else:
            return (Address(str(displacement), vm), pos)

    elif isinstance(token_line[pos], NewSymbol):
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
                    register, displacement, pos = get_address(token_line, pos, vm)
                    if register:
                        return (Symbol(symbol, vm, register), pos)
                        
                    return (Symbol(symbol, vm, displacement), pos)
                else:
                    if isinstance(vm.symbols[symbol], list):
                        return (Symbol(symbol, vm, 0), pos)
                    else:
                        return (Symbol(symbol,vm), pos)
            else:
                if isinstance(vm.symbols[symbol], list):
                    return (Symbol(symbol, vm, 0), pos)
                else:
                    return (Symbol(symbol,vm), pos)
    else:
        raise InvalidArgument(token_line[pos].get_nm())

def parse_exec_unit(token_line, vm):
    pos = 0
    token_instruction = []
    if not isinstance(token_line[pos], Instruction):
        raise InvalidInstruction(token_line[pos].get_nm())
    token_instruction.append(token_line[pos])
    pos += 1 
    while pos < len(token_line):
        op, pos = get_op(token_line, pos, vm)
        token_instruction.append(op)
        if pos < len(token_line):
            if isinstance(token_line[pos], Comma): 
                pos += 1
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
        if isinstance(tokens[0][0], Section):
            if tokens[0][0].get_nm() == "data":
                parse_data = True
                parse_text = False
                continue
            elif tokens[0][0].get_nm() == "text":
                parse_text = True
                parse_data = False
                continue
            else: 
                raise InvalidSection(tokens[0][0].get_nm())
        if parse_data:
            parse_data_token(tokens[0], vm)
        elif parse_text:
            token_instrs.append((parse_exec_unit(tokens[0], vm), 
                                 tokens[1]))
    return token_instrs