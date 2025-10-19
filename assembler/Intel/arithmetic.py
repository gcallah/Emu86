"""
arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import DivisionZero, check_num_args, InvalidConVal
from assembler.errors import InvalidOperand
from assembler.tokens import Instruction, MAX_INT, Register, MIN_INT
from assembler.ops_check import one_op_arith


def two_op_arith(ops, vm, instr, line_num, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2, line_num)
    ops[0].set_val(
        checkflag(operator(ops[0].get_val(line_num),
                           ops[1].get_val(line_num)), vm, operator), line_num)
    vm.changes.add(ops[0].get_nm())


def checkflag(val, vm, operator):
    if(operator == opfunc.add):
        if(val > MAX_INT):
            vm.flags['CF'] = 1
            vm.flags['OF'] = 1
            vm.flags['SF'] = 1
            vm.flags['ZF'] = 0
            val = (val - MAX_INT) + MIN_INT
        elif(val == 0):
            vm.flags['ZF'] = 1
        else:
            vm.flags['CF'] = 0
            vm.flags['OF'] = 0
            vm.flags['SF'] = 0
            vm.flags['ZF'] = 0
    elif(operator == opfunc.sub):
        vm.flags['CF'] = 0
        vm.flags['OF'] = 0
        vm.flags['SF'] = 0
        vm.flags['ZF'] = 0
        if(val == 0):
            vm.flags['ZF'] = 1
        if(val < 0):
            vm.flags['CF'] = 1
        if(val < MIN_INT):
            vm.flags['OF'] = 1
            vm.flags['SF'] = 1
            val = MAX_INT - (MIN_INT - val) + 1
    elif(operator == opfunc.mul):
        if(val > MAX_INT):
            vm.flags['CF'] = 1
            vm.flags['OF'] = 1
            val = val & 0x7FFFFFFF
        elif(val < MIN_INT):
            vm.flags['CF'] = 1
            vm.flags['OF'] = 1
            val = val & 0xFFFFFFFF
            val = val | 0x80000000
    elif(operator == opfunc.and_ or
         operator == opfunc.or_ or
         operator == opfunc.xor):
        vm.flags['CF'] = 0
        vm.flags['OF'] = 0
        if(val == 0):
            vm.flags['ZF'] = 1
        else:
            vm.flags['ZF'] = 0
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
        <descr>
            Adds the first operand with the second and stores the result in
            the first operand. The destination can be a register or memory
            location; the source can be an immediate, register, or memory
            location. Two memory operands cannot be used. Immediate values are
            sign extended. Works on both signed and unsigned integer operands.
        </descr>
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
        <descr>
            Subtracts the second operand from the first operand and stores the
            result in the first operand. The destination can be a register or
            memory location; the source can be an immediate, register, or
            memory location. Two memory operands cannot be used. Immediate
            values are sign extended. Evaluates the result for both signed
            and unsigned integer operands.
        </descr>
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
        <descr>
            Performs a signed multiplication of two operands. The first
            operand is multiplied by the second operand. The destination is a
            general purpose register and the source can be an immediate, a
            register, or a memory location. The product is truncated and
            stored in the destination operand location.
        </descr>
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
        <descr>
            Performs a bitwise AND operation on the destination (first) and
            source (second) operands and stores the result in the destination
            operand location. The source operand can be an immediate, a
            register, or a memory location; the destination operand can be a
            register or memory location. Two memory operands cannot be used in
            one instruction. Each bit of the result is set to 1 if both
            corresponding bits of the first and second operands are 1;
            otherwise it is set to 0.
        </descr>
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
        <descr>
            Performs a bitwise inclusive OR operation between the destination
            (first) and source (second) operands and stores the result in the
            destination operand location. The source operand can be an
            immediate, a register, or a memory location; the destination
            operand can be a register or a memory location. Two memory
            operands cannot be used in one instruction. Each bit of the result
            of the OR instruction is set to 0 if both corresponding bits of
            the first and second operands are 0; otherwise, each bit is set to
            1.
        </descr>
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
        <descr>
            Performs a bitwise exlcusive OR (XOR) operation on the destination
            (first) and source (second) operands and stores the result in the
            destination operand location. The source operand can be an
            immediate, a register, or a memory location; the destination
            operand can be a register or a memory location. Two memory
            operands cannot be used in one instruction. Each bit of the result
            is 1 if the corresponding bits of the operands are different; each
            bit is 0 if the corresponding bits are the same.
        </descr>
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
        <descr>
            Shifts the bits in the first operand (destination operand) to the
            left by the number of bits specified in the second operand
            (count operand). Bits shifted beyonf the destination operand
            boundary are first shifted into the CF flag, then discarded. At the
            end of the shift operation, the CF flag contains the last bit
            shifted out of the destination operand.
            The destination operand can be a register or a memory location. The
            count operand can be an immediate value or the CL register.
        </descr>
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
        <descr>
            Shifts the bits in the first operand (destination operand) to the
            right by the number of bits specified in the second operand
            (count operand). Bits shifted beyond the destination operand
            boundary are first shifted into the CF flag, then discarded. At the
            end of the shift operation, the CF flag contains the last bit
            shifted out of the destination operand.
            The destination operand can be a register or a memory location. The
            count operand can be an immediate value or a register.
        </descr>
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
        <descr>
            Performs a bitwise NOT operation (each 1 is set to 0, and each 0 is
            set to 1) on the destination operand and stores the result in the
            destination operand location. The destination operand is a
            register.
        </descr>
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
        <descr>
            Adds 1 to the destination operand, while preserving the state of
            the CF flag. The destination operand must be a register. This
            instruction allows a loop counter to be updated without disturbing
            the CF flag. (Use an ADD instriction with an immediate operand of 1
            to perform an increment operation that does update the CF flag.)
        </descr>
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
        <descr>
            Subtracts 1 from the destination operand, while preserving the
            state of the CF flag. The destination operand must be a register.
            This instruction allows a loop counter to be updated without
            disturbing the CF flag. (To perform a decrement operation that
            updates the CF flag, use a SUB instruction with an immediate
            operand of 1.)
        </descr>
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
           Replaces the value of operand (the destination operand) with its
           two's complement. (This operation is equivalent to subracting the
           operand from 0.) The destination operand is located in a general-
           purpose register.
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
            The idiv instruction divides the contents of the 64 bit integer
            EDX:EAX (constructed by viewing EDX as the most significant four
            bytes and EAX as the least significant four bytes) by the specified
            operand value. The quotient result of the division is stored into
            EAX, while the remainder is placed in EDX.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 1, line_num)

        hireg = int(vm.registers['EDX']) << 32
        lowreg = int(vm.registers['EAX'])
        dividend = hireg + lowreg
        if ops[0].get_val(line_num) == 0:
            raise DivisionZero( line_num )
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
    <descr>
        Selects the bit in a bit string (specified with the first operand,
        called the bit base) at the bit-position designated by the bit offset
        operand (second operand), stores the value of the bit in the CF flag,
        and clears the selected bit in the bit string to 0. The bit base
        operand can be a register or a memory location; the bit offset operand
        can be a register or an immediate value.
        If the bit base operand is a register, the instruction takes the modulo
        16, 32, or 64 of the bit offset operand (modulo size depends on the
        mode and register size). This allows any bit position to be selected.
    </descr>
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
    <descr>
        Selects the bit in a bit string (specified with the first operand,
        called the bit base) at the bit-position designated by the bit offset
        operand (second operand), stores the value of the bit in the CF flag,
        and sets the selected bit in the bit string to 1. The bit base operand
        is a register; the bit offset operand can be a register or an immediate
        value.
        If the bit base operand is a register, the instruction takes the modulo
        16, 32, or 64 of the bit offset operand (modulo size depends on the
        mode and register size.) This allows any bit position to be selected.
    </descr>
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
    <descr>
        Searches the source operand (second operand) for the least significant
        set bit (1 bit). If a least significant 1 bit is found, its bit index
        is stored in the destination operand (first operand). The source
        operand can be a register or memory location; the destination operand
        is a register. The bit index is an unsigned offset from bit 0 of the
        source operand. If the content of the source operand is 0, the content
        of the destination operand is undefined.
    </descr>
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
    <descr>
        Searches the source operand (second operand) for the most significant
        set bit (1 bit). If a most significant 1 bit is found, its bit index is
        stored in the destination operand (first operand). The source operand
        can be a register or a memory location; the destination operand is a
        register. The bit index is an unsigned offset from bit 0 of the source
        operand. If the content source operand is 0, the content of the
        destination operand is undefined.
    </descr>
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
    <descr>
        Selects the bit in a bit string (specified with the first operand,
        called the bit base) at the bit-position designated by the bit offset
        (specified by the second operand) and stores the value of the bit in
        the CF flag. The bit base operand is a register; the bit offset operand
        can be a register or an immediate value. The instruction takes the
        modulo 16, 32, or 64 of the bit offset operand (modulo size depends on
        the mode and register size).
    </descr>
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
    <descr>
        Selects the bit in a bit string (specified with the first operand,
        called the bit base) at the bit-position desginated by the bit offset
        operand (second operand), stores the value of the bit in the CF flag,
        and complements the selected bit in the bit string. The bit base
        operand is a register; the bit offset operand can be a register or an
        immediate value. The instruction takes the modulo 16, 32, or 64 of the
        bit offset operand (modulo size depends on the mode and register size).
    </descr>
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
