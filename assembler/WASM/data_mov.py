from assembler.errors import check_num_args, InvalidArgument
from assembler.tokens import Instruction, Symbol


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
                stack_loc = hex(vm.get_sp() + 1).split('x')[-1].upper()
                vm.stack[stack_loc] = vm.globals[ops[0].get_nm()].get_val()
            except Exception:
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
                stack_loc = hex(vm.get_sp() + 1).split('x')[-1].upper()
                vm.stack[stack_loc] = vm.local[ops[0].get_nm()].get_val()
            except Exception:
                raise InvalidArgument(ops[0].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())


class Store_global(Instruction):
    """
        <instr>
             global
        </instr>
        <syntax>
            global var
        </syntax>
        <descr>
            Store a global value into the globals dictionary
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 1)
        if isinstance(ops[0], Symbol):
            try:
                vm.globals[ops[0].get_nm()] = ops[0]
            except Exception:
                raise InvalidArgument(ops[0].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())


class Store_local(Instruction):
    """
        <instr>
             local
        </instr>
        <syntax>
            local var
        </syntax>
        <descr>
            Store a local value into the locals dictionary
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 1)
        if isinstance(ops[0], Symbol):
            try:
                vm.locals[ops[0].get_nm()] = ops[0]
            except Exception:
                raise InvalidArgument(ops[0].get_nm())
        else:
            raise InvalidArgument(ops[0].get_nm())
