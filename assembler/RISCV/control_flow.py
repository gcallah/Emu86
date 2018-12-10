"""
control_flow.py: control flow instructions,

"""

from assembler.errors import check_num_args, OutofBounds, InvalidArgument
from assembler.tokens import Instruction, Register, IntegerTok
from assembler.flowbreak import Jump
from assembler.ops_check import get_one_op, get_two_ops


class Jr(Instruction):
    """
        <instr>
            JR
        </instr>
        <syntax>
            JR reg
        </syntax>
        <descr>
            Jump to address.
            PC = R[rs1]
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        raise Jump(str(target.get_val()))


class Jal(Instruction):
    """
        <instr>
            JAL
        </instr>
        <syntax>
            JAL rd, imm
        </syntax>
        <descr>
            Jump to address and place return address in GPR.
            R[rd] = PC + 4; PC = PC + sext(imm)
        </descr>
    """
    def fhook(self, ops, vm):
        current_ip = vm.get_ip()
        target = current_ip + ops[1]
        ops[0].set_val(current_ip + 4)
        vm.changes.add(ops[0].get_nm())
        raise Jump(str(target.get_val()))
# The original implementation of JAL was pretty off. 
# I've corrected it, but it needs to be tested some more. 

class Jalr(Instruction):
    """
        <instr>
            JALR
        </instr>
        <syntax>
            JALR rd, rs1, imm
        </syntax>
        <descr>
            Jump to address and place return address in GPR
            R[rd] = PC + 4; PC = ( R[rs1] + sext(imm) ) & 0xfffffffe
        </descr>
    """
    def fhook(self, ops, vm):
        target = get_one_op(self.get_nm(), ops)
        raise Jump(str(target.get_val()))


class Beq(Instruction):
    """
        <instr>
            BEQ
        </instr>
        <syntax>
            BEQ rs1, rs2, imm
        </syntax>
        <descr>
            Branch if 2 GPRs are equal.
            PC = ( R[rs1] == R[rs2] ) ? PC + sext(imm) : PC + 4
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("BEQ", ops, 3)
        disp = 0
        if isinstance(ops[2], IntegerTok):
            disp = ops[2].get_val()
        else:
            raise InvalidArgument(ops[0].get_nm())
        val_one, val_two = (0, 0)
        if isinstance(ops[0], Register):
            val_one = ops[0].get_val()
            if isinstance(ops[1], Register):
                val_two = ops[1].get_val()
            else:
                InvalidArgument(ops[1].get_nm())
        else:
            InvalidArgument(ops[0].get_nm())
        if val_one == val_two:
            current_ip = vm.get_ip()
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds()


class Bne(Instruction):
    """
        <instr>
            BNE
        </instr>
        <syntax>
            BNE rs1, rs2, imm
        </syntax>
        <descr>
            Branch if 2 GPRs are not equal.
            PC = ( R[rs1] != R[rs2] ) ? PC + sext(imm) : PC + 4
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("BNE", ops, 3)
        disp = 0
        if isinstance(ops[2], IntegerTok):
            disp = ops[2].get_val()
        else:
            raise InvalidArgument(ops[0].get_nm())
        val_one, val_two = (0, 0)
        if isinstance(ops[0], Register):
            val_one = ops[0].get_val()
            if isinstance(ops[1], Register):
                val_two = ops[1].get_val()
            else:
                InvalidArgument(ops[1].get_nm())
        else:
            InvalidArgument(ops[0].get_nm())
        if val_one != val_two:
            current_ip = vm.get_ip()
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds()


class Blt(Instruction):
    """
        <instr>
            BLT
        </instr>
        <syntax>
            BLT rs1, rs2, imm
        </syntax>
        <descr>
            Branch based on signed comparison of two GPRs
            PC = ( R[rs1] <s R[rs2] ) ? PC + sext(imm) : PC + 4
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args("BNE", ops, 3)
        disp = 0
        if isinstance(ops[2], IntegerTok):
            disp = ops[2].get_val()
        else:
            raise InvalidArgument(ops[0].get_nm())
        val_one, val_two = (0, 0)

        if isinstance(ops[0], Register):
            val_one = ops[0].get_val()
            if isinstance(ops[1], Register):
                val_two = ops[1].get_val()
            else:
                InvalidArgument(ops[1].get_nm())
        else:
            InvalidArgument(ops[0].get_nm())

        if val_one < val_two:
            current_ip = vm.get_ip()
            if current_ip + disp * 4 >= 0:
                vm.set_ip(current_ip + disp * 4)
            else:
                raise OutofBounds()
