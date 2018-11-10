"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction
from assembler.ops_check import one_op_arith, checkFloat
from .arithmetic import checkflag


def convert_float_binary(num, dec_place=10):
    print(str(num))
    whole, dec = str(num).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + "."
    for x in range(dec_place):
        whole, dec = str((dec_convert(dec)) * 2).split(".")
        dec = int(dec)
        res += whole
    return res


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
    if checkFloat:
        ops[0].set_val(
            checkflag(operator(ops[0].get_val(),
                               ops[1].get_val()), vm))
        vm.changes.add(ops[0].get_nm())


class FADD(Instruction):
    """
        <instr>
             add
        </instr>
        <syntax>
            ADD reg, reg
            ADD reg, mem
            ADD reg, const
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.add)


class FAndf(Instruction):

    # def fhook(self, ops, vm):
    #     two_op_arith(ops, vm, self.name, opfunc.and_)
    #     return ''
    def andFunc(intVal, intVal2):
        print(intVal, intVal2)
        floatOne = convert_float_binary(intVal)
        floatTwo = convert_float_binary(intVal2)
        while len(floatOne) < len(floatTwo):
            floatOne = "0" + floatOne
        while len(floatTwo) < len(floatOne):
            floatTwo = "0" + floatTwo
        newFloat = ""
        for i in range(len(floatOne)):
            if floatOne[i] == '1' and floatTwo[i] == '1':
                newFloat += '1'
            elif floatOne[i] == '.':
                newFloat += '.'
            else:
                newFloat += '0'
        return newFloat


class FSUB(Instruction):
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.sub)


class FMUL(Instruction):
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.mul)


class FOrf(Instruction):
    """
        <instr>
             or
        </instr>
        <syntax>
            OR reg, reg
            OR reg, mem
            OR reg, con
        </syntax>
    """
    def orFunc(intVal, intVal2):
        floatOne = convert_float_binary(intVal)
        floatTwo = convert_float_binary(intVal2)
        while len(floatOne) < len(floatTwo):
            floatOne = "0" + floatOne
        while len(floatTwo) < len(floatOne):
            floatTwo = "0" + floatTwo
        newFloat = ""
        for i in range(len(floatOne)):
            if floatOne[i] == '1' or floatTwo[i] == '1':
                newFloat += '1'
            elif floatOne[i] == '.':
                newFloat += '.'
            else:
                newFloat += '0'
        return newFloat


class FShr(Instruction):
    """
        <instr>
             shr
        </instr>
        <syntax>
            SHR reg, reg
            SHR reg, mem
            SHR reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.rshift)


class FXor(Instruction):
    """
        <instr>
             xor
        </instr>
        <syntax>
            XOR reg, reg
            XOR reg, mem
            XOR reg, con
        </syntax>
    """
    def xorFunc(intVal, intVal2):
        floatOne = convert_float_binary(intVal)
        floatTwo = convert_float_binary(intVal2)
        while len(floatOne) < len(floatTwo):
            floatOne = "0" + floatOne
        while len(floatTwo) < len(floatOne):
            floatTwo = "0" + floatTwo
        newFloat = ""
        for i in range(len(floatOne)):
            if floatOne[i] == '1' and floatTwo[i] == '1':
                newFloat += '0'
            if ((floatOne[i] == '0' and floatTwo[i] == '1') or
                    (floatOne[i] == '1' and floatTwo[i] == '0')):
                newFloat += '1'
            elif floatOne[i] == '.':
                newFloat += '.'
            else:
                newFloat += '0'
        return newFloat


class FShl(Instruction):
    """
        <instr>
             fshl
        </instr>
        <syntax>
            SHL reg, reg
            SHL reg, mem
            SHL reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.lshift)
        return ''


class FDec(Instruction):
    """
        <instr>
             dec
        </instr>
        <syntax>
            DEC reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() - 1)
        vm.changes.add(ops[0].get_nm())


class FNeg(Instruction):
    """
        <instr>
             neg
        </instr>
        <syntax>
            NEG reg
        </syntax>
    """
    def fhook(self, ops, vm):
        one_op_arith(ops, vm, self.name, opfunc.neg)
        return ''


class FInc(Instruction):
    """
        <instr>
             Finc
        </instr>
        <syntax>
            INC reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() + 1)
        vm.changes.add(ops[0].get_nm())


class FNotf(Instruction):
    """
        <instr>
             not
        </instr>
        <syntax>
            NOT reg
        </syntax>
    """
    def notFunc(val):
        floatOne = convert_float_binary(val)
        newFloat = ""
        for i in range(len(floatOne)):
            if floatOne[i] == '1':
                newFloat += '0'
            else:
                newFloat += '1'
        return (newFloat)


class FDIV(Instruction):
    def fhook(self, ops, vm):
        return
        # check_num_args(self.name, ops, 1)
        #
        # hireg = int(vm.registers['EDX']) << 32
        # lowreg = int(vm.registers['EAX'])
        # dividend = hireg + lowreg
        # if ops[0].get_val() == 0:
        #     raise DivisionZero()
        # vm.registers['EAX'] = dividend // ops[0].get_val()
        # vm.registers['EDX'] = dividend % ops[0].get_val()
        # vm.changes.add('EAX')
        # vm.changes.add('EDX')
        # return ''
