'''
Contains the arithmetic and logical instructions for 
RISC V

There is a good amount of overlap between the
'''
import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT, Register, IntegerTok
from assembler.ops_check import one_op_arith
from .argument_check import * 

def three_op_arith_reg(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)
    ops[0].set_val(
    check_overflow(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm)) 
    if operator == opfunc.sub:
        ops[1].get_val(), ops[2].get_val()
    vm.changes.add(ops[0].get_nm())

def three_op_arith_immediate(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3)
    check_immediate_three(instr, ops)
    ops[0].set_val(
    check_overflow(operator(ops[1].get_val(),
                       ops[2].get_val()), 
                       vm))
    vm.changes.add(ops[0].get_nm()) 

def check_overflow(val, vm):
    '''
    To emulate the wraparound that occurs when a number 
    has too many bits to represent in machine code. 

    '''
    if (val > MAX_INT): 
        val = val - MAX_INT+1
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


class Mul(Instruction):
    """
        <instr>
            MUL
        </instr>
        <syntax>
            MUL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm): 
        three_op_arith_reg(ops, vm, self.name, opfunc.mul)

class And(Instruction):
    """
        <instr>
            AND
        </instr>
        <syntax>
            AND reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm): 
        three_op_arith_reg(ops , vm, self.name, opfunc.and_)

class Andi(Instruction):
    """
        <instr>
            ANDI
        </instr>
        <syntax>
            ANDI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.and_)

class Or(Instruction):
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

class Ori(Instruction):
    """
        <instr>
            ORI
        </instr>
        <syntax>
            ORI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.or_)

class Xor(Instruction):
    """
        <instr>
            XOR
        </instr>
        <syntax>
            XOR reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_reg(ops, vm, self.name, opfunc.xor)
        
class Xori(Instruction):
    """
        <instr>
            XORI
        </instr>
        <syntax>
            XORI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm): 
        three_op_arith_immediate(ops, vm, self.name, opfunc.xor)

class Srl(Instruction):
    """
        <instr>
            SRL  
        </instr>
        <syntax>
            SRL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.rshift)

class Sll(Instruction):
    """
        <instr>
            SLL
        </instr>
        <syntax>
            SLL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        three_op_arith_immediate(ops, vm, self.name, opfunc.lshift)