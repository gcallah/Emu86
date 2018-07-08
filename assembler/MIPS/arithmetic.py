"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT, Register, IntegerTok
from .argument_check import * 


def one_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1)
    ops[0].set_val(operator(ops[0].get_val()))

def three_op_arith_reg(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)
    ops[0].set_val(
    checkflag(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm))

def three_op_arith_immediate(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_immediate_three(instr, ops)
    ops[0].set_val(
    checkflag(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm))

def checkflag(val, vm):
    if(val > MAX_INT):
        vm.flags['CF'] = 1
        val = val - MAX_INT+1
    else:
        vm.flags['CF'] = 0
    return val


class Add(Instruction):
    """
        <instr>
             ADD
        </instr>
        <syntax>
            ADD reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.add)

class Addi(Instruction):
    """
        <instr>
             ADDI
        </instr>
        <syntax>
            ADDI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.add)

class Sub(Instruction):
    """
        <instr>
             SUB
        </instr>
        <syntax>
            SUB reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.sub)

class Subi(Instruction):
    """
        <instr>
             SUBI
        </instr>
        <syntax>
            SUBI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.sub)

class Mult(Instruction):
    """
        <instr>
             MULT
        </instr>
        <syntax>
            MULT reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 2)
        check_reg_only(self.name, ops)
        result = ops[0].get_val() * ops[1].get_val()
        if result > 2 ** 32 - 1:
            vm.registers['LO'] = opfunc.lshift(result, 32)
            vm.registers['HI'] = opfunc.rshift(result, 32)
        else:
            vm.registers['LO'] = result
            vm.registers['HI'] = 0
        return ''

class Andf(Instruction):
    """
        <instr>
             AND
        </instr>
        <syntax>
            AND reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.and_)
        return ''

class Andi(Instruction):
    """
        <instr>
             AND
        </instr>
        <syntax>
            ANDI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.and_)
        return ''

class Orf(Instruction):
    """
        <instr>
             OR
        </instr>
        <syntax>
            OR reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.or_)
        return ''

class Ori(Instruction):
    """
        <instr>
             OR
        </instr>
        <syntax>
            ORI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.or_)
        return ''

class Nor(Instruction):
    """
        <instr>
             NOR
        </instr>
        <syntax>
            NOR reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.or_)
        ops[0].set_val(opfunc.inv(ops[0].get_val()))
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

class Sll(Instruction):
    """
        <instr>
             sll
        </instr>
        <syntax>
            SLL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.lshift)
        return ''

class Srl(Instruction):
    """
        <instr>
             srl
        </instr>
        <syntax>
            SRL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.rshift)

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

class Div(Instruction):
    """
        <instr>
             DIV
        </instr>
        <syntax>
            DIV reg, reg
        </syntax>
        <descr>
            The div instruction divides the contents of
            the two registers. The quotient result
            of the division is stored into LO, while the
            remainder is placed in HI.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 2)
        check_reg_only(self.name, ops)
        if ops[1].get_val() == 0:
            raise DivisionZero()

        quotient = ops[0].get_val() // ops[1].get_val()
        remainder = ops[0].get_val() % ops[1].get_val()
        vm.registers['LO'] = quotient
        vm.registers['HI'] = remainder
        return ''

class Mfhi(Instruction):
    """
        <instr>
             mfhi
        </instr>
        <syntax>
            MFHI reg
        </syntax>
        <descr>
            Moves the value from the HI register into the 
            destination register given.
    """

    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
        if not isinstance(ops[0], Register):
            raise InvalidArgument(ops[0].get_nm())
        ops[0].set_val(vm.registers['HI'])
        return ''

class Mflo(Instruction):
    """
        <instr>
             mflo
        </instr>
        <syntax>
            MFLO reg
        </syntax>
        <descr>
            Moves the value from the LO register into the 
            destination register given.
    """

    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
        if not isinstance(ops[0], Register):
            raise InvalidArgument(ops[0].get_nm())
        ops[0].set_val(vm.registers['LO'])
        return ''
        
