"""
data_mov.py: data movement instructions.
"""
from assembler.errors import check_num_args, InvalidArgument
from assembler.tokens import Instruction, Register, RegAddress


class Global_mov(Instruction):
    """
        <instr>
             global.get
        </instr>
        <syntax>
            global.get var
        </syntax>
        <descr>
            Copies the value of op1 onto the stack
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 1)
        if isinstance(ops[0], Symbol):
            try:
                vm.dec_sp()
                m.stack[hex(vm.get_sp() + 1).split('x')[-1].upper()] = vm.globals[op[0].get_val()]
            except Error:
                raise InvalidArgument(ops[0].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())

class Local_mov(Instruction):
    """
        <instr>
             local.get
        </instr>
        <syntax>
            local.get var
        </syntax>
        <descr>
            Copies the value of op1 onto the stack
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 1)
        if isinstance(ops[0], Symbol):
            try:
                vm.dec_sp()
                m.stack[hex(vm.get_sp() + 1).split('x')[-1].upper()] = vm.local[op[0].get_val()]
            except Error:
                raise InvalidArgument(ops[0].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())