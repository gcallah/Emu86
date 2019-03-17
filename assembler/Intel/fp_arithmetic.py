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
        mapping[str(i)]=i
    for i in range(10,16):
        mapping[chr(i-10+97)]=i

    flag = 1
    if fhex[0]=='-':
        flag = -1
        fhex = fhex[1:]
    before_point_hex, after_point_hex = fhex.split('.')
    before_point_dec, after_point_dec = 0, 0
    for i in range(len(before_point_hex)):
        before_point_dec += mapping[before_point_hex[i]]*(16**(len(before_point_hex)-i-1))
    for i in range(len(after_point_hex)):
        after_point_dec += mapping[after_point_hex[i]]*(16**(-1*(i+1)))
    res =  '{}.{}'.format(str(before_point_dec),str(after_point_dec)[2:])
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
    fdec = flag*fdec
    fdec = str(fdec)
    before_point_dec, after_point_dec = fdec.split('.')
    before_point_hex = hex(int(before_point_dec))[2:]
    binary = convert_after_point_dec_to_binary('0.'+after_point_dec)
    after_point_hex = ''
    for i in range(0,len(binary),4):
        after_point_hex += convert_grouped_binary_to_hex(binary[i:i+4])
    if flag == -1:
        final_hex = '-'+before_point_hex+'.'+after_point_hex
    elif flag == 1:
        final_hex = before_point_hex+'.'+after_point_hex
    return final_hex


def convert_after_point_dec_to_binary(dec):
    a = float(dec)
    binary = ''
    while a>0.0:
        a = a*2
        binary += str(int(a))
        if a>=1:
            a -= 1
    return binary

def convert_grouped_binary_to_hex(binary):
    mapping = {}
    for i in range(10):
        mapping[i]=str(i)
    for i in range(10,16):
        mapping[i]=chr(i-10+97)
    binary = binary+'0'*(4-len(binary))
    integer = int(binary,2)
    hexequi = mapping[integer]
    return hexequi




def dec_convert(val):
    while val > 1:
        val = val / 10
    return val


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


class FAdd(Instruction):
    """
    sets sum  of floating-point register (FPR) FRA and
    floating-point register (FPB)
        <instr>
             FADD
        </instr>
        <syntax>
            FADD FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, add)


class FSub(Instruction):
    """
    sets sum  of floating-point register (FPR) FRA and
    floating-point register (FPB)

        <instr>
             FSUB
        </instr>
        <syntax>
            FSUB FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, sub)


class FMul(Instruction):
    """
    sets product  of floating-point register (FPR) FRA and
    floating-point register (FPB)

        <instr>
             FMUL
        </instr>
        <syntax>
            FMUL FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
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
    sets quotient of floating-point register (FPR) FRA and
    floating-point register (FPB)

        <instr>
             FDIV
        </instr>
        <syntax>
            FDIV FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, div)
