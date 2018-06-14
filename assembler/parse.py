"""
parse.py: creates parse tree.
"""

import re
import pdb
from random import randrange

from .errors import InvalidMemLoc, InvalidOperand, InvalidInstruction
from .errors import UnknownName, InvalidDataType
from .tokens import Location, Address, Register, IntOp, Symbol, Instruction
from .tokens import RegAddress, Label, NewSymbol, SymAddress
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


def parse_data_val(token_line, vm):
    """
    Parses the data secton 

    Args: 
        token_line: A list of tuples of terms for a line of code
        vm: Virtual machine
    """
    try:
        # denote symbol
        symbol = ""
        if isinstance(token_line[0], NewSymbol):
            symbol = token_line[0].get_nm()
        data_type = token_line[1]

        # denote data size
        dsize = ""
        try:
            dsize = dtype_info[data_type][BYTES]
        except KeyError:
            raise InvalidDataType(date_type)

        # set values
        if isinstance(token_line[2], IntOp):
            val = str(token_line[2].get_val())
        else:
            val = str(token_line[2])
        if len(token_line) > 3:
            index = 3
            while (index < len (token_line)):
                # if contains DUP 
                if token_line[index] == "DUP":
                    try:
                        val += (token_line[index] + 
                               str(token_line[index + 1].get_val())+ ",")
                        index += 2
                    except Exception:
                        raise InvalidDataVal(val)
                # if contains an integer
                else:
                    # strip in case next term is DUP 
                    val = val.strip(",")
                    val += "," + str(token_line[index].get_val())
                    index += 1

        # strip off extra comma if there is from DUP
        val = val.strip(",")
        # convert values if necessary
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
                except Exception:
                    raise InvalidDataVal(val)
    except Exception:
        raise InvalidDataVal(token_line)

def parse_text_instr(token_line, vm):
    """
    Parses the text section

    Args:
        token_line: Line of code representing the instruction
        vm: Virtual machine

    Returns:
        The instruction in list form with its parameters 
    """
    token_instruction = []

    # add instruction
    if isinstance(token_line[0], Instruction):
        token_instruction.append(token_line[0])
    else: 
        raise InvalidInstruction(token_line[0].get_nm())

    # adding the parameters 
    for index in range(1, len(token_line)):
        if isinstance(token_line[index], NewSymbol):
            if token_line[index].get_nm() in vm.labels:
                token_instruction.append(Label(token_line[index].get_nm(), 
                                               vm))
            elif token_line[index].get_nm() not in vm.symbols:
                raise UnknownName(token_line[index].get_nm())
            elif isinstance (vm.symbols[token_line[index].get_nm()], list): 
                add_debug("Adding label " + token_line[index].get_nm(), vm)    
                token_instruction.append(
                                      Symbol(token_line[index].get_nm(), 
                                             vm, 0))
            else:
                add_debug("Matched a symbol-type token " + 
                           token_line[index].get_nm(), vm)
                token_instruction.append(Symbol(token_line[index].get_nm(), 
                                                vm))
        elif isinstance(token_line[index], SymAddress):
            token_instruction.append(Symbol(token_line[index].get_nm(), 
                                            vm, token_line[index].get_val()))
        else:   
            token_instruction.append(token_line[index])
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
        if tokens[0][0] == DATA_SECT:
            parse_data = True
            parse_text = False
            continue
        elif tokens[0][0] == TEXT_SECT:
            parse_text = True
            parse_data = False
            continue
        if parse_data:
            parse_data_val(tokens[0], vm)
        elif parse_text:
            token_instrs.append((parse_text_instr(tokens[0], vm), 
                                 tokens[1]))
    return token_instrs