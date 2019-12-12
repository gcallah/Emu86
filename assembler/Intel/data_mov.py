"""
data_mov.py: data movement instructions.
"""
from assembler.errors import check_num_args, StackFull
from assembler.tokens import Instruction, Register, Address


class Fld(Instruction):
    """
        <instr>
             fld
        </instr>
        <syntax>
            fld con
        </syntax>
        <descr>
            loads value onto stack
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if vm.is_FP_stack_full():
            raise StackFull(line_num)
        # if isinstance(ops[0], FloatTok):
        #     vm.push_to_Float_Stack(ops[0].get_val(line_num))
        vm.push_to_Float_Stack(ops[0].get_val(line_num))


class Fst(Instruction):
    """
        <instr>
             fst
        </instr>
        <syntax>
            fst con
        </syntax>
        <descr>
            stores value from top of stack
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if vm.is_FP_stack_full():
            raise StackFull(line_num)
        ops[0].set_val(vm.registers['ST0'], line_num)


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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 2, line_num)
        ops[0].set_val(ops[1].get_val(line_num), line_num)
        if isinstance(ops[0], Register):
            vm.changes.add(ops[0].get_nm())
        elif isinstance(ops[0], Address):
            vm.changes.add(f'MEM{ops[0].get_mem_addr(line_num)}')


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
    def fhook(self, ops, vm, line_num):
        vm.inc_sp(line_num)
        check_num_args("POP", ops, 1, line_num)
        val = int(vm.stack[hex(vm.get_sp()).split('x')[-1].upper()])
        ops[0].set_val(val, line_num)
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = vm.empty_cell()


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
    def fhook(self, ops, vm, line_num):
        vm.dec_sp(line_num)
        check_num_args("PUSH", ops, 1, line_num)
        vm.stack[hex(vm.get_sp() +
                     1).split('x')[-1].upper()] = ops[0].get_val(line_num)


class Lea(Instruction):
    """
        <instr>
             lea
        </instr>
        <syntax>
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args("LEA", ops, 2, line_num)
        # TBD!
