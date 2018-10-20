# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .forms import MainForm
from assembler.virtual_machine import intel_machine, mips_machine, riscv_machine
from assembler.assemble import assemble, add_debug

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

def main_page(request):
    last_instr = ""
    error = ""
    sample = ""
    bit_code = ""
    button = ""

    site_hdr = get_hdr()
    if request.method == 'GET':
        if intel_machine.flavor == None and mips_machine.flavor == None and riscv_machine.flavor == None:
            return render(request, 'main_error.html', {HEADER: site_hdr})
        intel_machine.re_init()
        mips_machine.re_init()
        riscv_machine.re_init()
        form = MainForm()
    else:
        base = request.POST['base']
        if 'language' in request.POST:
            intel_machine.re_init()
            mips_machine.re_init()
            riscv_machine.re_init()
            form = MainForm()
            lang = request.POST['language']
            if lang in MIPS:
                intel_machine.flavor = None
                riscv_machine.flavor = None
                mips_machine.flavor = lang
                mips_machine.base = base
                site_hdr += ": " + MIPS[lang] + " " + mips_machine.base.upper()
                hex_conversion(mips_machine)
                return render(request, 'main.html',
                            {'form': form,
                             HEADER: site_hdr,
                             'last_instr': "",
                             'error': "",
                             'unwritable': mips_machine.unwritable,
                             'debug': mips_machine.debug,
                             NXT_KEY: mips_machine.nxt_key,
                             'registers': mips_machine.registers,
                             'memory': mips_machine.memory, 
                             'stack': mips_machine.stack, 
                             'symbols': mips_machine.symbols,
                             'cstack': mips_machine.c_stack,
                             'flags': mips_machine.flags,
                             'flavor': mips_machine.flavor,
                             'data_init': mips_machine.data_init,
                             'base': mips_machine.base,
                             'sample': 'none',
                             'start_ip': mips_machine.start_ip,
                             'bit_code': "",
                             'button_type': "",
                             'changes': [],
                             'stack_change': ""
                            })
            if lang in INTEL:
                mips_machine.flavor = None
                riscv_machine.flavor = None
                intel_machine.base = base
                intel_machine.flavor = lang
                header_line = site_hdr
                site_hdr += ": " + INTEL[lang] + " " + intel_machine.base.upper()
                hex_conversion(intel_machine)
                return render(request, 'main.html',
                              {'form': form,
                               HEADER: site_hdr,
                               'last_instr': "",
                               'error': "",
                               'unwritable': intel_machine.unwritable,
                               'debug': intel_machine.debug,
                               NXT_KEY: intel_machine.nxt_key,
                               'registers': intel_machine.registers,
                               'memory': intel_machine.memory, 
                               'stack': intel_machine.stack, 
                               'symbols': intel_machine.symbols,
                               'cstack': intel_machine.c_stack,
                               'flags': intel_machine.flags,
                               'flavor': intel_machine.flavor,
                               DATA_INIT: intel_machine.data_init,
                               'base': intel_machine.base,
                               'sample': 'none',
                               'start_ip': intel_machine.start_ip,
                               'bit_code': "",
                               'button_type': "",
                               'changes': [],
                               'stack_change': ""
                              })
            if lang in RISCV: 
                mips_machine.flavor = None
                intel_machine.flavor = None
                riscv_machine.flavor = lang 
                riscv_machine.base = base 
                site_hdr += ": " + RISCV[lang] + " " + riscv_machine.base.upper()
                hex_conversion(riscv_machine)
                return render(request, 'main.html',
                            {'form': form,
                             HEADER: site_hdr,
                             'last_instr': "",
                             'error': "",
                             'unwritable': riscv_machine.unwritable,
                             'debug': riscv_machine.debug,
                             NXT_KEY: riscv_machine.nxt_key,
                             'registers': riscv_machine.registers,
                             'memory': riscv_machine.memory, 
                             'stack': riscv_machine.stack, 
                             'symbols': riscv_machine.symbols,
                             'cstack': riscv_machine.c_stack,
                             'flags': riscv_machine.flags,
                             'flavor': riscv_machine.flavor,
                             'data_init': riscv_machine.data_init,
                             'base': riscv_machine.base,
                             'sample': 'none',
                             'start_ip': riscv_machine.start_ip,
                             'bit_code': "",
                             'button_type': "",
                             'changes': [],
                             'stack_change': ""
                            })


        form = MainForm(request.POST)
        if 'flavor' in request.POST:
            language = request.POST['flavor']
            if language in INTEL:
                intel_machine.flavor = language
                intel_machine.base = base
                mips_machine.flavor = None
                riscv_machine.flavor = None
            if language in MIPS:
                intel_machine.flavor = None
                mips_machine.flavor = language
                mips_machine.base = base
                riscv_machine.flavor = None
            if language in RISCV: 
                intel_machine.flavor = None
                mips_machine.flavor = None 
                riscv_machine.flavor = language
                riscv_machine.base = base
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
                if intel_machine.flavor != None:
                    add_debug("Getting next key", intel_machine)
                    try:
                        intel_machine.nxt_key = int(request.POST.get(NXT_KEY, 0))
                    except Exception:
                        intel_machine.nxt_key = 0
                if mips_machine.flavor != None:
                    add_debug("Getting next key", mips_machine)
                    try:
                        mips_machine.nxt_key = int(request.POST.get(NXT_KEY, 0))
                    except Exception:
                        mips_machine.nxt_key = 0  
                if riscv_machine.flavor != None: 
                    add_debug("Getting next key", riscv_machine)
                    try:
                        riscv_machine.nxt_key = int(request.POST.get(NXT_KEY, 0))
                    except Exception:
                        riscv_machine.nxt_key = 0  

            if intel_machine.flavor != None:
                get_reg_contents(intel_machine.registers, request)
                get_mem_contents(intel_machine.memory, request)
                get_stack_contents(intel_machine.stack, request)
                get_flag_contents(intel_machine.flags, request)
                intel_machine.data_init = request.POST[DATA_INIT]
                intel_machine.start_ip = int(request.POST['start_ip'])
            if mips_machine.flavor != None:
                get_reg_contents(mips_machine.registers, request)
                get_mem_contents(mips_machine.memory, request)
                get_stack_contents(mips_machine.stack, request)
                get_flag_contents(mips_machine.flags, request)
                mips_machine.data_init = request.POST[DATA_INIT]
                mips_machine.start_ip = int(request.POST['start_ip'])
            if riscv_machine.flavor != None: 
                get_reg_contents(riscv_machine.registers, request)
                get_mem_contents(riscv_machine.memory, request)
                get_stack_contents(riscv_machine.stack, request)
                get_flag_contents(riscv_machine.flags, request)
                riscv_machine.data_init = request.POST[DATA_INIT]
                riscv_machine.start_ip = int(request.POST['start_ip'])

            if intel_machine.flavor in INTEL:
                (last_instr, error, bit_code) = assemble(request.POST[CODE], intel_machine.flavor,
                                               intel_machine, step)
            if mips_machine.flavor in MIPS:
                (last_instr, error, bit_code) = assemble(request.POST[CODE], mips_machine.flavor, 
                                               mips_machine, step)
            if riscv_machine.flavor in RISCV: 
                (last_instr, error, bit_code) = assemble(request.POST[CODE], riscv_machine.flavor, 
                                               riscv_machine, step)
    if button == DEMO:
        if (last_instr == "Reached end of executable code." or 
            last_instr.find("Exiting program") != -1):
            button = ""
        elif error != "":
            button = ""
    else:
        button = ""

    if mips_machine.flavor in MIPS:
        mips_machine.order_mem()
        site_hdr += ": " + MIPS[mips_machine.flavor] + " " + mips_machine.base.upper()
        hex_conversion(mips_machine)
        return render(request, 'main.html',
                    {'form': form,
                     HEADER: site_hdr,
                     'last_instr': last_instr,
                     'error': error,
                     'unwritable': mips_machine.unwritable,
                     'debug': mips_machine.debug,
                     NXT_KEY: mips_machine.nxt_key,
                     'registers': mips_machine.registers,
                     'memory': mips_machine.memory, 
                     'stack': mips_machine.stack, 
                     'symbols': mips_machine.symbols,
                     'cstack': mips_machine.c_stack,
                     'flags': mips_machine.flags,
                     'flavor': mips_machine.flavor,
                     DATA_INIT: mips_machine.data_init,
                     'base': mips_machine.base,
                     'sample': sample,
                     'start_ip': mips_machine.start_ip,
                     'bit_code': bit_code,
                     'button_type': button,
                     'changes': mips_machine.changes,
                     'stack_change': mips_machine.stack_change
                    })
    if intel_machine.flavor in INTEL:    
        intel_machine.order_mem()
        site_hdr += ": " + INTEL[intel_machine.flavor] + " " + intel_machine.base.upper()
        hex_conversion(intel_machine)
        return render(request, 'main.html',
                      {'form': form,
                       HEADER: site_hdr,
                       'last_instr': last_instr,
                       'error': error,
                       'unwritable': intel_machine.unwritable,
                       'debug': intel_machine.debug,
                       NXT_KEY: intel_machine.nxt_key,
                       'registers': intel_machine.registers,
                       'memory': intel_machine.memory, 
                       'stack': intel_machine.stack, 
                       'symbols': intel_machine.symbols,
                       'cstack': intel_machine.c_stack,
                       'flags': intel_machine.flags,
                       'flavor': intel_machine.flavor,
                       DATA_INIT: intel_machine.data_init,
                       'base': intel_machine.base, 
                       'sample': sample,
                       'start_ip': intel_machine.start_ip,
                       'bit_code': bit_code,
                       'button_type': button,
                       'changes': intel_machine.changes,
                       'stack_change': intel_machine.stack_change
                      })
    if riscv_machine.flavor in RISCV: 
        riscv_machine.order_mem()
        site_hdr += ": " + RISCV[riscv_machine.flavor] + " " + riscv_machine.base.upper()
        hex_conversion(riscv_machine)
        return render(request, 'main.html',
                      {'form': form,
                       HEADER: site_hdr,
                       'last_instr': last_instr,
                       'error': error,
                       'unwritable': riscv_machine.unwritable,
                       'debug': riscv_machine.debug,
                       NXT_KEY: riscv_machine.nxt_key,
                       'registers': riscv_machine.registers,
                       'memory': riscv_machine.memory, 
                       'stack': riscv_machine.stack, 
                       'symbols': riscv_machine.symbols,
                       'cstack': riscv_machine.c_stack,
                       'flags': riscv_machine.flags,
                       'flavor': riscv_machine.flavor,
                       DATA_INIT: riscv_machine.data_init,
                       'base': riscv_machine.base, 
                       'sample': sample,
                       'start_ip': riscv_machine.start_ip,
                       'bit_code': bit_code,
                       'button_type': button,
                       'changes': riscv_machine.changes,
                       'stack_change': riscv_machine.stack_change
                      })


