import logging

from django.shortcuts import render

from .models import AdminEmail
from .models import Site
from .forms import MainForm
from assembler.virtual_machine import intel_machine, mips_machine
from assembler.virtual_machine import riscv_machine
from assembler.assemble import assemble, add_debug
from assembler.virtual_machine import wasm_machine

# for floating point to binary and back
import struct
import binascii

logger = logging.getLogger(__name__)
CODE = 'code'
NXT_KEY = 'nxt_key'
STEP = 'step'
DEMO = 'demo'
CLEAR = 'clear'
HEADER = 'header'
DATA_INIT = 'data_init'

MIPS = {'mips_asm': 'MIPS Assembly',
        'mips_mml': 'MIPS Mnemonic Machine Language'
        }

INTEL = {'intel': 'Intel',
         'att': 'AT&T'
         }

RISCV = {'riscv': 'RISC-V'
         }

WASM = {'wasm': 'WASM'}


def get_hdr():
    site_hdr = "Emu: a multi-language assembly emulator"
    site_list = Site.objects.all()
    for site in site_list:
        site_hdr = site.header
        break   # since we only expect a single site record!
    return site_hdr


def dump_dict(d, intel_machine):
    for key, val in d.items():
        add_debug(str(key) + ": " + str(val), intel_machine)

getBin = lambda x: x > 0 and str(bin(x))[2:] or "-" + str(bin(x))[3:] # noqa


def f_to_b64(value):
    if (value == 0):
        return "0"*64
    val = struct.unpack('q', struct.pack('d', value))[0]
    return "0" + getBin(val)

# to convert a float to a hex
# using double for a significant amount of precisions
# (i think its up to 48 bits of precision)


def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])


# to convert the ieee 754 hex back to the actual float value

def hex_to_float(h):
    h2 = h[2:]
    h2 = binascii.unhexlify(h2)
    return struct.unpack('>f', h2)[0]


def welcome(request):
    global intel_machine
    global mips_machine
    global riscv_machine
    intel_machine.re_init()
    mips_machine.re_init()
    riscv_machine.re_init()
    intel_machine.flavor = None
    mips_machine.flavor = None
    riscv_machine.flavor = None
    intel_machine.base = None
    mips_machine.base = None
    riscv_machine.base = None
    site_hdr = get_hdr()
    return render(request, 'welcome.html', {HEADER: site_hdr})


def getRegisters(registers, keys, type):
    retArray = []
    for key in keys:
        retArray.append((key, registers[key]))
    if type == 'F':
        retArray.insert(28, ('HI', registers['HI']))
        retArray.insert(31, ('LO', registers['LO']))
        retArray.insert(34, ('PC', registers['PC']))
    return(retArray)


def processRegisters(vm):
    r, f = [], []
    if (len(vm.registers) > 35):
        r = getRegisters(vm.registers,
                         list(vm.registers.keys())[:35], 'R')
        f = getRegisters(vm.registers,
                         list(vm.registers.keys())[35:], 'F')
    return(r, f)


def getCurrRegister(post_body):
    if 'curr_reg' in post_body:
        return post_body['curr_reg']
    else:
        return ''


