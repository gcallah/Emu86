"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

"""

from assembler.errors import check_num_args
from assembler.tokens import Instruction
from assembler.flowbreak import Jump
from assembler.ops_check import get_one_op, get_two_ops


class Cmpf(Instruction):
    """
        <instr>
             cmp
        </instr>
        <syntax>
            CMP reg, reg
            CMP reg, mem
            CMP reg, con
        </syntax>
        <descr>
            Compares op1 and op2, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        (op1, op2) = get_two_ops(self.get_nm(), ops, line_num)
        res = op1.get_val(line_num) - op2.get_val(line_num)
        # set the proper flags
        # zero flag:
        if res == 0:
            vm.flags['ZF'] = 1
        else:
            vm.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            vm.flags['SF'] = 1
        else:
            vm.flags['SF'] = 0
        vm.changes.add('FLAGZF')
        vm.changes.add('FLAGSF')


class Jmp(Instruction):
    """
        <instr>
            jmp
        </instr>
        <syntax>
            JMP lbl
        </syntax>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        raise Jump(target.name)


class Je(Instruction):
    """
        <instr>
             je
        </instr>
        <syntax>
            JE lbl
        </syntax>
        <descr>
            Jumps if ZF is one. <br>
            Equivalent name: JZ
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if int(vm.flags['ZF']) == 1:
            raise Jump(target.name)


class Jne(Instruction):
    """
        <instr>
             jne
        </instr>
        <syntax>
            JNE lbl
        </syntax>
        <descr>
            Jumps if ZF is zero. <br>
            Equivalent name: JNZ
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if int(vm.flags['ZF']) == 0:
            raise Jump(target.name)


class Jg(Instruction):
    """
        <instr>
             jg
        </instr>
        <syntax>
            JG lbl
        </syntax>
        <descr>
            Jumps if SF == 0 and ZF == 0. <br>
            Equivalent name: JLNE
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if (int(vm.flags['SF']) == 0 and
                int(vm.flags['ZF']) == 0):
            raise Jump(target.name)


class Jge(Instruction):
    """
        <instr>
             jge
        </instr>
        <syntax>
            JGE lbl
        </syntax>
        <descr>
            Jumps if SF == 0.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if int(vm.flags['SF']) == 0:
            raise Jump(target.name)
        return ''


class Jl(Instruction):
    """
        <instr>
             jl
        </instr>
        <syntax>
            JL lbl
        </syntax>
        <descr>
            Jumps if SF == 1. <br>
            Equivalent name: JGNE
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if int(vm.flags['SF']) == 1:
            raise Jump(target.name)
        return ''


class Jle(Instruction):
    """
        <instr>
             jle
        </instr>
        <syntax>
            JLE lbl
        </syntax>
        <descr>
            Jumps if SF == 1 or ZF == 1.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        target = get_one_op(self.get_nm(), ops, line_num)
        if (int(vm.flags['SF']) == 1 or
                int(vm.flags['ZF']) == 1):
            raise Jump(target.name)
        return ''


class Call(Instruction):
    """
        <instr>
             call
        </instr>
        <syntax>
            CALL lbl
        </syntax>
        <descr>
            Pushes value of EIP to stack and jumps to the internal subroutine.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args("CALL", ops, 1, line_num)
        vm.dec_sp(line_num)
        vm.stack[hex(vm.get_sp() + 1).split('x')[-1].upper()] = vm.get_ip()
        target = get_one_op(self.get_nm(), ops, line_num)
        vm.c_stack.append(vm.get_ip())
        raise Jump(target.name)


class Ret(Instruction):
    """
        <instr>
             ret
        </instr>
        <syntax>
            RET
        </syntax>
        <descr>
            Pops value from stack to EIP and returns control to the
            the line after the subroutine call.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args("RET", ops, 0, line_num)
        vm.inc_sp(line_num)
        vm.set_ip(int(vm.stack[hex(vm.get_sp()).split('x')[-1].upper()]))
        vm.stack[hex(vm.get_sp()).split('x')[-1].upper()] = vm.empty_cell()
        while not isinstance(vm.c_stack[-1], int):
            vm.c_stack.pop()
        if isinstance(vm.c_stack[-1], int):
            vm.c_stack.pop()
