"""
data_mov.py: data movement instructions.
"""
from assembler.errors import check_num_args
from assembler.tokens import Instruction
class Load(Instruction):
    """
        <instr>
             LW
        </instr>
        <syntax>
            LW reg, reg
            LW reg, disp(reg)
        </syntax>
        <descr>
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register) and isinstance(ops[1], RegAddress):
            ops[0].set_val(ops[1].get_val())
        else: 
            raise Exception()

class Store(Instruction):
    """
        <instr>
             SW
        </instr>
        <syntax>
            SW reg, reg
            SW reg, disp(reg)
        </syntax>
        <descr>
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], RegAddress) and isinstance(ops[1], Register):
            ops[0].set_val(ops[1].get_val())
        else: 
            raise Exception()