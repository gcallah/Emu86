"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

Contains:
    JMP

    FlowBreak
    Jmp
"""

from .parse import get_one_op


class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Uknown control flow exception."


class Jmp(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


def jmp(code, registers, memory, code_pos):
    """
    Implments the MOV instruction.
    """
    (target, code_pos) = get_one_op("JMP", code, registers, memory, code_pos)
    raise Jmp(target.name)

