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
        <descr>
            The 32 bit word value in Rt is added to the 32 bit word value in Rs
            to produce a 32 bit result. If the addition results in 32 bit 2's
            complement arithmetic overflow, the destination register is not
            modified and an Integer Overflow exception occurs. If the addition
            deos not overflow, the 32 bit result is placed into Rd.
        </descr>
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
        <descr>
            The 16 bit signed immediate is added to the 32 bit value in Rs to
            produce a 32 bit result. If the addition in 32 bit 2's complement
            arithmetic overflow, the destination register is not modified and
            an Integer Overflow exception occurs. If the addition does not
            overflow, the 32 bit result is placed into Rt.
        </descr>
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
        <descr>
            The 32 bit word value in Rt is subtracted from the 32 bit value in
            Rs to produce a 32 bit result. If the subtraction results in a 32
            bit 2's complement arithmetic overflow, then the destination
            register is not modified and an Integer Overflow exception occurs.
            If it does not overflow, the 32 bit result is placed into Rd.
        </descr>
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
        <descr>
            The 32 bit word value in Rt is multiplied by the 32 bit value in Rs
            to produce a 64 bit result. The upper 32 bits of the 64 bit result
            is placed in the special register HI, whereas the lower 32 bits are
            placed in the register LO. Use MFHI and MFLO to move the result to
            a general purpose register.
        </descr>
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
        <descr>
            Performs a bitwise AND operation on registers Rt and Rs and stores
            the result in register Rd. If the bit in both Rt and Rs is 1, Rd
            will get 1; otherwise it will get 0.
        </descr>
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
        <descr>
            Performs a bitwise AND operation on register Rs and a 16 bit sign-
            extended immediate extended to 32 bits and stores the result in
            register Rt. If the bit in both Rs and the immediate is 1, Rt gets
            a 1; otherwise it will get a 0.
        </descr>
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
        <descr>
            Performs a bitwise OR operation on registers Rs and Rt and stores
            the result in register Rd. If the bit in both Rs and Rt is 0, Rd
            gets a 0; otherwise it will get a 1.
        </descr>
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
        <descr>
            Performs a bitwise OR operation on register Rs and a 16 bit sign-
            extended immediate extended to 32 bits and stores the result in Rt.
            If the bit in both Rs and the immediate is 0, Rt gets a 0;
            otherwise it will get a 1.
        </descr>
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
        <descr>
            Performs a bitwise NOR operation on registers Rs and Rt and stores
            the result in register Rd. If the bit in both Rs and Rt is 0, Rd
            gets a 1; otherwise it will get a 0.
        </descr>
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
        <descr>
            Performs a bitwise XOR operation on registers Rs and Rt and stores
            the result in register Rd. If the bit in Rs and Rt is different, Rd
            gets a 1; otherwise it will get a 0.
        </descr>
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
        <descr>
            The 32 bit word value in register Rs is shifted to the left by a
            number of bits specified by the 16 bit immediate. The result is
            stored as a 32 bit word value in register Rt. This is equivalent
            to multiplying by a power of 2. Bits shifted beyond the boundary of
            Rt are discarded.
        </descr>
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
        <descr>
            The 32 bit word value in register Rs is shifted to the right by a
            number of bits specified by the 16 bit immediate. The result is
            stored as a 32 bit word value in register Rt. This is equivalent to
            dividing by a power of 2. Bits shifted beyond the boundary of Rt
            are discarded.
        </descr>
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
            The 32 bit word value in register Rs is divided by the 32 bit word
            value in register Rt. The 32 bit result of the division is stored
            in special register LO. The 32 bit modulus of the division is
            stored in the special register HI. Use MFHI and MFLO to move these
            results to general purpose registers.
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
