"""
data_mov.py: data movement instructions.
"""
from assembler.errors import check_num_args, InvalidArgument, TooBigForSingle, NotEvenRegister
from assembler.tokens import Instruction, Register, RegAddress, Symbol

#64 bits
getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:]
def h_to_b64(value):
    return hex(int(value, 2))
def f_to_b64(value):
    val = struct.unpack('q', struct.pack('d', value))[0]
    return getBin(val)
def b_to_f64(value):
    hx = hex(int(value, 2))   
    return struct.unpack("d", struct.pack("q", int(hx, 16)))[0]

class Loadc(Instruction):
    """
        <instr>
             LWC
        </instr>
        <syntax>
            LWC reg, reg
            LWC reg, disp(reg)
        </syntax>
        <descr>
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register):
            if int(ops[0].__str__()[1:]) % 2 != 0:
                raise NotEvenRegister(ops[0].__str__()[1:])
            if isinstance(ops[1], RegAddress):
                # if (float(ops[1].get_val()) > float(2 ** 22)):
                #     raise TooBigForSingle(str(float(ops[1].get_val())))
                ops[0].set_val(float(ops[1].get_val()))
                vm.changes.add(ops[0].get_nm())
            else:
                raise InvalidArgument(ops[1].get_nm())
        else: 
            raise InvalidArgument(ops[0].get_nm())

class Storec(Instruction):
    """
        <instr>
             SWC
        </instr>
        <syntax>
            SWC reg, reg
            SWC reg, disp(reg)
        </syntax>
        <descr>
            Copies the value of op2 to the location mentioned in op1. 
        </descr>
    """
    def fhook(self, ops, vm):
        check_num_args(self.get_nm(), ops, 2)
        if isinstance(ops[0], Register):
            if int(ops[0].__str__()[1:]) % 2 != 0:
                raise NotEvenRegister(ops[0].__str__()[1:])
            if isinstance(ops[1], RegAddress):
                # if (float(ops[0].get_val()) > float(2 ** 22)):
                #     raise TooBigForSingle(str(float(ops[0].get_val())))
                ops[1].set_val(float(ops[0].get_val()))
            else:
                InvalidArgument(ops[1].get_nm())
        else: 
            raise InvalidArgument(ops[0].get_nm())
