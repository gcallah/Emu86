"""
assemble.py
Executes assembly code typed in.
"""
from .flowbreak import FlowBreak
from .errors import Error, InvalidInstruction, ExitProg
from .parse import add_debug, parse
from .lex import lex

# from .RISCV.control_flow import  Jr, Jal

MAX_INSTRUCTIONS = 1000  # prevent infinite loops!

JMP_STR = "A jump instruction."

INSTR_INTEL = 0
OPS_INTEL = 1

PC_MIPS = 0
INSTR_MIPS = 1
OPS_MIPS = 2


def dump_flags(vm):
    for flag, val in vm.flags.items():
        add_debug("Flag = " + flag + "; val = " + str(val), vm)


def exec(tok_lines, vm, last_instr):
    """
        Executes a single instruction at location reg[EIP] in tok_lines.
        Returns:
            success: was instruction valid?
            last_instr: any last_instr
            err_msg: if no success, what went wrong?
    """
    try:
        ip = vm.get_ip() - vm.start_ip
        curr_instr = None
        source = None
        last_instr = None

        if vm.past_last_instr(tok_lines):
            raise InvalidInstruction("Past end of code.")
        (curr_instr, source, line_num) = tok_lines[ip // vm.get_ip_div()]
        last_instr = vm.exec_instr(curr_instr, line_num)

        vm.set_next_stack_change()

        return (True, source, "")

    except FlowBreak as brk:
        # we have hit one of the JUMP instructions: jump to that line.
        add_debug("In FlowBreak", vm)
        dump_flags(vm)
        return vm.jump_handler(brk, source, curr_instr)
    except ExitProg:
        raise ExitProg(source)
    except Error as err:
        error_msg = f'Line {err.line_num}: {err.msg}'
        return (False, last_instr, error_msg)


def step_code(tok_lines, vm, error, last_instr, bit_code):
    if vm.get_ip() == 0:
        vm.set_ip(vm.get_start_ip())

    if not vm.past_last_instr(tok_lines):
        (success, last_instr, error) = exec(tok_lines, vm,
                                            last_instr)
    else:
        last_instr = "Reached end of executable code."
        # rewind:
        vm.set_ip(vm.start_ip)

    return (last_instr, error, bit_code)


def run_code(tok_lines, vm, error, last_instr, bit_code):
    count = 0
    add_debug("Setting ip to 0", vm)
    vm.set_ip(vm.get_start_ip())   # instruction pointer reset for 'run'

    while not vm.past_last_instr(tok_lines) and count < MAX_INSTRUCTIONS:
        (success, last_instr, error) = exec(tok_lines, vm,
                                            last_instr)
        if not success:
            break
        count += 1

    if count >= MAX_INSTRUCTIONS:
        error = ("Possible infinite loop detected: "
                 + "instructions run has exceeded " + str(MAX_INSTRUCTIONS))

    return (last_instr, error, bit_code)


def assemble(code, vm, step=False, web=True):
    """
        Assembles and runs code.
        Args:
            code: code to assemble.
            vm:
                Our virtual machine. Contains:
                registers: current register values.
                memory: current memory values.
                flags: current values of flags.
            step: are we stepping through code or running continuously?
        Returns:
            next
            Error, if any.
    """
    last_instr = ''
    error = ''
    bit_code = ''
    if vm.flavor != 'wasm' and vm.next_stack_change != "":
        vm.stack_change = vm.next_stack_change
        vm.next_stack_change = ""
        if len(vm.c_stack) != 0 and not isinstance(vm.c_stack[-1], int):
            vm.c_stack.pop()
        vm.c_stack.append(vm.stack_change)

    if code is None or len(code) == 0:
        return ("", "Must submit code to run.", "")

    tok_lines = None

    # break the code into tokens:
    try:
        tok_lines = lex(code, vm)
        tok_lines = parse(tok_lines, vm, web)

    except Error as err:
        error_msg = f'Line {err.line_num}: {err.msg}'
        return (last_instr, error_msg, bit_code)

    try:
        for curr_instr, source, line_num in tok_lines:
            bit_code += vm.create_bit_instr(curr_instr)

        if step:
            return step_code(tok_lines, vm, error, last_instr, bit_code)
        else:  # step through code
            return run_code(tok_lines, vm, error, last_instr, bit_code)

    except ExitProg as ep:
        last_instr = ep.msg.split(":")[0] + ": Exiting program"
        vm.set_int_ip()
    return (last_instr, error, bit_code)
