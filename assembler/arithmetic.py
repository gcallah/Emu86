"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from .errors import *
from .tokens import Instruction


BITS = 32  # for now we assume 32-bit ints


def one_op_arith(ops, gdata, instr, f):
    check_num_args(instr, ops, 1)
    ops[0].set_val(f(ops[0].get_val()))

def two_op_arith(ops, gdata, instr, f):
    check_num_args(instr, ops, 2)
    ops[0].set_val(f(ops[0].get_val(), ops[1].get_val()))


class Add(Instruction):
    """
        <instr>
             add
        </instr>
        SYNTAX:
            ADD reg, reg
            ADD reg, mem
            ADD reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.add)
        return ''

class Sub(Instruction):
    """
        <instr>
             sub
        </instr>
        SYNTAX:
            SUB reg, reg
            SUB reg, mem
            SUB reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.sub)
        return ''

class Imul(Instruction):
    """
        <instr>
             imul
        </instr>
        SYNTAX:
            IMUL reg, reg
            IMUL reg, mem
            IMUL reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.mul)
        return ''

class Andf(Instruction):
    """
        <instr>
             and
        </instr>
        SYNTAX:
            AND reg, reg
            AND reg, mem
            AND reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.and_)
        return ''

class Orf(Instruction):
    """
        <instr>
             or
        </instr>
        SYNTAX:
            OR reg, reg
            OR reg, mem
            OR reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.or_)
        return ''

class Xor(Instruction):
    """
        <instr>
             xor
        </instr>
        SYNTAX:
            XOR reg, reg
            XOR reg, mem
            XOR reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.xor)
        return ''

class Shl(Instruction):
    """
        <instr>
             shl
        </instr>
        SYNTAX:
            SHL reg, reg
            SHL reg, mem
            SHL reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.lshift)
        return ''

class Shr(Instruction):
    """
        <instr>
             shr
        </instr>
        SYNTAX:
            SHR reg, reg
            SHR reg, mem
            SHR reg, con
    """
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfunc.rshift)
        return ''

class Notf(Instruction):
    """
        <instr>
             not
        </instr>
        SYNTAX:
            NOT reg
    """
    def f(self, ops, gdata):
        one_op_arith(ops, gdata, self.name, opfunc.inv)
        return ''

class Inc(Instruction):
    """
        <instr>
             inc
        </instr>
        SYNTAX:
            INC reg
    """
    def f(self, ops, gdata):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() + 1)
        return ''

class Dec(Instruction):
    """
        <instr>
             dec
        </instr>
        SYNTAX:
            DEC reg
    """
    def f(self, ops, gdata):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() - 1)
        return ''

class Neg(Instruction):
    """
        <instr>
             neg
        </instr>
        SYNTAX:
            NEG reg
    """
    def f(self, ops, gdata):
        one_op_arith(ops, gdata, self.name, opfunc.neg)
        return ''

class Idiv(Instruction):
    """
        <instr>
             idiv
        SYNTAX:
            IDIV reg
    """
    def f(self, ops, gdata):
        check_num_args(self.name, ops, 1)
    
        hireg = int(gdata.registers['EDX']) << 32
        lowreg = int(gdata.registers['EAX'])
        dividend = hireg + lowreg
        gdata.registers['EAX'] = dividend // ops[0].get_val()
        gdata.registers['EBX'] = dividend % ops[0].get_val()
        return ''
