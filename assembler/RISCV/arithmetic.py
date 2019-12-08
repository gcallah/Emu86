'''
Arithmetic and Logical instructions for
RISC-V
'''
import operator as opfunc

from assembler.errors import check_num_args, IncorrectImmLength
from assembler.tokens import Instruction, MAX_INT
# from assembler.ops_check import one_op_arith
from .argument_check import check_reg_only, check_immediate_three
from .argument_check import check_immediate_two


def three_op_arith_reg(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3, line_num)
    check_reg_only(instr, ops, line_num)
    ops[0].set_val(check_overflow(operator(ops[1].get_val(line_num),
                   ops[2].get_val(line_num)), vm), line_num)
    vm.changes.add(ops[0].get_nm())


def three_op_arith_immediate(ops, vm, instr, operator, line_num):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 3, line_num)
    check_immediate_three(instr, ops, line_num)
    ops[0].set_val(check_overflow(operator(ops[1].get_val(line_num),
                   ops[2].get_val(line_num)), vm), line_num)
    vm.changes.add(ops[0].get_nm())


def get_three_ops(instr, ops, line_num):
    '''
    Function to grab the values in registers.
    Put in a separate so that we don't have to write out the checks
    all the time.

    '''
    check_num_args(instr, ops, 3, line_num)
    check_reg_only(instr, ops, line_num)
    return (ops[0], ops[1], ops[2])


def get_three_ops_imm(instr, ops, line_num):
    '''
    Same concept as the function above.
    '''
    check_num_args(instr, ops, 3, line_num)
    check_immediate_three(instr, ops, line_num)
    return (ops[0], ops[1], ops[2])


def get_two_op_imm(instr, ops, line_num):
    """
    Again, same as above, except for reg, imm format
    """
    check_num_args(instr, ops, 2, line_num)
    check_immediate_two(instr, ops, line_num)
    return (ops[0], ops[1])


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


class Mul(Instruction):
    """
        <instr>
            MUL
        </instr>
        <syntax>
            MUL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.mul, line_num)


class And(Instruction):
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


class Andi(Instruction):
    """
        <instr>
            ANDI
        </instr>
        <syntax>
            ANDI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.and_, line_num)


class Or(Instruction):
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


class Ori(Instruction):
    """
        <instr>
            ORI
        </instr>
        <syntax>
            ORI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.or_, line_num)


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


class Xori(Instruction):
    """
        <instr>
            XORI
        </instr>
        <syntax>
            XORI reg, reg, con
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.xor, line_num)


class Srl(Instruction):
    """
        <instr>
            SRL
        </instr>
        <syntax>
            SRL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 3, line_num)
        check_reg_only(self.name, ops, line_num)
        fixed_op2 = ops[2].get_val(line_num) % 32
        ops[0].set_val(check_overflow(opfunc.rshift(ops[1].get_val(line_num),
                       fixed_op2), vm), line_num)
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.rshift, line_num)


class Sll(Instruction):
    """
        <instr>
            SLL
        </instr>
        <syntax>
            SLL reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 3, line_num)
        check_reg_only(self.name, ops, line_num)
        fixed_op2 = ops[2].get_val(line_num) % 32
        ops[0].set_val(check_overflow(opfunc.lshift(ops[1].get_val(line_num),
                       fixed_op2), vm), line_num)
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
    def fhook(self, ops, vm, line_num):
        three_op_arith_immediate(ops, vm, self.name, opfunc.lshift, line_num)


class Slt(Instruction):
    """
        <instr>
            SLT
        </instr>
        <syntax>
            SLT reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops, line_num)
        if (op2.get_val(line_num) - op3.get_val(line_num)) < 0:
            op1.set_val(1, line_num)
        else:
            op1.set_val(0, line_num)
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
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops, line_num)
        abs_op2 = abs(op2.get_val(line_num))
        abs_op3 = abs(op3.get_val(line_num))
        if (abs_op2 - abs_op3) < 0:
            op1.set_val(1, line_num)
        else:
            op1.set_val(0, line_num)
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
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops, line_num)
        if (op2.get_val(line_num) - op3.get_val(line_num)) < 0:
            op1.set_val(1, line_num)
        else:
            op1.set_val(0, line_num)
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
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops, line_num)
        abs_op2 = abs(op2.get_val(line_num))
        abs_op3 = abs(op3.get_val(line_num))
        if (abs_op2 - abs_op3) < 0:
            op1.set_val(1, line_num)
        else:
            op1.set_val(0, line_num)
        vm.changes.add(op1.get_nm())


class Sra(Instruction):
    """
        <instr>
            SRA
        </instr>
        <syntax>
            SRA reg, reg, reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops, line_num)
        bin_str_op2 = bin(abs(op2.get_val(line_num)))[2:]
        if op2.get_val(line_num) >= 0:
            sign = '0'
        else:
            sign = '1'
        signed_str = sign * op3.get_val(line_num)
        shifted_str = signed_str + bin_str_op2[: - op3.get_val(line_num)]
        op1.set_val(int(shifted_str, 2), line_num)
        vm.changes.add(op1.get_nm())


