from assembler.errors import check_num_args


def checkFloat(ops, line_num):
    return isinstance(ops[0].get_val(line_num),
                      float) and isinstance(ops[1].get_val(line_num), float)


def get_one_op(instr, ops, line_num):
    check_num_args(instr, ops, 1, line_num)
    return ops[0]


def get_two_ops(instr, ops, line_num):
    check_num_args(instr, ops, 2, line_num)
    return (ops[0], ops[1])


def one_op_arith(ops, vm, instr, line_num, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1, line_num)
    ops[0].set_val(operator(ops[0].get_val(line_num)), line_num)
    vm.changes.add(ops[0].get_nm())
