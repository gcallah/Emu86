"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from .errors import *
from .tokens import Instruction, MAX_INT, Register, IntegerTok


def one_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1)
    ops[0].set_val(operator(ops[0].get_val()))


def two_op_arith_reg(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    if (isinstance(ops[0], Register) and 
        isinstance(ops[1], Register) and 
        isinstance(ops[2], Register)):
            ops[0].set_val(
            checkflag(operator(ops[1].get_val(),
                               ops[2].get_val()), 
                               vm))

def two_op_arith_immediate(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    if isinstance(ops[0], Register):
        print ("YO")
        if ((isinstance(ops[1], IntegerTok) and isinstance(ops[2], Register)) or
            (isinstance(ops[1], Register) and isinstance(ops[2], IntegerTok))):
            print (ops[1].get_val(), ops[2].get_val())
            ops[0].set_val(
            checkflag(operator(ops[1].get_val(),
                               ops[2].get_val()), 
                               vm))
            print (ops[0].get_val())


def checkflag(val, vm):
    if(val > MAX_INT):
        vm.flags['CF'] = 1
        val = val - MAX_INT+1
    else:
        vm.flags['CF'] = 0
    return val


class Add_MIPS(Instruction):
    """
        <instr>
             ADD
        </instr>
        <syntax>
            ADD reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_reg(ops, vm, self.name, opfunc.add)

class Addi(Instruction):
    """
        <instr>
             ADD
        </instr>
        <syntax>
            ADD reg, reg, con
            ADD reg, con, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        print (self.name)
        print (ops)
        two_op_arith_immediate(ops, vm, self.name, opfunc.add)

class Sub_MIPS(Instruction):
    """
        <instr>
             SUB
        </instr>
        <syntax>
            SUB reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_reg(ops, vm, self.name, opfunc.sub)

class Subi(Instruction):
    """
        <instr>
             SUB
        </instr>
        <syntax>
            SUB reg, reg, con
            SUB reg, con, reg
        </syntax>
    """
    def fhook_immediate(self, ops, vm):
        two_op_arith_immediate(ops, vm, self.name, opfunc.sub)

class Imul_MIPS(Instruction):
    """
        <instr>
             IMUL
        </instr>
        <syntax>
            IMUL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_reg(ops, vm, self.name, opfunc.mul)
        return ''

class Andf_MIPS(Instruction):
    """
        <instr>
             AND
        </instr>
        <syntax>
            AND reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_reg(ops, vm, self.name, opfunc.and_)
        return ''

class Andi(Instruction):
    """
        <instr>
             AND
        </instr>
        <syntax>
            AND reg, con, reg
            AND reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_immediate(ops, vm, self.name, opfunc.and_)
        return ''

class Orf_MIPS(Instruction):
    """
        <instr>
             OR
        </instr>
        <syntax>
            OR reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_reg(ops, vm, self.name, opfunc.or_)
        return ''

class Ori(Instruction):
    """
        <instr>
             OR
        </instr>
        <syntax>
            OR reg, con, reg
            OR reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith_immediate(ops, vm, self.name, opfunc.or_)
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
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.xor)
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
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.lshift)
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
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.rshift)

class Notf(Instruction):
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

class Inc(Instruction):
    """
        <instr>
             inc
        </instr>
        <syntax>
            INC reg
        </syntax>
    """
    def fhook(self, ops, vm):
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
    def fhook(self, ops, vm):
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
    def fhook(self, ops, vm):
        one_op_arith(ops, vm, self.name, opfunc.neg)
        return ''

class Idiv(Instruction):
    """
        <instr>
             idiv
        </instr>
        <syntax>
            IDIV reg
        </syntax>
        <descr>
            The idiv instruction divides the contents of
            the 64 bit integer EDX:EAX (constructed by viewing
            EDX as the most significant four bytes and EAX
            as the least significant four bytes) by the
            specified operand value. The quotient result
            of the division is stored into EAX, while the
            remainder is placed in EDX.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
    
        hireg = int(vm.registers['EDX']) << 32
        lowreg = int(vm.registers['EAX'])
        dividend = hireg + lowreg
        vm.registers['EAX'] = dividend // ops[0].get_val()
        vm.registers['EDX'] = dividend % ops[0].get_val()
        return ''
