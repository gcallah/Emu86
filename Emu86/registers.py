"""
registers.py
Keeps track of x86 registers.
"""


class Registers():

    """
    Eight 32-bit registers, like any good, modern x86.
    """

    def __init__(self, vals=None):
        self.vals = {
                'EAX': 0,
                'EBX': 0,
                'ECX': 0,
                'EDX': 0,
                'ESI': 0,
                'EDI': 0,
                'ESP': 0,
                'EBP': 0,
                }