def main_page(request):
    last_instr = ""
    error = ""
    sample = "none"
    bit_code = ""
    button = ""

    site_hdr = get_hdr()
    if request.method == 'GET':
        if (intel_machine.flavor is None and
                mips_machine.flavor is None and
                riscv_machine.flavor is None):
            return render(request, 'main_error.html', {HEADER: site_hdr})
        intel_machine.re_init()
        mips_machine.re_init()
        riscv_machine.re_init()
        wasm_machine.re_init()
        form = MainForm()
    else:
        vm = None
        base = request.POST['base']
        if 'language' in request.POST:
            intel_machine.re_init()
            mips_machine.re_init()
            riscv_machine.re_init()
            wasm_machine.re_init()
            intel_machine.flavor = None
            riscv_machine.flavor = None
            mips_machine.flavor = None
            wasm_machine.flavor = None
            form = MainForm()
            lang = request.POST['language']
            curr_reg = getCurrRegister(request.POST)
            if lang in MIPS:
                mips_machine.flavor = lang
                mips_machine.base = base
                site_hdr += ": " + MIPS[lang] + " " + mips_machine.base.upper()
                vm = mips_machine
            if lang in INTEL:
                intel_machine.base = base
                intel_machine.flavor = lang
                site_hdr += ": " + INTEL[lang] + " "
                site_hdr += intel_machine.base.upper()
                vm = intel_machine
            if lang in RISCV:
                riscv_machine.flavor = lang
                riscv_machine.base = base
                site_hdr += ": " + RISCV[lang] + " "
                site_hdr += riscv_machine.base.upper()
                vm = riscv_machine
            if lang in WASM:
                wasm_machine.flavor = lang
                wasm_machine.base = base
                site_hdr += ": " + WASM[lang] + " " + wasm_machine.base.upper()
                # wasm does not have registers so it should not be calling
                # hex_conversion(wasm_machine)
                # r_reg, f_reg = processRegisters(wasm_machine.registers)
                return render(request, 'wasm.html',
                              {'form': form,
                               HEADER: site_hdr,
                               'last_instr': "",
                               'error': "",
                               'debug': wasm_machine.debug,
                               NXT_KEY: wasm_machine.nxt_key,
                               'memory': wasm_machine.memory,
                               'stack': wasm_machine.stack,
                               'symbols': wasm_machine.symbols,
                               'cstack': wasm_machine.c_stack,
                               'flavor': wasm_machine.flavor,
                               'data_init': wasm_machine.data_init,
                               'base': wasm_machine.base,
                               'sample': 'none',
                               'start_ip': wasm_machine.start_ip,
                               'bit_code': "",
                               'button_type': "",
                               'changes': [],
                               'stack_change': "",
                               })

            hex_conversion(vm)
            render_data = {'form': form,
                           HEADER: site_hdr,
                           'last_instr': last_instr,
                           'error': error,
                           'unwritable': vm.unwritable,
                           'debug': vm.debug,
                           NXT_KEY: vm.nxt_key,
                           'registers': vm.registers,
                           'memory': vm.memory,
                           'stack': vm.stack,
                           'symbols': vm.symbols,
                           'cstack': vm.c_stack,
                           'flags': vm.flags,
                           'flavor': vm.flavor,
                           DATA_INIT: vm.data_init,
                           'base': vm.base,
                           'sample': sample,
                           'start_ip': vm.start_ip,
                           'bit_code': bit_code,
                           'button_type': button,
                           'changes': vm.changes,
                           'stack_change': vm.stack_change
                           }
            if lang in MIPS:
                r_reg, f_reg = processRegisters(vm)
                render_data['int_registers'] = r_reg
                render_data['float_registers'] = f_reg
                render_data['curr_reg'] = curr_reg
            if lang in INTEL:
                int_array = []
                float_array = []
                # for key in vm.registers:
                #     int_array.append((key, vm.registers[key]))
                # for key in vm.fp_stack_registers:
                #     float_array.append((key, vm.fp_stack_registers[key]))
                for key in vm.registers:
                    if key[:2] == "ST":
                        float_array.append((key, vm.registers[key]))
                    else:
                        int_array.append((key, vm.registers[key]))
                render_data['int_registers'] = int_array
                render_data['float_registers'] = float_array
                render_data['curr_reg'] = curr_reg
            return render(request, 'main.html', render_data)

        form = MainForm(request.POST)
        vm = None
        if 'flavor' in request.POST:
            intel_machine.flavor = None
            mips_machine.flavor = None
            riscv_machine.flavor = None
            language = request.POST['flavor']
            if language in INTEL:
                intel_machine.flavor = language
                intel_machine.base = base
                vm = intel_machine
            if language in MIPS:
                mips_machine.flavor = language
                mips_machine.base = base
                vm = mips_machine
            if language in RISCV:
                riscv_machine.flavor = language
                riscv_machine.base = base
                vm = riscv_machine
        sample = request.POST['sample']
        button = request.POST['button_type']
        if button == CLEAR:
            intel_machine.re_init()
            mips_machine.re_init()
            riscv_machine.re_init()
        else:
            intel_machine.changes_init()
            mips_machine.changes_init()
            riscv_machine.changes_init()
            step = (button == STEP) or (button == DEMO)
            intel_machine.nxt_key = 0
            mips_machine.nxt_key = 0
            riscv_machine.nxt_key = 0
            if step:
                key = 0
                try:
                    key = int(request.POST.get(NXT_KEY, 0))
                except Exception:
                    key = 0
                add_debug("Getting next key", vm)
                vm.nxt_key = key

            get_reg_contents(vm.registers, request)
            get_mem_contents(vm.memory, request)
            get_stack_contents(vm.stack, request)
            get_flag_contents(vm.flags, request)
            vm.data_init = request.POST[DATA_INIT]
            vm.start_ip = int(request.POST['start_ip'])

            (last_instr, error, bit_code) = assemble(request.POST[CODE],
                                                     vm.flavor,
                                                     vm, step)
    if button == DEMO:
        if (last_instr == "Reached end of executable code." or
                last_instr.find("Exiting program") != -1):
            button = ""
        elif error != "":
            button = ""
    else:
        button = ""

    vm.order_mem()
    hex_conversion(vm)
    render_data = {'form': form,
                   'last_instr': last_instr,
                   'error': error,
                   'unwritable': vm.unwritable,
                   'debug': vm.debug,
                   NXT_KEY: vm.nxt_key,
                   'registers': vm.registers,
                   'memory': vm.memory,
                   'stack': vm.stack,
                   'symbols': vm.symbols,
                   'cstack': vm.c_stack,
                   'flags': vm.flags,
                   'flavor': vm.flavor,
                   DATA_INIT: vm.data_init,
                   'base': vm.base,
                   'sample': sample,
                   'start_ip': vm.start_ip,
                   'bit_code': bit_code,
                   'button_type': button,
                   'changes': vm.changes,
                   'stack_change': vm.stack_change}
    if vm.flavor in MIPS:
        site_hdr += ": " + MIPS[vm.flavor] + " "
        site_hdr += vm.base.upper()
        r_reg, f_reg = processRegisters(vm)
        curr_reg = getCurrRegister(request.POST)
        render_data['int_registers'] = r_reg
        render_data['float_registers'] = f_reg
        render_data[HEADER] = site_hdr
        render_data['curr_reg'] = curr_reg
    if vm.flavor in INTEL:
        site_hdr += ": " + INTEL[vm.flavor] + " "
        site_hdr += vm.base.upper()
        render_data[HEADER] = site_hdr
        curr_reg = getCurrRegister(request.POST)
        render_data['curr_reg'] = curr_reg
        int_array = []
        float_array = []
        # for key in vm.registers:
        #     int_array.append((key, vm.registers[key]))
        # for key in vm.fp_stack_registers:
        #     float_array.append((key, vm.fp_stack_registers[key]))
        for key in vm.registers:
            if key[:2] == "ST":
                float_array.append((key, vm.registers[key]))
            else:
                int_array.append((key, vm.registers[key]))
        render_data['int_registers'] = int_array
        render_data['float_registers'] = float_array
        print(float_array)
    if riscv_machine.flavor in RISCV:
        site_hdr += ": " + RISCV[vm.flavor] + " "
        site_hdr += vm.base.upper()
        render_data[HEADER] = site_hdr
    return render(request, 'main.html', render_data)


