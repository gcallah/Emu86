"""
interrupts.py: data movement instructions.
"""

from assembler.errors import check_num_args, InvalidOperand
from assembler.errors import ExitProg, UnknownInt
from assembler.tokens import Instruction, IntegerTok

EAX = 'EAX'


def read_key(vm, msg=None):
    # we are faking 'reading' from the keyboard
    c = vm.ret_str[vm.nxt_key]
    vm.nxt_key = (vm.nxt_key + 1) % len(vm.ret_str)
    vm.registers[EAX] = ord(c)
    return ""


def exit_prog(vm, msg):
    raise ExitProg(msg)


int_vectors = {
    22: {0: read_key},
    32: {0: exit_prog},
}


class Interrupt(Instruction):
    """
        <instr>
             int
        </instr>
        <syntax>
            INT con
        </syntax>
        <descr>
            The behavior of INT depends on both its "con" operand
            as well as the value of the EAX register. See the descriptions
            of specific interrupt commands below.
            We will build various "interrupt" handlers as needed.
            At present, we only have two:
                INT 22, with EAX set to 0, to get a key from
            the keyboard. And we only pretend the key is from the keyboard,
            since we are running on the Internet, and can't read the user's
            keyboard.
            And INT 32, to exit the program. There should be a 0 in EAX.
        </descr>
    """

    def fhook(self, ops, vm, line_num):
        check_num_args(self.get_nm(), ops, 1, line_num)
        if type(ops[0]) != IntegerTok:
            raise InvalidOperand(str(ops[0]), line_num)
        try:
            interrupt_class = int_vectors[ops[0].get_val(line_num)]
            interrupt_handler = interrupt_class[int(vm.registers[EAX])]
        except KeyError:
            raise UnknownInt(str(ops[0].get_val(line_num)) + ": "
                             + vm.registers[EAX], line_num)
        c = interrupt_handler(vm, self.get_nm())
        return str(c)
