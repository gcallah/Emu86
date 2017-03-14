"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfs

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
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.add)
        return ''

class Sub(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.sub)
        return ''

class Imul(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.mul)
        return ''

class Andf(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.and_)
        return ''

class Orf(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.or_)
        return ''

class Xor(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.xor)
        return ''

class Shl(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.lshift)
        return ''

class Shr(Instruction):
    def f(self, ops, gdata):
        two_op_arith(ops, gdata, self.name, opfs.rshift)
        return ''

class Notf(Instruction):
    def f(self, ops, gdata):
        one_op_arith(ops, gdata, self.name, opfs.inv)
        return ''

class Inc(Instruction):
    def f(self, ops, gdata):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() + 1)
        return ''

class Dec(Instruction):
    def f(self, ops, gdata):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() - 1)
        return ''

class Neg(Instruction):
    def f(self, ops, gdata):
        one_op_arith(ops, gdata, self.name, opfs.neg)
        return ''

class Idiv(Instruction):
    def f(self, ops, gdata):
        check_num_args(self.name, ops, 1)
    
        hireg = int(gdata.registers['EDX']) << 32
        lowreg = int(gdata.registers['EAX'])
        dividend = hireg + lowreg
        gdata.registers['EAX'] = dividend // ops[0].get_val()
        gdata.registers['EBX'] = dividend % ops[0].get_val()
        return ''