def is_hex_form(request):
    if request.POST['base'] == "hex":
        return True
    return False


def get_reg_contents(registers, request):
    hex_term = is_hex_form(request)
    for reg in registers:
        if reg[0] == 'F' and type(registers[reg]) is str:
            if 'x' in str(registers[reg]):
                registers[reg] = hex_to_float(registers[reg])
            else:
                if hex_term:
                    if int(str(reg[1:])) % 2 == 1:
                        temp = registers[reg]
                        temp = (64 - len(temp)) * "0" + temp
                        registers[reg] = hex(int(temp, 2))
                        return
                    else:
                        registers[reg] = hex(int(registers[reg], 2))
                else:
                    registers[reg] = float(request.POST[reg])
        elif reg[:2] == 'ST':
            registers[reg] = float(registers[reg])
        else:
            if hex_term:
                registers[reg] = int(request.POST[reg], 16)
            else:
                registers[reg] = int(request.POST[reg])


def get_flag_contents(flags, request):
    for flag in flags:
        flags[flag] = request.POST[flag]


def get_mem_contents(memory, request):
    hex_term = is_hex_form(request)
    mem_data = request.POST["mem_data"]
    if mem_data != "":
        mem_data = mem_data.split(", ")
        for key_val in mem_data:
            if key_val != "":
                key_mem, val_mem = key_val.split(":")[0], key_val.split(":")[1]
                if '.' not in val_mem:
                    if hex_term:
                        memory[key_mem] = int(val_mem, 16)
                    else:
                        memory[key_mem] = int(val_mem)
                else:
                    pass


