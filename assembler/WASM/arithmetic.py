"""
arithmetic.py: arithmetic instructions.
"""

import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction, MAX_INT


def two_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    sp = vm.get_sp()
    val_one = vm.stack[hex(sp).split('x')[-1].upper()]
    vm.stack[hex(sp).split('x')[-1].upper()] = 0
    vm.dec_sp()
    sp = vm.get_sp()
    val_two = vm.stack[hex(sp).split('x')[-1].upper()]
    vm.stack[hex(sp).split('x')[-1].upper()] = operator(val_one, val_two)


def check_overflow(val, vm):
    '''
    To emulate the wraparound that occurs when a number
    has too many bits to represent in machine code.

    '''
    if (val > MAX_INT):
        val = val - MAX_INT + 1
    return val


class Add(Instruction):
    """
        <instr>
             .add
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.add
        </syntax>
        <descr>
            $lhs and $rhs are example variables
        </descr>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.add)


class Sub(Instruction):
    """
        <instr>
             .sub
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.sub
        </syntax>
        <descr>
            $lhs and $rhs are example variables
        </descr>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.sub)


class Mul(Instruction):
    """
        <instr>
             .mul
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.mul
        </syntax>
        <descr>
            $lhs and $rhs are example variables
        </descr>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.mul)


class Div_S(Instruction):
    """
        <instr>
             .div_s
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.div_s
        </syntax>
        <descr>
            This is the division instruction for signed values.
        </descr>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.floordiv)


class Div_U(Instruction):
    """
        <instr>
             .div_u
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.div_u
        </syntax>
        <descr>
            This is the division instruction for unsigned values.
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 2)
        ops[0].set_val(check_overflow(opfunc.floordiv(
                       abs(ops[1].get_val()), abs(ops[2].get_val())), vm))
        vm.changes.add(ops[0].get_nm())
