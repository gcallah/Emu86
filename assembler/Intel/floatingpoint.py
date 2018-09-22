import operator as opfunc

from assembler.errors import *
from assembler.tokens import Instruction, MAX_INT
from assembler.ops_check import one_op_arith

class Add(Instruction):

    def fhook(self, ops, vm):
        two_op_arith(ops, vm, self.name, opfunc.add)