def get_stack_contents(stack, request):
    hex_term = is_hex_form(request)
    for loc in stack:
        if hex_term:
            stack[loc] = int(request.POST[str(loc)], 16)
        else:
            stack[loc] = request.POST[str(loc)]


def convert_reg_contents(registers):
    for reg in registers:
        if reg[0] == 'F' and not type(registers[reg]) is str:
            if registers[reg] != 0:
                registers[reg] = float_to_hex(registers[reg])
            pass
        else:
            hex_list = hex(int(registers[reg])).split('x')
            hex_list[1] = hex_list[1].upper()
            if "-" in hex_list[0]:
                registers[reg] = "-" + hex_list[1]
            else:
                registers[reg] = hex_list[1]


def convert_mem_contents(memory):
    for loc in memory:
        if '.' not in str(memory[loc]):
            hex_list = hex(int(memory[loc])).split('x')
            hex_list[1] = hex_list[1].upper()
            if "-" in hex_list[0]:
                memory[loc] = "-" + hex_list[1]
            else:
                memory[loc] = hex_list[1]
        else:
            pass


def convert_stack_contents(stack):
    for loc in stack:
        hex_list = hex(int(stack[loc])).split('x')
        hex_list[1] = hex_list[1].upper()
        if "-" in hex_list[0]:
            stack[loc] = "-" + hex_list[1]
        else:
            stack[loc] = hex_list[1]


def hex_conversion(vm):
    if vm.base == "hex":
        convert_reg_contents(vm.registers)
        convert_mem_contents(vm.memory)
        convert_stack_contents(vm.stack)


def help(request):
    intel_machine.re_init()
    mips_machine.re_init()
    riscv_machine.re_init()
    intel_machine.flavor = None
    mips_machine.flavor = None
    riscv_machine.flavor = None
    site_hdr = get_hdr()
    return render(request, 'help.html', {HEADER: site_hdr})


def feedback(request):
    intel_machine.re_init()
    mips_machine.re_init()
    riscv_machine.re_init()
    intel_machine.flavor = None
    mips_machine.flavor = None
    riscv_machine.flavor = None
    site_hdr = get_hdr()
    email_list = AdminEmail.objects.all()
    comma_del_emails = ""
    for email in email_list:
        comma_del_emails = comma_del_emails + email.email_addr + ","
    comma_del_emails = comma_del_emails[:-1]
    return render(request, 'feedback.html',
                  {'emails': comma_del_emails, HEADER: site_hdr})
