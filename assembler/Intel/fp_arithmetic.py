"""
fp_arithmetic.py: arithmetic floating point instructions.
"""

import operator as opfunc
from assembler.errors import check_num_args
from assembler.tokens import Instruction
from .arithmetic import checkflag
from assembler.virtual_machine import intel_machine
from .fp_conversions import anyfloat,add


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
        intel_machine.registers["FRT"] = add(intel_machine.registers["FRB"],intel_machine.registers["FRA"])
        print("SOLVED ", intel_machine.registers["FRT"])


class FMul(Instruction):

    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.mul)


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
            IEEE = anyfloat.from_float(intel_machine.registers["FRB"])
            """IEEE representation of floating point instruction"""
            IEEE.abs_sign()
            intel_machine.registers["FRT"] = float(IEEE)


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
            IEEE = anyfloat.from_float(intel_machine.registers["FRB"])
            """IEEE representation of floating point instruction"""
            IEEE.change_sign()
            intel_machine.registers["FRB"] = float(IEEE)


class FDiv(Instruction):
    def fhook(self, ops, vm):
        return
