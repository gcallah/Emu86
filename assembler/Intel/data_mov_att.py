"""
data_mov_att.py: other data movement instructions for AT&T
"""

from assembler.errors import check_num_args, InvalidConVal, InvalidArgument
from assembler.tokens import Instruction, IntegerTok, Register, Address, RegAddress
from assembler.virtual_machine import STACK_TOP, STACK_BOTTOM


def check_source_val(instr, ops, data_type, line_num):
    """
    Checks if the constant value matches the transfer size

    Args:
        instr: Instruction name
        ops: Operand list
        data_type: Transfer size
                   'b': byte
                   'w': word
                   'l': long

    Raises an Invalid Constant Value error if mismatch found
    """
    if (not isinstance(ops[1], IntegerTok) and not isinstance(ops[1], Register)
            and not isinstance(ops[1], Address)):
        raise InvalidArgument("Invalid data", line_num)
    val = ops[1].get_val(line_num)
    if data_type == "b":
        if (val >= 2 ** 8 or val <= -(2 ** 8)):
            raise InvalidConVal(str(val), line_num)
    elif data_type == "w":
        if (val >= 2 ** 16 or
                ops[1].get_val(line_num) <= -(2 ** 16)):
            raise InvalidConVal(str(ops[1].get_val(line_num)), line_num)
    else:
        if (ops[1].get_val(line_num) >= 2 ** 32 or
                ops[1].get_val(line_num) <= -(2 ** 32)):
            raise InvalidConVal(str(ops[1].get_val(line_num)), line_num)


class Movb(Instruction):
    """
        <instr>
             movb
        </instr>
        <syntax>
            MOVB con, mem
        </syntax>
        <descr>
            Copies the value of op1 to the location mentioned in op2.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 2, line_num)
        check_source_val(self.get_nm(), ops, 'b', line_num)
        stackarg = 0
        val = 1
        haveaddressarg = False
        instack = False
        if(isinstance(ops[0], Address) or isinstance(ops[0], RegAddress)):
            haveaddressarg = True
        if(isinstance(ops[1], Address) or isinstance(ops[1], RegAddress)):
            stackarg = 1
            val = 0
            haveaddressarg = True
        if(haveaddressarg):
            stack = int(ops[stackarg].get_mem_addr(line_num), 16)
            stack_loc = hex(stack).split('x')[-1].upper()
            instack = (stack < (STACK_TOP + 1) and stack >= STACK_BOTTOM)
        if(stackarg == 0 and instack):
            vm.stack[stack_loc] = ops[val].get_val(line_num)
        elif(stackarg == 1 and instack):
            ops[val].set_val(vm.stack[stack_loc], line_num)
        else:
            ops[0].set_val(ops[1].get_val(line_num), line_num)
        if isinstance(ops[0], Register):
            vm.changes.add(ops[0].get_nm())
        elif isinstance(ops[0], Address):
            vm.changes.add(f'MEM{ops[0].get_mem_addr(line_num)}')


class Movw(Instruction):
    """
        <instr>
             movw
        </instr>
        <syntax>
            MOVW con, mem
        </syntax>
        <descr>
            Copies the value of op1 to the location mentioned in op2.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 2, line_num)
        check_source_val(self.get_nm(), ops, 'w', line_num)
        stackarg = 0
        val = 1
        haveaddressarg = False
        instack = False
        if(isinstance(ops[0], Address) or isinstance(ops[0], RegAddress)):
            haveaddressarg = True
        if(isinstance(ops[1], Address) or isinstance(ops[1], RegAddress)):
            stackarg = 1
            val = 0
            haveaddressarg = True
        if(haveaddressarg):
            stack = int(ops[stackarg].get_mem_addr(line_num), 16)
            stack_loc = hex(stack).split('x')[-1].upper()
            instack = (stack < (STACK_TOP + 1) and stack >= STACK_BOTTOM)
        if(stackarg == 0 and instack):
            vm.stack[stack_loc] = ops[val].get_val(line_num)
        elif(stackarg == 1 and instack):
            ops[val].set_val(vm.stack[stack_loc], line_num)
        else:
            ops[0].set_val(ops[1].get_val(line_num), line_num)
        if isinstance(ops[0], Register):
            vm.changes.add(ops[0].get_nm())
        elif isinstance(ops[0], Address):
            vm.changes.add(f'MEM{ops[0].get_mem_addr(line_num)}')


class Movl(Instruction):
    """
        <instr>
             movl
        </instr>
        <syntax>
            MOVL con, mem
        </syntax>
        <descr>
            Copies the value of op1 to the location mentioned in op2.
        </descr>
    """
    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 2, line_num)
        check_source_val(self.get_nm(), ops, 'l', line_num)
        stackarg = 0
        val = 1
        haveaddressarg = False
        instack = False
        if(isinstance(ops[0], Address) or isinstance(ops[0], RegAddress)):
            haveaddressarg = True
        if(isinstance(ops[1], Address) or isinstance(ops[1], RegAddress)):
            stackarg = 1
            val = 0
            haveaddressarg = True
        if(haveaddressarg):
            stack = int(ops[stackarg].get_mem_addr(line_num), 16)
            stack_loc = hex(stack).split('x')[-1].upper()
            instack = (stack < (STACK_TOP + 1) and stack >= STACK_BOTTOM)
        if(stackarg == 0 and instack):
            vm.stack[stack_loc] = ops[val].get_val(line_num)
        elif(stackarg == 1 and instack):
            ops[val].set_val(vm.stack[stack_loc], line_num)
        else:
            ops[0].set_val(ops[1].get_val(line_num), line_num)
        if isinstance(ops[0], Register):
            vm.changes.add(ops[0].get_nm())
        elif isinstance(ops[0], Address):
            vm.changes.add(f'MEM{ops[0].get_mem_addr(line_num)}')
