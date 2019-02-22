"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction
from .arithmetic import checkflag
from assembler.virtual_machine import intel_machine
from .fp_conversions import anyfloat,add,sub,mul,div,fabs,chs


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

    ops[0].set_val(
        checkflag(operator(ops[0].get_val(),
                           ops[1].get_val()), vm))

    vm.changes.add(ops[0].get_nm())


class FAdd(Instruction):
    """
    sets sum  of floating-point register (FPR) FRA and
    floating-point register (FPB)
    and place the results into FPR FRT
        <instr>
             FADD
        </instr>
        <syntax>
            FADD FRT, FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, add)



class FSub(Instruction):
    """
    sets sum  of floating-point register (FPR) FRA and
    floating-point register (FPB)
    and place the results into FPR FRT
        <instr>
             FSUB
        </instr>
        <syntax>
            FSUB FRT, FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, sub)


class FMul(Instruction):
    """
    sets product  of floating-point register (FPR) FRA and
    floating-point register (FPB)
    and place the results into FPR FRT
        <instr>
             FMUL
        </instr>
        <syntax>
            FMUL FRT, FRA, FRB
        </syntax>
    """
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, mul)

class FAbs(Instruction):
        """
        sets bit  of floating-point register (FPR) FRB to 0
        and place the results into FPR FRT
            <instr>
                 FABS
            </instr>
            <syntax>
                fabs FRT, FRB
            </syntax>
        """
        def fhook(self, ops, vm):
            two_op_arith(ops, vm, self.name, fabs)


class FChs(Instruction):
        """
        complements the sign of floating-point register (FPR) FRB
            <instr>
                 FCHS
            </instr>
            <syntax>
                fchs FRT
            </syntax>
        """
        def fhook(self, ops, vm):
            two_op_arith(ops, vm, self.name, chs)


class FDiv(Instruction):
    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, div)
