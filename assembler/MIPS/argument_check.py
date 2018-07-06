from assembler.tokens import Register, IntegerTok
from assembler.errors import InvalidArgument

def check_reg_only(instr, ops):
    for i in range(0, len(ops) - 1):
        if not isinstance(ops[i], Register):
            raise InvalidArgument(ops[i].get_nm())

def check_immediate(instr, ops):
    if not isinstance(ops[0], Register):
        raise InvalidArgument(ops[i].get_nm())
    else:
        if isinstance(ops[1], IntegerTok):
            if not isinstance(ops[2], Register):
                raise InvalidArgument(ops[2].get_nm())
        elif isinstance(ops[1], Register):
            if not isinstance(ops[2], IntegerTok):
                raise InvalidArgument(ops[2].get_nm())
        else:
            raise InvalidArgument(ops[1].get_nm())