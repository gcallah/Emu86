"""
assemble.py
Executes assembly code typed in.
"""

from .errors import *  # import * OK here:
                       # there are *our* errors, after all!


debug = ""
delimiters = set([' ', ',', '\n', '\t',])

registers = None
code_pos = 0


def move(code):
    global registers

    (op1, iop1, iop2) = two_op_ints("MOV", code)
    registers[op1] = iop2

    return ''

def add(code):
    global registers
    
    (op1, iop1, iop2) = two_op_ints("ADD", code)
    registers[op1] = iop1 + iop2

    return ''

def sub(code):
    global registers
    
    (op1, iop1, iop2) = two_op_ints("ADD", code)
    registers[op1] = iop1 - iop2

    return ''

def two_op_ints(instr, code):
    global debug
    global registers
    
    op1 = get_token(code)
    op2 = get_token(code)

    if not op1 or not op2:
        raise InvalidNumArgs(instr, 2)
    if op1 not in registers:
        raise InvalidOperand(op1)
    iop1 = get_op_as_int(op1)
    iop2 = get_op_as_int(op2)

    return (op1, iop1, iop2)

instructions = {
        'ADD': add,
        'MOV': move,
        'SUB': sub,
        }



def assemble(code, regs):  # memory to come!
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            registers: current register values.
        Returns:
            Output, if any.
            Error, if any.
    """
    global code_pos
    code_pos = 0
    global registers
    registers = regs
    global debug
    debug = ''

    output = ''
    error = ''
    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug)

    while code_pos < len(code):
        try:
            output += get_instruction(code)
        except Error as err:
            return (output, err.msg, debug)
    return (output, '', debug)

def get_instruction(code):
    """
    We expect an instruction next.
        Args:
            code
        Returns:
            None
    """
    global debug

    instr = get_token(code)
    if instr not in instructions:
        raise InvalidInstruction(instr)
    else:
        debug += "Calling " + instr + "\n"
        return instructions[instr](code)

def get_token(code):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    global code_pos
    global debug

    token = ''
    if code_pos <= len(code):
        count = 0
        for char in code[code_pos:]:  # eat leading delimiters
            if char in delimiters:
                count += 1
            else:
                break
        code_pos += count
    
        if code_pos <= len(code):
            count = 0
            for char in code[code_pos:]:
                count += 1
                if char not in delimiters:
                    token = token + char
                else:
                    break
            code_pos += count

    return token

def get_op_as_int(op):
    """
    Returns int value of operand: direct int or reg val
    Args:
        op: operand to evaluate
    Returns:
        int value
    """
    global registers
    global debug

    int_val = None

    if op in registers:
        int_val = int(registers[op])
        debug = debug + "From reg " + op + " got val " + str(int_val)
    else:
        try:
            int_val = int(op)
        except Exception:
            raise InvalidOperand(op)
    return int_val