def is_hex_form(request):
    if request.POST['base'] == "hex":
        return True
    return False

def get_reg_contents(registers, request):
    hex_term = is_hex_form(request)

    for reg in registers:
        if hex_term:
            registers[reg] = int(request.POST[reg], 16)
        else:
            registers[reg] = request.POST[reg]

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
                if hex_term:
                    memory[key_mem] = int(val_mem, 16)
                else:
                    memory[key_mem] = int(val_mem)

def get_stack_contents(stack, request):
    hex_term = is_hex_form(request)
    for loc in stack:
        if hex_term:
            stack[loc] = int(request.POST[str(loc)], 16)
        else:
            stack[loc] = request.POST[str(loc)]

def convert_reg_contents(registers):
    for reg in registers:
        hex_list = hex(int(registers[reg])).split('x')
        hex_list[1] = hex_list[1].upper()
        if "-" in hex_list[0]:
            registers[reg] = "-" + hex_list[1]
        else:
            registers[reg] = hex_list[1]

def convert_mem_contents(memory):
    for loc in memory:
        hex_list = hex(int(memory[loc])).split('x')
        hex_list[1] = hex_list[1].upper()
        if "-" in hex_list[0]:
            memory[loc] = "-" + hex_list[1]
        else:
            memory[loc] = hex_list[1]

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
    return render(request, 'feedback.html', {'emails': comma_del_emails,
        HEADER: site_hdr})
