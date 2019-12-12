"""
arithmetic.py: arithmetic instructions.
"""

import operator as opfunc
from assembler.errors import DivisionZero
from assembler.tokens import Instruction, MAX_INT


def get_stack_operand(vm):
    position = hex(vm.get_sp()).split('x')[-1].upper()
    val_one = vm.stack[position]
    vm.stack[position] = 0
    return val_one


def get_stack_operands(vm, line_num):
    vm.dec_sp(line_num)
    val_one = get_stack_operand(vm)
    vm.dec_sp(line_num)
    val_two = get_stack_operand(vm)
    return val_one, val_two


def two_op_arith(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    val_one, val_two = get_stack_operands(vm, line_num)
    # vm.dec_sp(line_num)
    position = hex(vm.get_sp()).split('x')[-1].upper()
    vm.stack[position] = operator(val_one, val_two)
    vm.inc_sp(line_num)


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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.add, line_num)


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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.sub, line_num)


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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.mul, line_num)


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
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.floordiv, line_num)


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
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        if val_two == 0:
            raise DivisionZero(line_num)
        result = opfunc.floordiv(abs(val_one), abs(val_two))
        check_overflow(result, vm)
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Rem_S(Instruction):
    """
        <instr>
             .rem_s
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.rem_s
        </syntax>
        <descr>
            This is the remainder instruction for signed values.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.mod, line_num)


class Rem_U(Instruction):
    """
        <instr>
             .rem_u
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.rem_u
        </syntax>
        <descr>
            This is the remainder instruction for unsigned values.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        result = opfunc.mod(abs(val_one), abs(val_two))
        check_overflow(result, vm)
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class And(Instruction):
    """
        <instr>
             .and
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.and
        </syntax>
        <descr>
            $lhs and $rhs are example variables
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.and_, line_num)


class Or(Instruction):
    """
        <instr>
             .or
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.or
        </syntax>
        <descr>
            $lhs and $rhs are example variables
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.or_, line_num)


class Xor(Instruction):
    """
        <instr>
             .xor
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.xor
        </syntax>
        <descr>
            $lhs and $rhs are example variables
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        two_op_arith(ops, vm, self.name, opfunc.xor, line_num)


class Shl(Instruction):
    """
        <instr>
             .shl
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.shl
        </syntax>
        <descr>
            Integer Shift Left
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        val_two = val_two % 32  # only for i32
        result = opfunc.lshift(val_one, val_two)
        check_overflow(result, vm)
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Shr_S(Instruction):
    """
        <instr>
             .shr_s
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.shr_s
        </syntax>
        <descr>
            Integer Shift Right Signed
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        val_two = val_two % 32  # only for i32
        result = opfunc.rshift(val_one, val_two)
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Shr_U(Instruction):
    """
        <instr>
             .shr_u
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.shr_u
        </syntax>
        <descr>
            Integer Shift Right Unsigned
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        val_one_abs = abs(val_one)
        val_two_abs = abs(val_two)
        val_two_abs = val_two_abs % 32  # only for i32
        result = opfunc.rshift(val_one_abs, val_two_abs)
        check_overflow(result, vm)
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Rotl(Instruction):
    """
        <instr>
             .rotl
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.rotl
        </syntax>
        <descr>
            Integer Rotate Left
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        val_one = abs(val_one)
        val_two = abs(val_two)
        val_one_bin = bin(val_one)[2:]
        diff = 0
        if len(val_one_bin) < 32:
            diff = 32 - len(val_one_bin)
        for i in range(0, diff):
            val_one_bin = "0" + val_one_bin
        val_two = val_two % 32  # only for i32
        result = val_one_bin[val_two:] + val_one_bin[:val_two]
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = int(result, 2)
        vm.inc_sp(line_num)


class Rotr(Instruction):
    """
        <instr>
             .rotr
        </instr>
        <syntax>
            get_local $lhs
            get_local $rhs
            i32.rotr
        </syntax>
        <descr>
            Integer Rotate Right
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        val_one, val_two = get_stack_operands(vm, line_num)
        val_one = abs(val_one)
        val_two = abs(val_two)
        val_one_bin = bin(val_one)[2:]
        diff = 0
        if len(val_one_bin) < 32:
            diff = 32 - len(val_one_bin)
        for i in range(0, diff):
            val_one_bin = "0" + val_one_bin
        val_two = val_two % 32  # only for i32
        first_part = val_one_bin[-val_two:]
        second_part = val_one_bin[: len(val_one_bin) - val_two]
        result = first_part + second_part
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = int(result, 2)
        vm.inc_sp(line_num)


class Clz(Instruction):
    """
        <instr>
             .clz
        </instr>
        <syntax>
            get_local $lhs
            i32.clz
        </syntax>
        <descr>
            Integer Count Leading Zeros
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        vm.dec_sp(line_num)
        val_one = get_stack_operand(vm)
        val_one_bin = bin(val_one)[2:]
        result = 0
        for i in val_one_bin:
            if i == "0":
                result += 1
            else:
                break
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Ctz(Instruction):
    """
        <instr>
             .clz
        </instr>
        <syntax>
            get_local $lhs
            i32.clz
        </syntax>
        <descr>
            Integer Count Trailing Zeros
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        vm.dec_sp(line_num)
        val_one = get_stack_operand(vm)
        val_one_bin = bin(val_one)[2:]
        result = 0
        for i in val_one_bin[::-1]:
            if i == "0":
                result += 1
            else:
                break
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Popcnt(Instruction):
    """
        <instr>
             .popcnt
        </instr>
        <syntax>
            get_local $lhs
            i32.popcnt
        </syntax>
        <descr>
            Integer Population Count
            returns the number of 1-bits in its operand
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        vm.dec_sp(line_num)
        val_one = get_stack_operand(vm)
        val_one_bin = bin(val_one)[2:]
        result = 0
        for i in val_one_bin:
            if i == "1":
                result += 1
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)


class Eqz(Instruction):
    """
        <instr>
             .eqz
        </instr>
        <syntax>
            get_local $lhs
            i32.eqz
        </syntax>
        <descr>
            Integer Equal To Zero
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        vm.dec_sp(line_num)
        val_one = get_stack_operand(vm)
        result = False
        if val_one == 0:
            result = True
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = result
        vm.inc_sp(line_num)
