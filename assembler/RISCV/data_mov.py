"""
data_mov.py: data movement instructions.
"""
from assembler.errors import check_num_args, InvalidArgument
from assembler.tokens import Instruction, Register, RegAddress


class Load(Instruction):
    """
        <instr>
            LW
        </instr>
        <syntax>
            LW rd, imm(rs1)
        </syntax>
        <descr>
            Load value from memory into rd.
            R[rd] = M_4B[ R[rs1] + sext(imm) ]
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register):
            if isinstance(ops[1], RegAddress):
                ops[0].set_val(ops[1].get_val())
                vm.changes.add(ops[0].get_nm())
            else:
                raise InvalidArgument(ops[1].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())


class Store(Instruction):
    """
        <instr>
            SW
        </instr>
        <syntax>
            SW rs2, imm(rs1)
        </syntax>
        <descr>
            Store the value in rs2 into memory.
            M_4B[ R[rs1] + sext(imm) ] = R[rs2]
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register):
            if isinstance(ops[1], RegAddress):
                ops[1].set_val(ops[0].get_val())
            else:
                InvalidArgument(ops[1].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())
