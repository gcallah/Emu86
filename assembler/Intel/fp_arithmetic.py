"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction
from assembler.ops_check import one_op_arith, checkFloat
from .arithmetic import checkflag


def convert_float_binary(num, dec_place=10):
    # print(str(num))
    whole, dec = str(num).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + "."
    if num < 0 :
        res = '1'+res
    else:
        res = '0'+res
    if dec ==  0:
        return res+'0'
    for x in range(dec_place):
        if len(str((dec_convert(dec)) * 2).split("."))==2:
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


class FAdd(Instruction):
    """
        <instr>
             add
        </instr>
        <syntax>
            FADD reg, reg
            FADD reg, mem
            FADD reg, const
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.add)


class FAndf(Instruction):

    # def fhook(self, ops, vm):
    #     two_op_arith(ops, vm, self.name, opfunc.and_)
    #     return ''
    def andFunc(intVal, intVal2):
        # print(intVal, intVal2)
        floatOne = convert_float_binary(intVal)
        floatTwo = convert_float_binary(intVal2)
        signedDict = {'one':floatOne[0],'two':floatTwo[0]}
        floatOne=floatOne[1:]
        floatTwo=floatTwo[1:]
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
        if signedDict['one']=='1' and signedDict['two']=='1':
            newFloat='1'+newFloat
        else:
            newFloat='0'+newFloat
        return newFloat


class FSub(Instruction):
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.sub)


class FMul(Instruction):
    def mulFunc(val, val2):
        product = 0
        long=val2
        short=val
        if val>val2:
            long = val
            short = val2
        for i in range(short):
            opfunc.add(product,long)
        return product

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
        signedDict = {'one':floatOne[0],'two':floatTwo[0]}
        floatOne=floatOne[1:]
        floatTwo=floatTwo[1:]
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
        if signedDict['one']=='1' or signedDict['two']=='1':
            newFloat='1'+newFloat
        else:
            newFloat='0'+newFloat
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
    def shiftRightFunc(val):
        floatOne = convert_float_binary(val)
        floatOne=floatOne[1:]
        newFloat = "0"
        for i in range(1, len(floatOne)):
            newFloat += floatOne[i]
        if val<0:
            return('1'+newFloat)
        else:
            return('0'+newFloat)


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
        signedDict = {'one':floatOne[0],'two':floatTwo[0]}
        floatOne=floatOne[1:]
        floatTwo=floatTwo[1:]
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
        if signedDict['one']==signedDict['two']:
            newFloat='0'+newFloat
        else:
            newFloat='1'+newFloat
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
    def shiftLeftFunc(val):
        floatOne = convert_float_binary(val)
        floatOne=floatOne[1:]
        newFloat = ''
        for i in range(1, len(floatOne)):
            newFloat += floatOne[i]
        newFloat+='0'
        if val<0:
            return('1'+newFloat)
        else:
            return('0'+newFloat)
        return(newFloat)
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.lshift)
        return ''


class FDec(Instruction):
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
    def FnegFunc(val):
        floatOne = convert_float_binary(val)
        floatOne=floatOne[1:]
        newFloat = ""
        for i in range(len(floatOne)):
            if floatOne[i] == '1':
                newFloat += '0'
            else:
                newFloat += '1'
        if val<0:
            return('1'+newFloat)
        else:
            return('0'+newFloat)
        return (newFloat)

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
        floatOne=floatOne[1:]
        newFloat = ""
        for i in range(len(floatOne)):
            if floatOne[i] == '1':
                newFloat += '0'
            else:
                newFloat += '1'
        if val<0:
            return('1'+newFloat)
        else:
            return('0'+newFloat)
        return (newFloat)


class FDiv(Instruction):
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
