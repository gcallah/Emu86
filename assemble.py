"""
assemble.py
Executes assembly code typed in.
"""

from abc import abstractmethod

from .errors import *  # import * OK here:
                       # these are *our* errors, after all!


debug = ""
delimiters = set([' ', ',', '\n', '\r', '\t',])

code_pos = 0


class Operand:
    def __init__(self, name, val=0):
        self.name = name
        self.value = val

    def __str__(self):
        return self.name

    def get_val(self):
        return self.value

    def get_nm(self):
        return self.name


class IntOp(Operand):
    def __init__(self, val=0):
        super().__init__("IntOp", val)


class Location(Operand):
    """
    Class to give common type to memory and registers.
    Adds set_val(), not possible for ints!
    """
    @abstractmethod
    def set_val(self):
        pass


class Address(Location):
    def __init__(self, name, memory, val=0):
        super().__init__(name)
        self.memory = memory

    def get_val(self):
        return int(self.memory[self.name])

    def set_val(self, val):
        add_debug("Setting memory loc " + self.name + " to " + str(val))
        self.memory[self.name] = val


class Register(Location):
    def __init__(self, name, registers):
        super().__init__(name)
        self.registers = registers

    def get_val(self):
        return int(self.registers[self.name])

    def set_val(self, val):
        self.registers[self.name] = val


def add_debug(s):
    global debug
    debug += (s + "\n")

def move(code, registers, memory):
    """
    Implments the MOV instruction.
    """
    (op1, op2) = get_two_ops("MOV", code, registers, memory)
    op1.set_val(op2.get_val())
    return ''

def add(code, registers, memory):
    """
    Implments the ADD instruction.
    """
    (op1, op2) = get_two_ops("ADD", code, registers, memory)
    op1.set_val(op1.get_val() + op2.get_val())
    return ''

def sub(code, registers, memory):
    """
    Implments the SUB instruction.
    """
    (op1, op2) = get_two_ops("ADD", code, registers, memory)
    op1.set_val(op1.get_val() - op2.get_val())
    return ''

def imul(code, registers, memory):
    """
    Implments the IMUL instruction.
    """
    (op1, op2) = get_two_ops("IMUL", code, registers, memory)
    op1.set_val(op1.get_val() * op2.get_val())
    return ''

def andf(code, registers, memory):
    """
    Implments the AND instruction.
    """
    (op1, op2) = get_two_ops("AND", code, registers, memory)
    op1.set_val(op1.get_val() & op2.get_val())
    return ''

def orf(code, registers, memory):
    """
    Implments the OR instruction.
    """
    (op1, op2) = get_two_ops("OR", code, registers, memory)
    op1.set_val(op1.get_val() | op2.get_val())
    return ''

def xor(code, registers, memory):
    """
    Implments the XOR instruction.
    """
    (op1, op2) = get_two_ops("OR", code, registers, memory)
    op1.set_val(op1.get_val() ^ op2.get_val())
    return ''

def shl(code, registers, memory):
    """
    Implments the XOR instruction.
    """
    (op1, op2) = get_two_ops("SHL", code, registers, memory)
    op1.set_val(op1.get_val() << op2.get_val())
    return ''

def shr(code, registers, memory):
    """
    Implments the XOR instruction.
    """
    (op1, op2) = get_two_ops("SHR", code, registers, memory)
    op1.set_val(op1.get_val() >> op2.get_val())
    return ''

def notf(code, registers, memory):
    """
    Implments the NOT instruction.
    """
    op = get_one_op("NOT", code, registers, memory)
    op.set_val(~(op.get_val()))
    return ''

def inc(code, registers, memory):
    """
    Implments the INC instruction.
    """
    op = get_one_op("INC", code, registers, memory)
    op.set_val(op.get_val() + 1)
    return ''

def dec(code, registers, memory):
    """
    Implments the DEC instruction.
    """
    op = get_one_op("DEC", code, registers, memory)
    op.set_val(op.get_val() - 1)
    return ''

def idiv(code, registers, memory):
    """
    Implments the IDIV instruction.
    """
    op = get_one_op("IDIV", code, registers, memory)
    hireg = int(registers['EAX']) << 32
    lowreg = int(registers['EBX'])
    dividend = hireg + lowreg
    registers['EAX'] = dividend // op.get_val()
    registers['EBX'] = dividend % op.get_val()
    return ''

def get_one_op(instr, code, registers, memory):
    """
    For instructions that expect one integer operand.
    """
    tok = get_token(code)
    op = get_op(tok, registers, memory)

    if not op:
        raise InvalidNumArgs(instr, 1)

    return op

def get_two_ops(instr, code, registers, memory):
    """
    For instructions that expect two integer operands.
    """
    tok1 = get_token(code)
    tok2 = get_token(code)
    op1 = get_op(tok1, registers, memory)
    op2 = get_op(tok2, registers, memory)

    if not op1 or not op2:
        raise InvalidNumArgs(instr, 2)
    if not isinstance(op1, Location):
        raise InvalidOperand(op1)

    return (op1, op2)

# if a func name would interfere with a Python keyword,
# let's just add 'f' on the end!
instructions = {
        'ADD': add,
        'IMUL': imul,
        'IDIV': idiv,
        'MOV': move,
        'SUB': sub,
        'AND': andf,
        'OR': orf,
        'XOR': xor,
        'SHL': shl,
        'SHR': shr,
        'NOT': notf,
        'INC': inc,
        'DEC': dec,
        }


def assemble(code, registers, memory):
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
        return ("", "Must submit code to run.", debug)

    while code_pos < len(code):
        try:
            output += get_instruction(code, registers, memory)
        except Error as err:
            return (output, err.msg, debug)
    return (output, '', debug)

def get_instruction(code, registers, memory):
    """
    We expect an instruction next.
        Args:
            code
        Returns:
            None
    """
    instr = get_token(code)
    if instr == '':
        return ''
    elif instr not in instructions:
        raise InvalidInstruction(instr)
    else:
        add_debug("Calling " + instr)
        return instructions[instr](code, registers, memory)

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
                else:
                    break
            code_pos += count

    token = token.upper()  # for now, a simple-minded way to allow input in
                           # either case!
    return token

def get_op(token, registers, memory):
    """
    Returns int value of operand: direct int or reg val
    Args:
        op: operand to evaluate
    Returns:
        int value
    """

    int_val = 0

    if not token:
        return None
    elif token in registers:
        return Register(token, registers)
    elif token[0] == '[' and token[len(token) - 1] == ']':
        address = token[1:len(token) - 1]
        if address in memory:
            return Address(token[1:len(token) - 1], memory)
        else:
            raise InvalidAddress(address)
    else:
        try:
            int_val = int(token)
        except Exception:
            raise InvalidOperand(op)
        return IntOp(int_val)
