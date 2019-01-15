"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction
from assembler.ops_check import checkFloat
from assembler.ops_check import one_op_arith
from assembler.virtual_machine import intel_machine, STACK_TOP, STACK_BOTTOM
from .arithmetic import checkflag
from ctypes import *
from .fp_conversions import anyfloat

def dec_convert(val):
    while val > 1:
        val = val / 10
    return val


def two_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 2)
    if checkFloat:
        ops[0].set_val(
            checkflag(operator(ops[0].get_val(),
                               ops[1].get_val()), vm))
        vm.changes.add(ops[0].get_nm())


class FAdd(Instruction):
    """
        <instr>
             add
        </instr>
        <syntax>
            FADD reg, reg
            FADD reg, mem
            FADD reg, const
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.add)


class FSub(Instruction):
    def fhook(self, ops, vm):
        one_op_arith(ops, vm, self.name, opfunc.sub)


class FMul(Instruction):


    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.mul)


class FDec(Instruction):
    def fhook(self, ops, vm):
        check_num_args(self.name, ops, 1)
        ops[0].set_val(ops[0].get_val() - 1)
        vm.changes.add(ops[0].get_nm())

class FAbs(Instruction):
        """
        sets bit  of floating-point register (FPR) FRB to 0 and place the results into FPR FRT
            <instr>
                 test_fabs
            </instr>
            <syntax>
                fabs FRT, FRB
            </syntax>
        """
        def fhook(self, ops, vm):
            IEEE = anyfloat.from_float(intel_machine.registers["FRB"]) #IEEE representation of floating point instruction
            IEEE.abs_sign()
            intel_machine.registers["FRT"]=float(IEEE)
class FChs(Instruction):
        """
        complements the sign of floating-point register (FPR) FRB
            <instr>
                 test_fchs
            </instr>
            <syntax>
                fchs FRT
            </syntax>
        """
        def fhook(self, ops, vm):
            IEEE = anyfloat.from_float(intel_machine.registers["FRB"]) #IEEE representation of floating point instruction
            IEEE.change_sign()
            intel_machine.registers["FRB"]=float(IEEE)
class FDiv(Instruction):
    def fhook(self, ops, vm):
        return
