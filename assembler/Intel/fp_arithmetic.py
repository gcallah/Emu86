"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT
from assembler.ops_check import one_op_arith,checkFloat
def two_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    if checkFloat:
        ops[0].set_val(
            checkflag(operator(ops[0].get_val(),
                               ops[1].get_val()),
                               vm))
        vm.changes.add(ops[0].get_nm())

class FADD(Instruction):
        """
            <instr>
                 add
            </instr>
            <syntax>
                ADD reg, reg
                ADD reg, mem
                ADD reg, const
            </syntax>
        """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.add)
class FSUB(Instruction):

    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.sub)
class FMUL(Instruction):
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.mul)


class FDIV(Instruction):

    def fhook(self, ops, vm):
        return
        # check_num_args(self.name, ops, 1)
        #
        # hireg = int(vm.registers['EDX']) << 32
        # lowreg = int(vm.registers['EAX'])
        # dividend = hireg + lowreg
        # if ops[0].get_val() == 0:
        #     raise DivisionZero()
        # vm.registers['EAX'] = dividend // ops[0].get_val()
        # vm.registers['EDX'] = dividend % ops[0].get_val()
        # vm.changes.add('EAX')
        # vm.changes.add('EDX')
        # return ''
