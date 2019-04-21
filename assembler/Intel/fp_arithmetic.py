"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

# import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction
from .arithmetic import checkflag
# from assembler.virtual_machine import intel_machine
from .fp_conversions import add, sub, mul, div, fabs, chs


def convert_hex_to_decimal(fhex):
    """
    :param fhex: floating point hexadecimal number in str format
    :return: decimal equivalent of fhex in float format
    Eg : 'a2.4c' -> 162.296875
    """
    mapping = {}
    for i in range(10):
        mapping[str(i)] = i
    for i in range(10, 16):
        mapping[chr(i-10+97)] = i

    flag = 1
    if fhex[0] == '-':
        flag = -1
        fhex = fhex[1:]
    if '.' not in fhex:
        return int(fhex, 16)
    before_point_hex, after_point_hex = fhex.split('.')
    before_point_dec, after_point_dec = 0, 0
    for i in range(len(before_point_hex)):
        map_before_pt_hex = mapping[before_point_hex[i]]
        before_point_dec += map_before_pt_hex*(16**(len(before_point_hex)-i-1))
    for i in range(len(after_point_hex)):
        after_point_dec += mapping[after_point_hex[i]]*(16**(-1*(i+1)))
    res = '{}.{}'.format(str(before_point_dec), str(after_point_dec)[2:])
    return flag*float(res)


def convert_dec_to_hex(fdec):
    """
    :param fdec: floating point decimal number in float format
    :return: hexadecimal equivalent of fdec in str format
    Eg : 162.296875 -> 'a2.4c'
    """
    flag = 1
    if fdec < 0:
        flag = -1
    fdec = flag * fdec
    fdec = str(fdec)
    if '.' not in fdec:
        if flag == -1:
            return '-' + hex(int(fdec))[2:]
        else:
            return hex(int(fdec))[2:]
    before_point_dec, after_point_dec = fdec.split('.')
    before_point_hex = hex(int(before_point_dec))[2:]
    binary = convert_after_point_dec_to_binary('0.' + after_point_dec)
    after_point_hex = ''
    for i in range(0, len(binary), 4):
        after_point_hex += convert_grouped_binary_to_hex(binary[i:i + 4])
    if flag == -1:
        final_hex = '-' + before_point_hex + '.' + after_point_hex
    elif flag == 1:
        final_hex = before_point_hex + '.' + after_point_hex
    return final_hex


def convert_after_point_dec_to_binary(dec):
    a = float(dec)
    binary = ''
    while a > 0.0:
        a = a*2
        binary += str(int(a))
        if a >= 1:
            a -= 1
    return binary


def convert_grouped_binary_to_hex(binary):
    mapping = {}
    for i in range(10):
        mapping[i] = str(i)
    for i in range(10, 16):
        mapping[i] = chr(i-10+97)
    binary = binary+'0'*(4-len(binary))
    integer = int(binary, 2)
    hexequi = mapping[integer]
    return hexequi


def dec_convert(val):
    while val > 1:
        val = val / 10
    return val


def floating_point_addition(num1, num2):
    """
    :param num1: floating point hexadecimal number in str format
    :param num2: floating point hexadecimal number in str format
    :return: hexadecimal equivalent of addition of num1 and num2 in str format
    Eg:- 'a2.e' + '3f.b' -> 'e2.9'
    """
    flag1, flag2 = (num1[0] == '-'), (num2[0] == '-')
    if flag1 and flag2:
        return '-' + floating_point_addition(num1[1:], num2[1:])
    elif flag1:
        return floating_point_subtraction(num2, num1[1:])
    elif flag2:
        return floating_point_subtraction(num1, num2[1:])
    elif not flag1 and not flag2:
        num1_dec = convert_hex_to_decimal(num1)
        num2_dec = convert_hex_to_decimal(num2)
        res = num1_dec + num2_dec
        hex_equi = convert_dec_to_hex(res)
        if '.' not in hex_equi:
            hex_equi += '.0'
        return hex_equi


def floating_point_subtraction(num1, num2):
    """
    :param num1: floating point hexadecimal number in str format
    :param num2: floating point hexadecimal number in str format
    :return: hexadecimal equivalent of subtraction
     of num1 and num2 in str format
    Eg:- 'a2.e' - '3f.b' -> '63.3'
    """
    flag1, flag2 = (num1[0] == '-'), (num2[0] == '-')
    if flag1 and flag2:
        return floating_point_subtraction(num2[1:], num1[1:])
    elif flag1:
        return '-' + floating_point_addition(num1[1:], num2)
    elif flag2:
        return floating_point_addition(num1, num2[1:])
    else:
        num1_dec = convert_hex_to_decimal(num1)
        num2_dec = convert_hex_to_decimal(num2)
        res = num1_dec - num2_dec
        hex_equi = convert_dec_to_hex(res)
        if '.' not in hex_equi:
            hex_equi += '.0'
        return hex_equi


def two_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    ops[0].set_val(
        checkflag(operator(ops[0].get_val(),
                           ops[1].get_val()), vm))
    vm.changes.add(ops[0].get_nm())


def one_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    val_float_stack_top = vm.pop_from_Float_Stack()
    vm.push_to_Float_Stack(operator(val_float_stack_top,ops[0].get_val()))



class FAdd(Instruction):
    """
    1 op - adds val to stack top ST(0) and stores value at ST(0)
    2 ops - sets sum  of floating stack ST(i) and floating stack
    ST(j) to floating stack ST(i)
        <instr>
             FADD
        </instr>
        <syntax>
            FADD val
            FADD ST(i), ST(j)
        </syntax>
    """
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,add)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, add)


class FSub(Instruction):
    """
    1 op - subtracts val from stack top ST(0) and stores value at ST(0)
    2 ops - sets difference  of floating stack ST(i) and floating stack
    ST(j) to floating stack ST(i)
        <instr>
             FSUB
        </instr>
        <syntax>
            FSUB val
            FSUB ST(i), ST(j)
        </syntax>
    """
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,sub)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, sub)


class FMul(Instruction):
    """
    1 op - multiplies val with stack top ST(0) and stores value at ST(0)
    2 ops - sets product of floating stack ST(i) and floating stack
     ST(j) to floating stack ST(i)
        <instr>
             FMUL
        </instr>
        <syntax>
            FMUL val
            FMUL ST(i), ST(j)
        </syntax>
    """
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,mul)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, mul)


class FAbs(Instruction):
    """
    sets bit  of floating-point register (FPR) FRB to 0
    and place the results into FPR FRT
        <instr>
                FABS
        </instr>
        <syntax>
            fabs FRT, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, fabs)


class FChs(Instruction):
    """
    complements the sign of floating-point register (FPR) FRB
        <instr>
                FCHS
        </instr>
        <syntax>
            fchs FRT
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, chs)


class FDiv(Instruction):
    """
    1 op - divides stack top ST(0) with val and stores the result at ST(0)
    2 ops - sets the result of dividing floating stack ST(i) by floating stack
     ST(j) to floating stack ST(i)
        <instr>
             FDIV
        </instr>
        <syntax>
            FDIV val
            FDIV ST(i), ST(j)
        </syntax>
    """
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,div)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, div)
