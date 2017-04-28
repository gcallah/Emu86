"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from .errors import *
from .tokens import Instruction, MAX_INT


def one_op_arith(ops, gdata, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1)
    ops[0].set_val(operator(ops[0].get_val()))


def two_op_arith(ops, gdata, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    ops[0].set_val(
        checkflag(operator(ops[0].get_val(),
                           ops[1].get_val()), 
                           gdata))


def checkflag(val, gdata):
    if(val > MAX_INT):
        gdata.flags['CF'] = 1
        val = val - MAX_INT
    else:
        gdata.flags['CF'] = 0
    return val


class Add(Instruction):
    """
        <instr>
             add
        </instr>
        <syntax>
            ADD reg, reg
            ADD reg, mem
            ADD reg, con
        </syntax>
    """
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.add)

class Sub(Instruction):
    """
        <instr>
             sub
        </instr>
        <syntax>
            SUB reg, reg
            SUB reg, mem
            SUB reg, con
        </syntax>
    """
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.sub)

class Imul(Instruction):
    """
        <instr>
             imul
        </instr>
        <syntax>
            IMUL reg, reg
            IMUL reg, mem
            IMUL reg, con
        </syntax>
    """
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.mul)
        return ''

class Andf(Instruction):
    """
        <instr>
             and
        </instr>
        <syntax>
            AND reg, reg
            AND reg, mem
            AND reg, con
        </syntax>
    """
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.and_)
        return ''

class Orf(Instruction):
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
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.or_)
        return ''

class Xor(Instruction):
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
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.xor)
        return ''

class Shl(Instruction):
    """
        <instr>
             shl
        </instr>
        <syntax>
            SHL reg, reg
            SHL reg, mem
            SHL reg, con
        </syntax>
    """
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.lshift)
        return ''

class Shr(Instruction):
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
    def fhook(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.rshift)

class Notf(Instruction):
    """
        <instr>
             not
        </instr>
        <syntax>
            NOT reg
        </syntax>
    """
    def fhook(self, ops, gdata):
        one_op_arith(ops, gdata, self.name, opfunc.inv)

class Inc(Instruction):
    """
        <instr>
             inc
        </instr>
        <syntax>
            INC reg
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() + 1)

class Dec(Instruction):
    """
        <instr>
             dec
        </instr>
        <syntax>
            DEC reg
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() - 1)

class Neg(Instruction):
    """
        <instr>
             neg
        </instr>
        <syntax>
            NEG reg
        </syntax>
    """
    def fhook(self, ops, gdata):
        one_op_arith(ops, gdata, self.name, opfunc.neg)
        return ''

class Idiv(Instruction):
    """
        <instr>
             idiv
        </instr>
        <syntax>
            IDIV reg
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args(self.name, ops, 1)
    
        hireg = int(gdata.registers['EDX']) << 32
        lowreg = int(gdata.registers['EAX'])
        dividend = hireg + lowreg
        gdata.registers['EAX'] = dividend // ops[0].get_val()
        gdata.registers['EBX'] = dividend % ops[0].get_val()
        return ''
