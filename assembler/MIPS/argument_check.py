from assembler.tokens import Register, IntegerTok, Symbol
from assembler.errors import InvalidArgument


def check_reg_only(instr, ops):
    for i in range(0, len(ops)):
        if not isinstance(ops[i], Register):
            raise InvalidArgument(ops[i].get_nm())


def check_immediate_three(instr, ops):
    if not isinstance(ops[0], Register):
        raise InvalidArgument(ops[0].get_nm())
    else:
        if isinstance(ops[1], Register):
            if (not isinstance(ops[2], IntegerTok) and
                    not isinstance(ops[2], Symbol)):
                raise InvalidArgument(ops[2].get_nm())
        else:
            raise InvalidArgument(ops[1].get_nm())


def check_immediate_two(instr, ops):
    if isinstance(ops[0], Register):
        if not isinstance(ops[1], IntegerTok):
            raise InvalidArgument(ops[1].get_nm())
    else:
        raise InvalidArgument(ops[0].get_nm())
