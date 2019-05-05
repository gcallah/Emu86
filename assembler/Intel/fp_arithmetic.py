"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

# import operator as opfunc
from assembler.errors import check_num_args, DivisionZero
from assembler.tokens import Instruction, MAX_FLOAT, MIN_FLOAT, Register
# from .arithmetic import checkflag
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



def checkflag(val, vm):
    if(val > MAX_FLOAT):
        vm.flags['CF'] = 1
        val = val - MAX_FLOAT+1
    else:
        vm.flags['CF'] = 0
    return val


def two_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    offset1, offset2 = [int(x.get_nm()[-1]) for x in ops]
    first_reg = vm.get_float_stack_register_at_offset(offset1)
    second_reg = vm.get_float_stack_register_at_offset(offset2)
    r1, r2 = vm.fp_stack_registers[first_reg], vm.fp_stack_registers[second_reg]
    vm.fp_stack_registers[first_reg] = checkflag(operator(r1,r2),vm)
    # r1.set_val(
    #     checkflag(operator(r1.get_val(),
    #                        r2.get_val()), vm))
    # vm.changes.add(r1)


def one_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1)
    if operator.__name__ == 'div' and ops[0].get_val() == 0.0:
        raise DivisionZero()
    else:
        val_float_stack_top = vm.pop_from_Float_Stack()
        vm.push_to_Float_Stack(checkflag(operator(val_float_stack_top,ops[0].get_val()),vm))



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


class FaddP(Instruction):
    """
        1 op - adds val to stack top ST(0) and stores value at ST(0) and then pops stack
        2 ops - sets sum  of floating stack ST(i) and floating stack  ST(j) to floating stack ST(i) and then pops stack
            <instr>
                 FADDP
            </instr>
            <syntax>
                FADDP val
                FADDP ST(i), ST(j)
            </syntax>
        """
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops, vm, self.name, add)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, add)
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
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,sub)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, sub)


class FSubP(Instruction):
    """
    1 op - subtracts val from stack top ST(0) and stores value at ST(0) and then pops the stack
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
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,sub)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, sub)
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
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,mul)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, mul)


class FMulP(Instruction):
    """
    1 op - multiplies val with stack top ST(0) and stores value at ST(0) and then pops the stack
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
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,mul)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, mul)
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


class FDivP(Instruction):
    """
    1 op - divides stack top ST(0) with val and stores the result at ST(0) and pops the stack
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
    def fhook(self, ops, vm):
        if len(ops) == 1:
            one_op_arith(ops,vm,self.name,div)
        elif len(ops) == 2:
            two_op_arith(ops, vm, self.name, div)
        vm.pop_from_Float_Stack()
