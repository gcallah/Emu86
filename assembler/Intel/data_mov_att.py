"""
data_mov_att.py: other data movement instructions for AT&T
"""

from assembler.errors import check_num_args, InvalidConVal
from assembler.tokens import Instruction, IntegerTok


def check_constant_val(instr, ops, data_type, line_num):
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
    if not isinstance(ops[1], IntegerTok):
        raise InvalidConVal(ops[1].get_nm(), line_num)
    else:
        if data_type == "b":
            if (ops[1].get_val(line_num) >= 2 ** 8 or
                    ops[1].get_val(line_num) <= -(2 ** 8)):
                raise InvalidConVal(str(ops[1].get_val(line_num)), line_num)
        elif data_type == "w":
            if (ops[1].get_val(line_num) >= 2 ** 16 or
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
        check_constant_val(self.get_nm(), ops, 'b', line_num)
        ops[0].set_val(ops[1].get_val(line_num), line_num)


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
        check_constant_val(self.get_nm(), ops, 'w', line_num)
        ops[0].set_val(ops[1].get_val(line_num), line_num)


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
        check_constant_val(self.get_nm(), ops, 'l', line_num)
        ops[0].set_val(ops[1].get_val(line_num), line_num)
