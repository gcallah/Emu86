from assembler.errors import check_num_args, InvalidArgument
from assembler.tokens import Instruction, NewSymbol, IntegerTok


class Global_get(Instruction):
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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], NewSymbol):
            if ops[0].get_nm() in vm.globals:
                stack_loc = hex(vm.get_sp()).split('x')[-1].upper()
                vm.stack[stack_loc] = vm.globals[ops[0].get_nm()]
                vm.inc_sp(line_num)
            else:
                raise InvalidArgument(ops[0].get_nm(), line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)


class Global_set(Instruction):
    """
        <instr>
             global.set
        </instr>
        <syntax>
            global.set var
        </syntax>
        <descr>
            Copies the value of op1 onto the stack
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], NewSymbol):
            if ops[0].get_nm() in vm.globals:
                vm.dec_sp(line_num)
                stack_loc = hex(vm.get_sp()).split('x')[-1].upper()
                vm.globals[ops[0].get_nm()] = vm.stack[stack_loc]
                vm.inc_sp(line_num)
                vm.changes.add(f'GLOBALVAR{ops[0].get_nm()}')
            else:
                raise InvalidArgument(ops[0].get_nm(), line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)


class Local_get(Instruction):
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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], NewSymbol):
            if ops[0].get_nm() in vm.locals:
                stack_loc = hex(vm.get_sp()).split('x')[-1].upper()
                vm.stack[stack_loc] = vm.locals[ops[0].get_nm()]
                vm.inc_sp(line_num)
            else:
                raise InvalidArgument(ops[0].get_nm(), line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)


class Local_set(Instruction):
    """
        <instr>
             local.set
        </instr>
        <syntax>
            local.set var
        </syntax>
        <descr>
            Copies the value of op1 onto the stack
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], NewSymbol):
            if ops[0].get_nm() in vm.locals:
                vm.dec_sp(line_num)
                stack_loc = hex(vm.get_sp()).split('x')[-1].upper()
                vm.locals[ops[0].get_nm()] = vm.stack[stack_loc]
                vm.inc_sp(line_num)
                vm.changes.add(f'LOCALVAR{ops[0].get_nm()}')
            else:
                raise InvalidArgument(ops[0].get_nm(), line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)


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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], NewSymbol):
            vm.globals[ops[0].get_nm()] = ops[0].get_val(line_num)
            vm.changes.add(f'GLOBALVAR{ops[0].get_nm()}')
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)


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
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], NewSymbol):
            vm.locals[ops[0].get_nm()] = ops[0].get_val(line_num)
            vm.changes.add(f'LOCALVAR{ops[0].get_nm()}')
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)


class Store_const(Instruction):
    """
        <instr>
             i32.const
        </instr>
        <syntax>
            i32.const val
        </syntax>
        <descr>
            Store a constant value onto the stack
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if isinstance(ops[0], IntegerTok):
            try:
                stack_loc = hex(vm.get_sp()).split('x')[-1].upper()
                vm.stack[stack_loc] = ops[0].get_val(line_num)
                vm.inc_sp(line_num)
            except Exception:
                raise InvalidArgument(ops[0].get_nm(), line_num)
        else:
            raise InvalidArgument(ops[0].get_nm(), line_num)
