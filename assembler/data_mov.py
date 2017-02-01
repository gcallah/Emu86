"""
data_mov.py: data movement instructions.
"""

def mov(ops, gdata):
    """
    Implments the MOV instruction.
    """
    if len(ops) != 2:
        raise(InvalidNumArgs("MOV"))
    ops[0].set_val(ops[1].get_val())
    return ''
