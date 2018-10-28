"""
control_flow.py: control flow instructions,

"""

from assembler.errors import check_num_args, OutofBounds
from assembler.tokens import Instruction, Register, IntegerTok
from assembler.flowbreak import Jump
from assembler.ops_check import get_one_op, get_two_ops
from .argument_check import check_reg_only, check_immediate_three

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
        target = get_one_op(self.get_nm(), ops)
        raise Jump(str(target.get_val()))

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
