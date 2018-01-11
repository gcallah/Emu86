"""
interrupts.py: data movement instructions.
"""

from .errors import check_num_args, InvalidOperand, ExitProg, UnknownInt
from .tokens import Instruction, IntOp

EAX = 'EAX'

def read_key(vm):
    # we are faking 'reading' from the keyboard
    c = vm.ret_str[vm.nxt_key]
    vm.nxt_key = (vm.nxt_key + 1) % len(vm.ret_str)
    vm.registers[EAX] = ord(c)
    return ""

def exit_prog(vm):
    raise ExitProg()


int_vectors = {
    22: {0: read_key },
    33: {0: exit_prog },
}


class Interrupt(Instruction):
    """
        <instr>
             int
        </instr>
        <syntax>
            INT con, con
        </syntax>
        <descr>
            We will build various "interrupt" handlers as needed.
            At present, we only have two:
                INT 22, 0, to get a key from
            the keyboard. And we only pretend the key is from the keyboard,
            since we are running on the Internet, and can't read the user's
            keyboard.
            <br />
            And INT 33, 0, to exit the program.
        </descr>
    """

    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 1)
        if type(ops[0]) != IntOp:
            raise InvalidOperand(str(ops[0]))
        interrupt_class = int_vectors[ops[0].get_val()]
        interrupt_handler = interrupt_class[int(vm.registers[EAX])]
        c = interrupt_handler(vm)
        return str(c)
