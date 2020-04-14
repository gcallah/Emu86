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
        <descr>
            Performs an add operation on the two source registers and stores
            the result in the desination register. Overflows are ignored.
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
            Adds the sign extended 12-bit immediate to the source register
            and stores the result in the destination register. Overflows are
            ignored.
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
            Performs a subtract operation on the two source registers and
            stores the result in the destination register. Overflows are 
            ignored.
        </descr>
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
        <descr>
            Performs a multiply operation on the two source registers and
            stores the lower 32 bits of the result in the destination register.
        </descr>
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
        <descr>
            Performs a bitwise AND operation on the two source registers and
            stores the result in the destination register. If the bit in both
            source registers is 1, then the destination register gets a 1;
            otherwise it gets a 0.
        </descr>
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
        <descr>
            Performs a bitwise AND operation on a source registers and a 12-bit
            sign extended immediate and stores the result in the destination
            register. If the bit in both the source register and the immediate
            is 1, then the destination register gets a 1; otherwise it gets a 0.
        </descr>
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
		<descr>
		    Performs a bitwise OR operation on two source registers and stores
		    the result in the destination register. If the bit in both source
			registers is a 0, then the destination register gets a 0; otherwise
			it gets a 1.
		</descr>
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
		<descr>
			Performs a bitwise OR operation on a source register and a 12-bit
			sign extended immediate and stores the result in the destination
			register. If the bit in both the source register and the immediate
			is 0, then the destination register gets a 0; otherwise it gets a 1.
		</descr>
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
		<descr>
			Performs a bitwise XOR operation on two source registers and stores
			the result in the destination register. If the bit in the source 
			registers is different, the destination register gets a 1; otherwise
			it gets a 0.
		</descr>
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
		<descr>
			Performs a bitwise XOR operation on a source register and a 12-bit 
			sign extended immediate and stores the result in the destination 
			register. If the bit in the source register and the immediate is
			different, the destination register gets a 1; otherwise it gets a 0.
		</descr>
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
		<descr>
			Performs a logical right shift on the register rs1 by the amount
			specified by the lower 5 bits of rs2. The result is stored in
			register rd.
		</descr>
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
		<descr>
			Performs a logical right shift on the register rs1 by the amount
			specified by the 12 bit immediate. The result is stored in register 
			rd.
		</descr>
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
		<descr>
			Performs a logical left shift on the register rs1 by the amount
			specified by the lower 5 bits of register rs2. The result is stored
			in register rd.
		</descr>
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
		<descr>
			Perfors a logical left shift on the register rs1 by the amount
			specified by the 12 bit immediate. The result is stored in register
			rd.
		</descr>
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
		<descr>
				Compares the values in rs1 and rs2 and stores a 1 in rd if rs1
				is less than rs2. Otherwise rd gets a 0. 
		</descr>
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
		<descr>
			Performs an unsigned compare of the values in rs1 and rs2 and
			stores a 1 in rd if rs1 is less than rs2. Otherwise rd gets a 0.
		</descr>
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
		<descr>
			Compares the value in rs1 and the value of the 12-bit sign extended
			immediate. If rs1 is less than the immediate, rd gets a 1, otherwise
			it gets a 0.
		</descr>
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
            SLTIU
        </instr>
        <syntax>
            SLTIU reg, reg, con
        </syntax>
		<descr>
			Performs an unsigned compare of the value in rs1 and the 12-bit
			sign extended immediate. If rs1 is less than the immediate, rd gets
			a 1, otherwise it gets a 0.
		</descr>
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
		<descr>
			Performs an arithmetic right shift on the register rs1 by the 
			amount specified by the lower 5 bits of rs2. The result is stored 
			in register rd.
		</descr>
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
		<descr>
			Performs an arithmetic right shift on the register rs1 by the 
			amount specified by the 12-bit immediate. The result is stored in 
			register rd.
		</descr>
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
	<descr>
		Performs a divide using register rs1 as the dividend and register rs2
		as the divisor. The result is stored in register rd. To get the
		remainder, use REM.
	</descr>
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
	<descr>
		Performs an unsigned divide using register rs1 as the dividend and
		register rs2 as the divisor. The result is stored in register rd. To
		get the remainder, use REMU.
	</descr>
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
	<descr>
		Performs a divide using register rs1 as the dividend and register rs2 
		as the divisor. The remainder of the divide is stored in register rd.
		To get the result, use DIV.
	</descr>
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
	<descr>
		Performs an unsigned divide using register rs1 as the dividend and
		register rs2 as the divisor. The remainder of the divide is stored in
		register rd. To get the result, use DIVU.
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
        Places the specified 20-bit immediate in the upper 20 bits of the
		specified register. Fills the lower 12-bits with zeroes.
    </desc>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2) = get_two_op_imm(self.get_nm(), ops, line_num)
        if op2.get_val(line_num) > 1048576:
            raise IncorrectImmLength(op2.get_val(line_num), line_num)
        op1.set_val(check_overflow(opfunc.lshift(op2.get_val(line_num),
                    12), vm), line_num)
        vm.changes.add(op1.get_nm())