class Srai(Instruction):
    """
        <instr>
            SRAI
        </instr>
        <syntax>
            SRAI reg, reg, imm
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops, line_num)
        bin_str_op2 = bin(abs(op2.get_val(line_num)))[2:]
        if op2.get_val(line_num) >= 0:
            sign = '0'
        else:
            sign = '1'
        signed_str = sign * op3.get_val(line_num)
        shifted_str = signed_str + bin_str_op2[: - op3.get_val(line_num)]
        op1.set_val(int(shifted_str, 2), line_num)
        vm.changes.add(op1.get_nm())


class Div(Instruction):
    """
    <instr>
        DIV
    </instr>
    <syntax>
        DIV reg, reg, reg
    </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.floordiv, line_num)


class Divu(Instruction):
    """
    <instr>
        DIVU
    </instr>
    <syntax>
        DIVU reg, reg, reg
    </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 3, line_num)
        check_reg_only(self.name, ops, line_num)
        ops[0].set_val(
            check_overflow(
                opfunc.floordiv(
                    abs(ops[1].get_val(line_num)),
                    abs(ops[2].get_val(line_num))
                ), vm
            ),
            line_num
        )
        vm.changes.add(ops[0].get_nm())


class Rem(Instruction):
    """
    <instr>
        REM
    </instr>
    <syntax>
        REM reg, reg, reg
    </syntax>
    """
    def fhook(self, ops, vm, line_num):
        three_op_arith_reg(ops, vm, self.name, opfunc.mod, line_num)


class Remu(Instruction):
    """
    <instr>
        REMU
    </instr>
    <syntax>
        REMU reg, reg, reg
    </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.name, ops, 3, line_num)
        check_reg_only(self.name, ops, line_num)
        ops[0].set_val(
            check_overflow(
                opfunc.mod(
                       abs(ops[1].get_val(line_num)),
                       abs(ops[2].get_val(line_num))
                ), vm),
            line_num
        )
        vm.changes.add(ops[0].get_nm())


class Lui(Instruction):
    """
    <instr>
        LUI
    </instr>
    <syntax>
        LUI reg, imm
    </syntax>
    <desc>
        Loads a constant (EXPECTED TO BE 20 BITS MAX)
        That's been shifted left by 12 bits
    </desc>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2) = get_two_op_imm(self.get_nm(), ops, line_num)
        if op2.get_val(line_num) > 1048576:
            raise IncorrectImmLength(op2.get_val(line_num), line_num)
        # print(op2.get_val(line_num))
        op1.set_val(check_overflow(opfunc.lshift(op2.get_val(line_num),
                    12), vm), line_num)
        # print(op1.get_val(line_num))
        vm.changes.add(op1.get_nm())


'''
# class Auipc(Instruction):
    """
    <instr>
        AUIPC
    </instr>
    <syntax>
        AUIPC reg, reg, reg
    </syntax>
    """
    # Does lui, and then adds that value to the PC
    # instead of loading to a register.

# class Mulh(Instruction):
    """
    <instr>
        MULH
    </instr>
    <syntax>
        MULH reg, reg, reg
    </syntax>
    """


# class Mulhu(Instruction):
    """
    <instr>
        MULHU
    </instr>
    <syntax>
        MULHU reg, reg, reg
    </syntax>
    """


# class Mulhsu(Instruction):
    """
    <instr>
        MULHSU
    </instr>
    <syntax>
        MULHSU reg, reg, reg
    </syntax>
    """
'''
