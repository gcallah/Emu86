"""
data_mov.py: data movement instructions.
"""

from .errors import check_num_args
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
        <descr>
            Stores/Copies the value of op2 in op1. Callable for registers, 
            memory values and constants.
        </descr>
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
            POP reg
            POP mem
        </syntax>
        <descr>
            POPS the topmost value out of the stack with reference to 
            the stack pointer position (ESP). Decrements the stack pointer 
            automatically. Callable to store the stack value to a memory 
            location and register.
        </descr>
    """
    def fhook(self, ops, gdata):
        check_num_args("POP", ops, 1)
        gdata.inc_sp()
        val = gdata.stack[str(gdata.get_sp())]
        ops[0].set_val(val)
        gdata.stack[str(gdata.get_sp())] = gdata.empty_cell()


class Push(Instruction):
    """
        <instr>
             push
        </instr>
        <syntax>
            PUSH reg
            PUSH con
            PUSH mem
        </syntax>
        <descr>
            PUSHES the value into the stack with reference to the stack 
            pointer position (ESP). Increments the stack pointer automatically. 
            Callable to store a memory value, register value, and constant 
            value to the stack.
        </descr>
    """
    def fhook(self, ops, gdata):
        check_num_args("PUSH", ops, 1)
        gdata.stack[str(gdata.get_sp())] = ops[0]
        gdata.dec_sp()


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
