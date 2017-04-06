"""
data_mov.py: data movement instructions.
"""
from .errors import check_num_args,StackEmpty,StackFull
from .tokens import Instruction


class Mov(Instruction):
    """
        <instr>
             mov
        </instr>
        <syntax>
            MOV reg, reg
            MOV reg, con
            MOV reg, mem
            MOV mem, reg
            MOV mem, mem
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args(self.get_nm(), ops, 2)
        ops[0].set_val(ops[1].get_val())


class Pop(Instruction):
    """
        <instr>
             pop
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args("POP", ops, 1)
        if (int(gdata.registers['ESP']) == 0):
            raise StackEmpty(gdata.registers['ESP'])
        else:
            val = gdata.stack[str(int(gdata.registers['ESP'])+31)]
            ops[0].set_val(val)
            gdata.stack[str(int(gdata.registers['ESP'])+31)] = 0
            gdata.registers['ESP']=str(int(gdata.registers['ESP'])-1)
        # TBD!


class Push(Instruction):
    """
        <instr>
             push
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args("PUSH", ops, 1)
        if (int(gdata.registers['ESP']) == 32):
            raise StackFull(gdata.registers['ESP'])
        else:
            gdata.stack[str(int(gdata.registers['ESP'])+32)] = ops[0]
            gdata.registers['ESP'] =str(int(gdata.registers['ESP'])+1)
        # TBD!


class Lea(Instruction):
    """
        <instr>
             lea
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, gdata):
        check_num_args("LEA", ops, 2)
        # TBD!
