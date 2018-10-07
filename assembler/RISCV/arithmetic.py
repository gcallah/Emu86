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

'''
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
'''