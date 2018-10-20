"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT
from assembler.ops_check import one_op_arith,checkFloat
from .arithmetic import checkflag

def two_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    if checkFloat:
        ops[0].set_val(
            checkflag(operator(ops[0].get_val(),
                               ops[1].get_val()),
                               vm))
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
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.or_)
        return ''

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
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.xor)
        return ''
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
    def fhook(self, ops, vm):
        one_op_arith(ops, vm, self.name, opfunc.inv)

class FAndf(Instruction):

    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.and_)
        return ''

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
