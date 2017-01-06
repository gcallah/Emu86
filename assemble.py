"""
assemble.py
Executes assembly code typed in.
"""

from .errors import *  # import * OK here:
                       # there are *our* errors, after all!


debug = ""
delimiters = set([' ', ',', '\n', '\r', '\t',])

code_pos = 0


def add_debug(s):
    global debug
    debug += (s + "\n")

def move(code, registers):
    """
    Implments the MOV instruction.
    """
    (op1, iop1, iop2) = two_op_ints("MOV", code, registers)
    registers[op1] = iop2
    return ''

def add(code, registers):
    """
    Implments the ADD instruction.
    """
    (op1, iop1, iop2) = two_op_ints("ADD", code, registers)
    registers[op1] = iop1 + iop2
    return ''

def sub(code, registers):
    """
    Implments the SUB instruction.
    """
    (op1, iop1, iop2) = two_op_ints("ADD", code, registers)
    registers[op1] = iop1 - iop2
    return ''

def imul(code, registers):
    """
    Implments the IMUL instruction.
    """
    (op1, iop1, iop2) = two_op_ints("IMUL", code, registers)
    registers[op1] = iop1 * iop2
    return ''

def andf(code, registers):
    """
    Implments the AND instruction.
    """
    (op1, iop1, iop2) = two_op_ints("AND", code, registers)
    registers[op1] = iop1 & iop2
    return ''

def orf(code, registers):
    """
    Implments the OR instruction.
    """
    (op1, iop1, iop2) = two_op_ints("OR", code, registers)
    registers[op1] = iop1 | iop2
    return ''

def xor(code, registers):
    """
    Implments the XOR instruction.
    """
    (op1, iop1, iop2) = two_op_ints("OR", code, registers)
    registers[op1] = iop1 ^ iop2
    return ''

def shl(code, registers):
    """
    Implments the XOR instruction.
    """
    (op1, iop1, iop2) = two_op_ints("SHL", code, registers)
    registers[op1] = iop1 << iop2
    return ''

def shr(code, registers):
    """
    Implments the XOR instruction.
    """
    (op1, iop1, iop2) = two_op_ints("SHR", code, registers)
    registers[op1] = iop1 >> iop2
    return ''

def notf(code, registers):
    """
    Implments the NOT instruction.
    """
    (op, iop) = one_op_int("NOT", code, registers)
    registers[op] = ~iop
    return ''

def one_op_int(instr, code, registers):
    """
    For instructions that expect one integer operand.
    """
    op = get_token(code)

    if not op:
        raise InvalidNumArgs(instr, 1)
    iop = get_op_as_int(op, registers)

    return (op, iop)

def two_op_ints(instr, code, registers):
    """
    For instructions that expect two integer operands.
    """
    op1 = get_token(code)
    op2 = get_token(code)

    if not op1 or not op2:
        raise InvalidNumArgs(instr, 2)
    if op1 not in registers:
        raise InvalidOperand(op1)
    iop1 = get_op_as_int(op1, registers)
    iop2 = get_op_as_int(op2, registers)

    return (op1, iop1, iop2)

# if a func name would interfere with a Python keyword,
# let's just add 'f' on the end!
instructions = {
        'ADD': add,
        'IMUL': imul,
        'MOV': move,
        'SUB': sub,
        'AND': andf,
        'OR': orf,
        'XOR': xor,
        'SHL': shl,
        'SHR': shr,
        'NOT': notf,
        }


def assemble(code, registers):  # memory to come!
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
    global debug
    debug = ''

    output = ''
    error = ''
    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", debug, registers)

    while code_pos < len(code):
        try:
            add_debug("Trying for instruction with code_pos of " +
                    str(code_pos))
            output += get_instruction(code, registers)
        except Error as err:
            return (output, err.msg, debug, registers)
    return (output, '', debug, registers)

def get_instruction(code, registers):
    """
    We expect an instruction next.
        Args:
            code
        Returns:
            None
    """
    instr = get_token(code)
    if instr not in instructions:
        raise InvalidInstruction(instr)
    else:
        add_debug("Calling " + instr)
        return instructions[instr](code, registers)

def get_token(code):
    """
        Gets the next token.
        Args:
            The string of code, set to current pos.
        Returns:
            The next token from string.
    """
    global code_pos

    token = ''
    add_debug("Calling get_token() with code pos of: " + str(code_pos))
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
                    add_debug("Adding " + str(char) + " to " + token)
                else:
                    break
            code_pos += count

    token = token.upper()  # for now, a simple-minded way to allow input in
                           # either case!
    return token

def get_op_as_int(op, registers):
    """
    Returns int value of operand: direct int or reg val
    Args:
        op: operand to evaluate
    Returns:
        int value
    """

    int_val = None

    if op in registers:
        int_val = int(registers[op])
    else:
        try:
            int_val = int(op)
        except Exception:
            raise InvalidOperand(op)
    return int_val
