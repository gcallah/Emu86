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
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
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
            POPS the topmost value out of the stack.
            Decrements the stack pointer.
            Can move the stack value to a memory location or register.
        </descr>
    """
    def fhook(self, ops, vm):
        vm.inc_sp()
        check_num_args("POP", ops, 1)
        val = int(vm.stack[str(vm.get_sp())])
        ops[0].set_val(val)
        vm.stack[str(vm.get_sp())] = vm.empty_cell()

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
            pointer position (ESP). Increments the stack pointer automatically,
            everytime a PUSH is called. Callable to store a memory value,
            register value, and constant value to the stack.
        </descr>
    """
    def fhook(self, ops, vm):
        vm.dec_sp()
        check_num_args("PUSH", ops, 1)
        vm.stack[str(vm.get_sp() + 1)] = ops[0].get_val()


class Lea(Instruction):
    """
        <instr>
             lea
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, vm):
        check_num_args("LEA", ops, 2)
        # TBD!
