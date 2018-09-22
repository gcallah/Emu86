"""
fp_arithmetic.py: arithmetic and logic instructions.
"""

import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT, Register, IntegerTok
from assembler.ops_check import one_op_arith
from .argument_check import * 

#'ADD.S': Adds('ADD.S'),
class Adds(Instruction):
    """
        <instr>
             ADD.S
        </instr>
        <syntax>
            ADD.S reg, reg, reg
        </syntax>
    """
    # ops is a list of operands (reg, reg, reg)
    def fhook(self, ops, vm):
        # three_op_arith_reg(ops, vm, self.name, opfunc.add)
        operator = opfunc.add
        check_num_args(instr, ops, 3)
        check_reg_only(instr, ops)
        ops[0].set_val(
        check_overflow(operator(ops[1].get_val(),
                           ops[2].get_val()), 
                           vm)) 
        # vm.changes is for the website stuff
        # vm.changes.add(ops[0].get_nm())

#'SUB.S': Subs('SUB.S'),
#'MULT.S': Mults('MULT.S'),
#'DIV.S': Divs('DIV.S'),