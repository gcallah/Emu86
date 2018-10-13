'''
Arithmetic and Logical instructions for 
RISC-V
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


def get_three_ops(instr, ops):
    '''
    Function to grab the values in registers. 
    Put in a separate so that we don't have to write out the checks
    all the time. 

    '''
    check_num_args(instr, ops, 3)
    check_reg_only(instr, ops)
    return (ops[0], ops[1], ops[2])

def get_three_ops_imm(instr, ops):
    '''
    Same concept as the function above. 
    '''
    check_num_args(instr, ops, 3)
    check_immediate_three(instr, ops)
    return (ops[0], ops[1], ops[2])

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
        check_num_args(self.name, ops, 3)
        check_immediate_three(self.name, ops)
        fixed_op2 = ops[2].get_val() % 32
        ops[0].set_val(
        check_overflow(opfunc.rshift(ops[1].get_val(),
                       fixed_op2), 
                       vm))

        vm.changes.add(ops[0].get_nm()) 

class Srli(Instruction): 
    """
        <instr> 
            SRLI 
        </instr> 
        <syntax> 
            SRLI reg, reg, con
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
        check_num_args(self.name, ops, 3)
        check_immediate_three(self.name, ops)
        fixed_op2 = ops[2].get_val() % 32
        ops[0].set_val(
        check_overflow(opfunc.lshift(ops[1].get_val(),
                       fixed_op2), 
                       vm))

        vm.changes.add(ops[0].get_nm()) 

class Slli(Instruction): 
    """
        <instr> 
            SLLI 
        </instr> 
        <syntax> 
            SLLI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm): 
        three_op_arith_immediate(ops, vm, self.name, opfunc.lshift)

class Slt(Instruction):
    """
        <instr>
            SLT 
        </instr> 
        <syntax> 
            SLT reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops)   
        if (op2.get_val() - op3.get_val()) < 0: 
            op1.set_val(1)
        else: 
            op1.set_val(0)
        vm.changes.add(op1.get_nm())

class Sltu(Instruction):
    """
        <instr>
            SLTU 
        </instr> 
        <syntax> 
            SLTU reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops) 
        abs_op2 = abs(ops2.get_val())
        abs_op3 = abs(ops3.get_val())
        if (abs_op2 - abs_op3) < 0: 
            op1.set_val(1)
        else: 
            op1.set_val(0)
        vm.changes.add(op1.get_nm())

class Slti(Instruction):
    """
        <instr> 
            SLTI
        </instr> 
        <syntax> 
            SLTI reg, reg, con
        </syntax> 
    """
    def fhook(self, ops, vm):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops)   
        if (op2.get_val() - op3.get_val()) < 0: 
            op1.set_val(1)
        else: 
            op1.set_val(0)
        vm.changes.add(op1.get_nm())


class Sltiu(Instruction): 
    """
        <instr>
            SLTU 
        </instr> 
        <syntax> 
            SLTU reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops) 
        abs_op2 = abs(ops2.get_val())
        abs_op3 = abs(ops3.get_val())
        if (abs_op2 - abs_op3) < 0: 
            op1.set_val(1)
        else: 
            op1.set_val(0)
        vm.changes.add(op1.get_nm())

'''
>>>>>>>>>>>>>>>SLT: Set less than  
    reg reg reg 
    R-type
    0110011

>>>>>>>>>>>>>>SLTU: same as above, but unsigned.

>>>>>>>>>>>>>SLTI : Set gpr if source gpr < constant
signed comparison 
    reg reg con
    I-type 
    0010011

>>>>>>>>>>>>>SLTIU: same as above
unsigned comparison
    reg reg con
    I-type
    0010011

SRA: shift right arithmetic 
    reg reg reg 
    R-type
    0110011

SRAI: shift right arithmetic by constant 
    reg reg con
    I-type
    0010011

>>>>>>>>>SRLI: Shift right logical by constant
    reg reg con
    I-type
    0010011

>>>>>>>>SLLI: Shift left logical constant 
    reg reg con
    I-type
    0010011

LUI: Load constant into upper bits of word
    reg con
    I-type
    0110111

AUIPC: Load PC + constant into upper bits of word
    reg imm 
    I assume we load the contents of the stack pointer? not sure
    I-type 
    0010111



'''