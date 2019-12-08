"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

"""

from assembler.errors import check_num_args, InvalidArgument, OutofBounds
from assembler.tokens import Instruction, Register, IntegerTok
from assembler.flowbreak import Jump
from assembler.ops_check import get_one_op
from .argument_check import check_reg_only, check_immediate_three


def get_three_ops(instr, ops, line_num):
    check_num_args(instr, ops, 3, line_num)
    check_reg_only(instr, ops, line_num)
    return (ops[0], ops[1], ops[2])


def get_three_ops_imm(instr, ops, line_num):
    check_num_args(instr, ops, 3, line_num)
    check_immediate_three(instr, ops, line_num)
    return (ops[0], ops[1], ops[2])


class Slt(Instruction):
    """
        <instr>
             slt
        </instr>
        <syntax>
            SLT reg, reg, reg
        </syntax>
        <descr>
            Compares op2 and op3, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
            Store the result of SF flag into op1
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops(self.get_nm(), ops, line_num)
        res = op2.get_val(line_num) - op3.get_val(line_num)
        if res < 0:
            op1.set_val(1, line_num)
        else:
            op1.set_val(0, line_num)
        vm.changes.add(op1.get_nm())


class Slti(Instruction):
    """
        <instr>
             slti
        </instr>
        <syntax>
            SLTI reg, con, reg
            SLTI reg, reg, con
        </syntax>
        <descr>
            Compares op2 and op3, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
            Store the result of SF flag into op1
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2, op3) = get_three_ops_imm(self.get_nm(), ops, line_num)
        res = op2.get_val(line_num) - op3.get_val(line_num)
        if res < 0:
            op1.set_val(1, line_num)
        else:
            op1.set_val(0, line_num)
        vm.changes.add(op1.get_nm())


class Jmp(Instruction):
    """
        <instr>
            J
        </instr>
        <syntax>
            J lbl
            J loc
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if isinstance(target, IntegerTok):
            raise Jump(str(target.get_val(line_num)))
        else:
            raise Jump(target.name)


class Jal(Instruction):
    """
        <instr>
            JAL
        </instr>
        <syntax>
            JAL loc
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        raise Jump(str(target.get_val(line_num)))


class Jr(Instruction):
    """
        <instr>
            Jr
        </instr>
        <syntax>
            Jr reg
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        raise Jump(str(target.get_val(line_num)))


class Beq(Instruction):
    """
        <instr>
             BEQ
        </instr>
        <syntax>
            BEQ reg, reg, con
        </syntax>
        <descr>
            Jumps if registers are equal.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args("BEQ", ops, 3, line_num)
        disp = 0
        if isinstance(ops[2], IntegerTok):
            disp = ops[2].get_val(line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)
        val_one, val_two = (0, 0)
        if isinstance(ops[0], Register):
            val_one = ops[0].get_val(line_num)
            if isinstance(ops[1], Register):
                val_two = ops[1].get_val(line_num)
            else:
                InvalidArgument(ops[1].get_nm(), line_num)
        else:
            InvalidArgument(ops[0].get_nm(), line_num)
        if val_one == val_two:
            current_ip = vm.get_ip()
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds(line_num)


class Bne(Instruction):
    """
        <instr>
             BNE
        </instr>
        <syntax>
            BNE reg, reg, con
        </syntax>
        <descr>
            Jumps if registers are equal.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args("BNE", ops, 3, line_num)
        disp = 0
        if isinstance(ops[2], IntegerTok):
            disp = ops[2].get_val(line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)
        val_one, val_two = (0, 0)
        if isinstance(ops[0], Register):
            val_one = ops[0].get_val(line_num)
            if isinstance(ops[1], Register):
                val_two = ops[1].get_val(line_num)
            else:
                InvalidArgument(ops[1].get_nm(), line_num)
        else:
            InvalidArgument(ops[0].get_nm(), line_num)
        if val_one != val_two:
            current_ip = vm.get_ip()
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds(line_num)
