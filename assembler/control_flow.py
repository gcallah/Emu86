"""
control_flow.py: control flow instructions,
    plus Exceptions to signal break in flow.

"""

from .errors import check_num_args
from .tokens import Instruction



class FlowBreak(Exception):
    """
    Base class for all of our flow break exceptions.
    """
    def __init__(self, label):
        super().__init__("Flow break")
        self.label = label
        self.msg = "Unknown control flow exception."

def get_one_op(instr, ops):
    check_num_args(instr, ops, 1)
    return ops[0]

def get_two_ops(instr, ops):
    check_num_args(instr, ops, 2)
    return (ops[0], ops[1])

class Jump(FlowBreak):
    def __init__(self, label):
        super().__init__(label)
        self.msg = "Jump to " + label


class Cmpf(Instruction):
    """
        <instr>
             cmp
        </instr>
        <syntax>
            CMP reg, reg
            CMP reg, mem
            CMP reg, con
        </syntax>
        <descr>
            Compares op1 and op2, and sets (right now) the SF and ZF flags.
            It is not clear at this moment how to 
            treat the OF and CF flags in Python,
            since Python integer arithmetic never carries or overflows!
        </descr>
    """
    def fhook(self, ops, gdata):
        (op1, op2) = get_two_ops(self.get_nm(), ops)
        res = op1.get_val() - op2.get_val()
        # set the proper flags
        # zero flag:
        if res == 0:
            gdata.flags['ZF'] = 1
        else:
            gdata.flags['ZF'] = 0
        # sign flag:
        if res < 0:
            gdata.flags['SF'] = 1
        else:
            gdata.flags['SF'] = 0

class Jmp(Instruction):
    """
        <instr>
            jmp
        </instr>
        <syntax>
            JMP lbl
        </syntax>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Je(Instruction):
    """
        <instr>
             je
        </instr>
        <syntax>
            JE lbl
        </syntax>
        <descr>
            Jumps if ZF is one.
        </descr>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        gdata.debug += ("In JE; ZF = " + str(gdata.flags['ZF']) + "\n")
        if int(gdata.flags['ZF']) == 1:
            gdata.debug += ("About to raise Jump; ZF = " 
                            + str(gdata.flags['ZF']) + "\n")
            raise Jump(target.name)

class Jne(Instruction):
    """
        <instr>
             jne
        </instr>
        <syntax>
            JNE lbl
        </syntax>
        <descr>
            Jumps if ZF is zero.
        </descr>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if int(gdata.flags['ZF']) == 0:
            raise Jump(target.name)

class Jg(Instruction):
    """
        <instr>
             jg
        </instr>
        <syntax>
            JG lbl
        </syntax>
        <descr>
            Jumps if SF == 0 and ZF == 0.
        </descr>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if (int(gdata.flags['SF']) == 0 
            and int(gdata.flags['ZF']) == 0):
            raise Jump(target.name)

class Jge(Instruction):
    """
        <instr>
             jge
        </instr>
        <syntax>
            JGE lbl
        </syntax>
        <descr>
            Jumps if SF == 0.
        </descr>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if int(gdata.flags['SF']) == 0:
            raise Jump(target.name)
        return ''

class Jl(Instruction):
    """
        <instr>
             jl
        </instr>
        <syntax>
            JL lbl
        </syntax>
        <descr>
            Jumps if SF == 1.
        </descr>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if int(gdata.flags['SF']) == 1:
            raise Jump(target.name)
        return ''

class Jle(Instruction):
    """
        <instr>
             jle
        </instr>
        <syntax>
            JLE lbl
        </syntax>
        <descr>
            Jumps if SF == 1 or ZF == 1.
        </descr>
    """
    def fhook(self, ops, gdata):
        target = get_one_op(self.get_nm(), ops)
        if (int(gdata.flags['SF']) == 1
            or int(gdata.flags['ZF']) == 1):
            raise Jump(target.name)
        return ''

class Call(Instruction):
    """
        <instr>
             call
        </instr>
        <syntax>
            CALL <label>
        </syntax>
        <descr>
            Pushes value of EIP to stack and jumps to the internal subroutine.
        </descr>
    """
    def fhook(self, ops, gdata):
        check_num_args("CALL", ops, 1)
        gdata.dec_sp()
        gdata.stack[str(gdata.get_sp() + 1)] = gdata.get_ip()
        target = get_one_op(self.get_nm(), ops)
        raise Jump(target.name)

class Ret(Instruction):
    """
        <instr>
             ret
        </instr>
        <syntax>
            RET
        </syntax>
        <descr>
            Pops value from stack to EIP and returns control to the 
            the line after the subroutine call.
        </descr>
    """
    def fhook(self, ops, gdata):
        check_num_args("RET", ops, 0)
        gdata.inc_sp()
        gdata.set_ip(int(gdata.stack[str(gdata.get_sp())]))
        gdata.stack[str(gdata.get_sp())] = gdata.empty_cell()
