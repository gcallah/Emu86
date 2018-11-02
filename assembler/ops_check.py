from assembler.errors import check_num_args


def checkFloat(ops):
    return isinstance(ops[0].get_val(),
                      float) and isinstance(ops[1].get_val(), float)


def get_one_op(instr, ops):
    check_num_args(instr, ops, 1)
    return ops[0]


def get_two_ops(instr, ops):
    check_num_args(instr, ops, 2)
    return (ops[0], ops[1])


def one_op_arith(ops, vm, instr, operator):
    """
        operator: this is the functional version of Python's
            +, -, *, etc.
    """
    check_num_args(instr, ops, 1)
    ops[0].set_val(operator(ops[0].get_val()))
    vm.changes.add(ops[0].get_nm())
