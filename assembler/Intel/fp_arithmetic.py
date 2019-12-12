"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

from assembler.errors import check_num_args, DivisionZero, InvalidOperand
from assembler.tokens import Instruction, MAX_FLOAT
# from .arithmetic import checkflag
# from assembler.virtual_machine import intel_machine
from .fp_conversions import add, sub, mul, div, fabs, chs
import math


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
    """
    :param dec: decimal fraction number in string format
    :return: binary equivalent of dec in str format
    Eg : 0.9 -> '11100110011001100110011001100110'
    """
    a = float(dec)
    binary = ''
    while a > 0.0:
        a = a*2
        binary += str(int(a))
        if a >= 1:
            a -= 1
    return binary


def convert_grouped_binary_to_hex(binary):
    """

    :param binary: group of 4 binary number in string format
    :return hexadecimal equivalent of binary number in string format:
    """
    mapping = {}
    for i in range(10):
        mapping[i] = str(i)
    for i in range(10, 16):
        mapping[i] = chr(i-10+97)
    binary = binary+'0'*(4-len(binary))
    integer = int(binary, 2)
    hexequi = mapping[integer]
    return hexequi


"""
dec_convert method is not being used
"""


def dec_convert(val):
    while val > 1:
        val = val / 10
    return val


def checkflag(val, vm):
    """

    :param val: float
    :param vm:
    :return: val in float

    if overflow happens in that case it sets carry flag to one

    """
    if(val > MAX_FLOAT):
        vm.flags['CF'] = 1
        val = val - MAX_FLOAT+1
    else:
        vm.flags['CF'] = 0
    return val


def two_op_arith(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2, line_num)
    reg_one, reg_two = [int(x.get_nm()[-1]) for x in ops]
    # first_reg = vm.get_float_stack_register_at_offset(offset1)
    # second_reg = vm.get_float_stack_register_at_offset(offset2)
    # r1 = vm.fp_stack_registers[first_reg]
    # r2 = vm.fp_stack_registers[second_reg]
    # vm.fp_stack_registers[first_reg] = checkflag(operator(r1, r2), vm)
    if reg_one != 0 and reg_two != 0:
        raise InvalidOperand('Neither registers are ST0', line_num)
    r1 = vm.registers[f'ST{reg_one}']
    r2 = vm.registers[f'ST{reg_two}']
    vm.registers[f'ST{reg_one}'] = checkflag(operator(r1, r2), vm)
    # r1.set_val(
    #     checkflag(operator(r1.get_val(line_num),
    #                        r2.get_val(line_num)), vm))


def pop_arith(ops, vm, instr, operator, line_num):
    check_num_args(instr, ops, 2, line_num)
    reg_one, reg_two = [int(x.get_nm()[-1]) for x in ops]
    # first_reg = vm.get_float_stack_register_at_offset(offset1)
    # second_reg = vm.get_float_stack_register_at_offset(offset2)
    # r1 = vm.fp_stack_registers[first_reg]
    # r2 = vm.fp_stack_registers[second_reg]
    # vm.fp_stack_registers[first_reg] = checkflag(operator(r1, r2), vm)
    if reg_two != 0:
        raise InvalidOperand(f'ST{reg_two}', line_num)
    r1 = vm.registers[f'ST{reg_one}']
    r2 = vm.registers[f'ST{reg_two}']
    vm.registers[f'ST{reg_one}'] = checkflag(float(operator(r1, r2)), vm)
    # r1.set_val(
    #     checkflag(operator(r1.get_val(line_num),
    #                        r2.get_val(line_num)), vm))


def one_op_arith(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1, line_num)
    if operator.__name__ == 'div' and ops[0].get_val(line_num) == 0.0:
        raise DivisionZero(line_num)
    else:
        vm.registers["ST0"] = operator(vm.registers["ST0"],
                                       ops[0].get_val(line_num))


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
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, add, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, add, line_num)


class FaddP(Instruction):
    """
        1 op - adds val to stack top ST(0)
        and stores value at ST(0) and then pops stack
        2 ops - sets sum  of floating stack ST(i)
        and floating stack  ST(j) to floating stack ST(i)
        and then pops stack
            <instr>
                 FADDP
            </instr>
            <syntax>
                FADDP val
                FADDP ST(i), ST(j)
            </syntax>
        """
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, add, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, add, line_num)
        vm.pop_from_Float_Stack()


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
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, sub, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, sub, line_num)


class FSubP(Instruction):
    """
    1 op - subtracts val from stack top ST(0)
    and stores value at ST(0) and then pops the stack
    2 ops - sets difference  of floating stack ST(i) and floating stack
    ST(j) to floating stack ST(i) and then pops the stack
        <instr>
             FSUBP
        </instr>
        <syntax>
            FSUBP val
            FSUBP ST(i), ST(j)
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, sub, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, sub, line_num)
        vm.pop_from_Float_Stack()


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
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, mul, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, mul, line_num)


class FMulP(Instruction):
    """
    1 op - multiplies val with stack top ST(0)
    and stores value at ST(0) and then pops the stack
    2 ops - sets product of floating stack ST(i) and floating stack
     ST(j) to floating stack ST(i) and then pops the stack
        <instr>
             FMULP
        </instr>
        <syntax>
            FMULP val
            FMULP ST(i), ST(j)
        </syntax>
    """

    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, mul, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, mul, line_num)
        vm.pop_from_Float_Stack()


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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, fabs, line_num)


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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, chs, line_num)


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
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, div, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, div, line_num)


class FDivP(Instruction):
    """
    1 op - divides stack top ST(0) with val
    and stores the result at ST(0) and pops the stack
    2 ops - sets the result of dividing floating stack ST(i) by floating stack
     ST(j) to floating stack ST(i) and pops the stack
        <instr>
             FDIVP
        </instr>
        <syntax>
            FDIVP val
            FDIVP ST(i), ST(j)
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, div, line_num)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, div, line_num)
        vm.pop_from_Float_Stack()


class FSqrt(Instruction):
    """
    0 op - computes the square root of the source value in the ST(0)
    register and stores the result in ST(0)
        <instr>
             FSQRT
        </instr>
        <syntax>
            FSQRT
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        if len(ops) == 0:
            top_value = vm.pop_from_Float_Stack()
            sqrt = math.sqrt(top_value)
            vm.push_to_Float_Stack(sqrt)
