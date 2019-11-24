"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc
from .argument_check import check_reg_only, check_immediate_three
from assembler.errors import check_num_args, DivisionZero, InvalidArgument

from assembler.tokens import Instruction, MAX_INT, Register


def three_op_arith_reg(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3, line_num)
    check_reg_only(instr, ops, line_num)
    ops[0].set_val(
        check_overflow(
            operator(ops[1].get_val(line_num),
                     ops[2].get_val(line_num)),
            vm),
        line_num)
    vm.changes.add(ops[0].get_nm())


def three_op_arith_immediate(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3, line_num)
    check_immediate_three(instr, ops, line_num)
    ops[0].set_val(
        check_overflow(
            operator(ops[1].get_val(line_num),
                     ops[2].get_val(line_num)),
            vm),
        line_num)
    vm.changes.add(ops[0].get_nm())


def check_overflow(val, vm):
    if(val > MAX_INT):
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.add, line_num)


class Addi(Instruction):
    """
        <instr>
             ADDI
        </instr>
        <syntax>
            ADDI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.add, line_num)


class Sub(Instruction):
    """
        <instr>
             SUB
        </instr>
        <syntax>
            SUB reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.sub, line_num)


class Mult(Instruction):
    """
        <instr>
             MULT
        </instr>
        <syntax>
            MULT reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 2, line_num)
        check_reg_only(self.name, ops, line_num)
        result = ops[0].get_val(line_num) * ops[1].get_val(line_num)
        if result > 2 ** 32 - 1:
            vm.registers['LO'] = opfunc.lshift(result, 32)
            vm.registers['HI'] = opfunc.rshift(result, 32)
        else:
            vm.registers['LO'] = result
            vm.registers['HI'] = 0
        vm.changes.add('LO')
        vm.changes.add('HI')
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.and_, line_num)
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.and_, line_num)
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.or_, line_num)
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.or_, line_num)
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.or_, line_num)
        ops[0].set_val(opfunc.inv(ops[0].get_val(line_num)), line_num)
        return ''


class Xor(Instruction):
    """
        <instr>
             XOR
        </instr>
        <syntax>
            XOR reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.xor, line_num)
        return ''


class Sll(Instruction):
    """
        <instr>
             sll
        </instr>
        <syntax>
            SLL reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.lshift, line_num)
        return ''


class Srl(Instruction):
    """
        <instr>
             srl
        </instr>
        <syntax>
            SRL reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.rshift, line_num)


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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 2, line_num)
        check_reg_only(self.name, ops, line_num)
        if ops[1].get_val(line_num) == 0:
            raise DivisionZero(line_num)

        quotient = ops[0].get_val(line_num) // ops[1].get_val(line_num)
        remainder = ops[0].get_val(line_num) % ops[1].get_val(line_num)
        vm.registers['LO'] = quotient
        vm.registers['HI'] = remainder
        vm.changes.add('LO')
        vm.changes.add('HI')
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
        </descr>
    """

    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 1, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidArgument(ops[0].get_nm(), line_num)
        ops[0].set_val(vm.registers['HI'], line_num)
        vm.changes.add(ops[0].get_nm())
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
        </descr>
    """

    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 1, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidArgument(ops[0].get_nm(), line_num)
        ops[0].set_val(vm.registers['LO'], line_num)
        vm.changes.add(ops[0].get_nm())
        return ''
