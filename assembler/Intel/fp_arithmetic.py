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
    if num < 0:
        res = '1'+res
    else:
        res = '0'+res
    if dec == 0:
        return res+'0'
    for x in range(dec_place):
        if len(str((dec_convert(dec)) * 2).split(".")) == 2:
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





class FSub(Instruction):
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.sub)


class FMul(Instruction):
    def multiplyMantissas(val1, val2):
        val1 = '1' + val1
        val2 = '1' + val2
        return(int(val1, 2)*int(val2, 2))

    def convertIEEE(val):
        binary = convert_float_binary(val)
        binary = binary[1:]
        found = False
        posVal = 0
        posDecimal = 0
        for i in range(len(binary)):
            if binary[i] == '1' and found == False:
                posVal = i
                found = True
            if binary[i] == '.':
                posDecimal = i
        expo = posDecimal - posVal - 1
        Mantissa = binary[posVal+1:posDecimal] + binary[posDecimal+1:]
        return (expo, Mantissa)

    def multiply(val1, val2):
        convert1 = FMul.convertIEEE(val1)
        convert2 = FMul.convertIEEE(val2)
        productMantisa = FMul.multiplyMantissas(convert1[1], convert2[1])
        bitresult = str(bin(productMantisa))[1:]
        print(bitresult.lstrip("0b"))
        while len(bitresult) < 23:
            bitresult += '0'
        exponentResult = (convert1[0] + convert2[0]) + 127
        returnBin = None
        expoFinalResult = bin(exponentResult).lstrip("0b")

        while len(expoFinalResult) != 8:
            expoFinalResult += '0'
        if val1 < 0 or val2 < 0:
            returnBin = '1'+expoFinalResult+bitresult.lstrip("0b")
        else:
            returnBin = '0'+expoFinalResult+bitresult.lstrip("0b")
        return returnBin

    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.mul)


class FDec(Instruction):
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() - 1)
        vm.changes.add(ops[0].get_nm())





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
