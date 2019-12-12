"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import DivisionZero, check_num_args, InvalidConVal
from assembler.errors import InvalidOperand
from assembler.tokens import Instruction, MAX_INT, Register
from assembler.ops_check import one_op_arith


def two_op_arith(ops, vm, instr, line_num, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2, line_num)
    ops[0].set_val(
        checkflag(operator(ops[0].get_val(line_num),
                           ops[1].get_val(line_num)), vm), line_num)
    vm.changes.add(ops[0].get_nm())


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
             add
        </instr>
        <syntax>
            ADD reg, reg
            ADD reg, mem
            ADD reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.add)


class Sub(Instruction):
    """
        <instr>
             sub
        </instr>
        <syntax>
            SUB reg, reg
            SUB reg, mem
            SUB reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.sub)


class Imul(Instruction):
    """
        <instr>
             imul
        </instr>
        <syntax>
            IMUL reg, reg
            IMUL reg, mem
            IMUL reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.mul)
        return ''


class Andf(Instruction):
    """
        <instr>
             and
        </instr>
        <syntax>
            AND reg, reg
            AND reg, mem
            AND reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.and_)
        return ''


class Orf(Instruction):
    """
        <instr>
             or
        </instr>
        <syntax>
            OR reg, reg
            OR reg, mem
            OR reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.or_)
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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.xor)
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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.lshift)
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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, line_num, opfunc.rshift)


class Notf(Instruction):
    """
        <instr>
             not
        </instr>
        <syntax>
            NOT reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        one_op_arith(ops, vm, self.name, line_num, opfunc.inv)


class Inc(Instruction):
    """
        <instr>
             inc
        </instr>
        <syntax>
            INC reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 1, line_num)
        ops[0].set_val(ops[0].get_val(line_num) + 1, line_num)
        vm.changes.add(ops[0].get_nm())


class Dec(Instruction):
    """
        <instr>
             dec
        </instr>
        <syntax>
            DEC reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 1, line_num)
        ops[0].set_val(ops[0].get_val(line_num) - 1, line_num)
        vm.changes.add(ops[0].get_nm())


class Neg(Instruction):
    """
        <instr>
             neg
        </instr>
        <syntax>
            NEG reg
        </syntax>
        <descr>
           Replaces the value of operand with
           it's two's complement.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        one_op_arith(ops, vm, self.name, line_num, opfunc.neg)
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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 1, line_num)

        hireg = int(vm.registers['EDX']) << 32
        lowreg = int(vm.registers['EAX'])
        dividend = hireg + lowreg
        if ops[0].get_val(line_num) == 0:
            raise DivisionZero()
        vm.registers['EAX'] = dividend // ops[0].get_val(line_num)
        vm.registers['EDX'] = dividend % ops[0].get_val(line_num)
        vm.changes.add('EAX')
        vm.changes.add('EDX')
        return ''


class BTR(Instruction):
    """
    <instr>
        btr
    </instr>
    <syntax>
        btr reg, reg
        btr reg, const
    </syntax>
    """

    def fhook(self, ops, vmachine, line_num):
        check_num_args(self.name, ops, 2, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidOperand('Operand 1 is not of type Register', line_num)
        if ops[1].get_val(line_num).bit_length() >= 9:
            raise InvalidConVal(ops[1].get_nm(), line_num)
        ops[0].set_val(set_bit(ops[0].get_val(line_num),
                               ops[1].get_val(line_num), 0), line_num)


def set_bit(v, index, x):
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v


class BTS(Instruction):
    """
    <instr>
        bts
    </instr>
    <syntax>
        bts reg, reg
        bts reg, const
    </syntax>
    """

    def fhook(self, ops, vmachine, line_num):
        check_num_args(self.name, ops, 2, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidOperand('Operand 1 is not of type Register', line_num)
        if ops[1].get_val(line_num).bit_length() >= 9:
            raise InvalidConVal(ops[1].get_nm(), line_num)
        ops[0].set_val(set_bit(ops[0].get_val(line_num),
                               ops[1].get_val(line_num), 1), line_num)


class BSF(Instruction):
    """
    <instr>
        bsf
    </instr>
    <syntax>
        bsf reg, reg
        bsf reg, mem
    </syntax>
    """

    def fhook(self, ops, vmachine, line_num):
        check_num_args(self.name, ops, 2, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidOperand('Operand 1 is not of type Register', line_num)
        num = ops[1].get_val(line_num)

        if num == 0:
            vmachine.flags["ZF"] = 1
        else:
            vmachine.flags["ZF"] = 0
            if ops[1].get_val(line_num).bit_length() <= 16:
                bit_size = 16
            else:
                bit_size = 32
            bin_str = str(bin(num))[2:].zfill(bit_size)[::-1]
            for index in range(len(bin_str)):
                if bin_str[index] == '1':
                    break
            ops[0].set_val(index, line_num)


class BSR(Instruction):
    """
    <instr>
        bsr
    </instr>
    <syntax>
        bsr reg, reg
        bsr reg, mem
    </syntax>
    """

    def fhook(self, ops, vmachine, line_num):
        check_num_args(self.name, ops, 2, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidOperand('Operand 1 is notof type Register', line_num)
        num = ops[1].get_val(line_num)
        if num == 0:
            vmachine.flags["ZF"] = 1
        else:
            vmachine.flags["ZF"] = 0
            if ops[1].get_val(line_num).bit_length() <= 16:
                bit_size = 16
            else:
                bit_size = 32
            binStr = str(bin(num))[2:].zfill(bit_size)
            for index in range(len(binStr)):
                if binStr[index] == '1':
                    break
            index = bit_size - index
            ops[0].set_val(index, line_num)


class BT(Instruction):
    """
    <instr>
        bt
    </instr>
    <syntax>
        bt reg, reg
        bt reg, const
    </syntax>
    """

    def fhook(self, ops, vmachine, line_num):
        check_num_args(self.name, ops, 2, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidOperand('Operand 1 is not of type Register', line_num)
        # print('length', ops[1].get_val(line_num).bit_length())
        # if ops[1].get_val(line_num).bit_length() < 8:
        #     raise InvalidOperand('Operand 2 should be of size 8 bit')

        binary_num = bin(ops[0].get_val(line_num))
        index = len(binary_num) - ops[1].get_val(line_num)
        vmachine.flags["CF"] = binary_num[index]


class BTC(Instruction):
    """
    <instr>
        bt
    </instr>
    <syntax>
        bt reg, reg
        bt reg, const
    </syntax>
    """

    def fhook(self, ops, vmachine, line_num):
        check_num_args(self.name, ops, 2, line_num)
        if not isinstance(ops[0], Register):
            raise InvalidOperand('Operand 1 is not of type Register', line_num)
        # if ops[1].get_val(line_num).bit_length() != 8:
        #     raise InvalidOperand('Operand 2 should be of size 8 bit')

        binary_num = bin(ops[0].get_val(line_num))
        index = len(binary_num) - ops[1].get_val(line_num)
        if binary_num[index] == '1':
            complement = '0'
        else:
            complement = '1'
        vmachine.flags["CF"] = complement
