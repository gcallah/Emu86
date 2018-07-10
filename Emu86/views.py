# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .forms import MainForm
from assembler.virtual_machine import intel_machine, mips_machine
from assembler.assemble import assemble, add_debug

CODE = 'code'
NXT_KEY = 'nxt_key'
STEP = 'step'
CLEAR = 'clear'
HEADER = 'header'
INTEL = 'intel'
ATT = 'att'
DATA_INIT = 'data_init'


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
    intel_machine.re_init()
    mips_machine.re_init()
    intel_machine.flavor = None
    mips_machine.flavor = None
    site_hdr = get_hdr()
    return render(request, 'welcome.html', {HEADER: site_hdr})

def main_page(request):
    last_instr = ""
    error = ""

    site_hdr = get_hdr()
    if request.method == 'GET':
        if intel_machine.flavor == None and mips_machine.flavor == None:
            return render(request, 'main_error.html', {HEADER: site_hdr})
        intel_machine.re_init()
        mips_machine.re_init()
        form = MainForm()
    else:
        if 'language' in request.POST:
            intel_machine.re_init()
            mips_machine.re_init()
            form = MainForm()
            lang = request.POST['language']
            if lang == "mips":
                intel_machine.flavor = None
                mips_machine.flavor = "mips"
                return render(request, 'main.html',
                            {'form': form,
                             HEADER: site_hdr + ": MIPS",
                             'last_instr': "",
                             'error': "",
                             'unwritable': mips_machine.unwritable,
                             'debug': mips_machine.debug,
                             NXT_KEY: mips_machine.nxt_key,
                             'registers': mips_machine.registers,
                             'memory': mips_machine.memory, 
                             'stack': mips_machine.stack, 
                             'flags': mips_machine.flags,
                             'flavor': mips_machine.flavor,
                             'data_init': mips_machine.data_init
                            })
            else:
                mips_machine.flavor = None
                header_line = site_hdr
                if lang == "att":
                    intel_machine.flavor = "att"
                    header_line += ": AT&T"
                else:
                    intel_machine.flavor = "intel"
                    header_line += ": Intel"
                return render(request, 'main.html',
                              {'form': form,
                               HEADER: header_line,
                               'last_instr': "",
                               'error': "",
                               'unwritable': intel_machine.unwritable,
                               'debug': intel_machine.debug,
                               NXT_KEY: intel_machine.nxt_key,
                               'registers': intel_machine.registers,
                               'memory': intel_machine.memory, 
                               'stack': intel_machine.stack, 
                               'flags': intel_machine.flags,
                               'flavor': intel_machine.flavor,
                               DATA_INIT: intel_machine.data_init
                              })
        form = MainForm(request.POST)
        if 'flavor' in request.POST:
            language = request.POST['flavor']
            if language == "intel" or language == "att":
                intel_machine.flavor = language
                mips_machine.flavor = None
            elif language == "mips":
                intel_machine.flavor = None
                mips_machine.flavor = language
        if CLEAR in request.POST:
            intel_machine.re_init()
            mips_machine.re_init()
        else:
            step = (STEP in request.POST)
            intel_machine.nxt_key = 0
            mips_machine.nxt_key = 0
            if step:
                if intel_machine.flavor != None:
                    add_debug("Getting next key", intel_machine)
                    try:
                        intel_machine.nxt_key = int(request.POST.get(NXT_KEY, 0))
                    except Exception:
                        intel_machine.nxt_key = 0
                else:
                    add_debug("Getting next key", mips_machine)
                    try:
                        mips_machine.nxt_key = int(request.POST.get(NXT_KEY, 0))
                    except Exception:
                        mips_machine.nxt_key = 0
                    
            if intel_machine.flavor != None:
                get_reg_contents(intel_machine.registers, request)
                get_mem_contents(intel_machine.memory, request)
                get_stack_contents(intel_machine.stack, request)
                get_flag_contents(intel_machine.flags, request)
                intel_machine.data_init = request.POST[DATA_INIT]
            else:
                get_reg_contents(mips_machine.registers, request)
                get_mem_contents(mips_machine.memory, request)
                get_stack_contents(mips_machine.stack, request)
                get_flag_contents(mips_machine.flags, request)
                mips_machine.data_init = request.POST[DATA_INIT]
            if intel_machine.flavor == "intel":
                (last_instr, error) = assemble(request.POST[CODE], INTEL,
                                               intel_machine, step)
            elif intel_machine.flavor == "att":
                (last_instr, error) = assemble(request.POST[CODE], ATT, 
                                               intel_machine, step)
            else:
                (last_instr, error) = assemble(request.POST[CODE], "mips", 
                                               mips_machine, step)


    if mips_machine.flavor == "mips":
        return render(request, 'main.html',
                    {'form': form,
                     HEADER: site_hdr + ": MIPS",
                     'last_instr': last_instr,
                     'error': error,
                     'unwritable': mips_machine.unwritable,
                     'debug': mips_machine.debug,
                     NXT_KEY: mips_machine.nxt_key,
                     'registers': mips_machine.registers,
                     'memory': mips_machine.memory, 
                     'stack': mips_machine.stack, 
                     'flags': mips_machine.flags,
                     'flavor': mips_machine.flavor,
                     DATA_INIT: mips_machine.data_init
                    })

    header_intel = site_hdr
    if intel_machine.flavor == "intel":
        header_intel += ": Intel"
    else:
        header_intel += ": AT&T"
    return render(request, 'main.html',
                  {'form': form,
                   HEADER: header_intel,
                   'last_instr': last_instr,
                   'error': error,
                   'unwritable': intel_machine.unwritable,
                   'debug': intel_machine.debug,
                   NXT_KEY: intel_machine.nxt_key,
                   'registers': intel_machine.registers,
                   'memory': intel_machine.memory, 
                   'stack': intel_machine.stack, 
                   'flags': intel_machine.flags,
                   'flavor': intel_machine.flavor,
                   DATA_INIT: intel_machine.data_init
                  })

def get_reg_contents(registers, request):
    for reg in registers:
        registers[reg] = request.POST[reg]

def get_flag_contents(flags, request):
    for flag in flags:
        flags[flag] = request.POST[flag]

def get_mem_contents(memory, request):
    for loc in memory:
        memory[loc] = request.POST[str(loc)]

def get_stack_contents(stack, request):
    for loc in stack:
        stack[loc] = request.POST[str(loc)]

def help(request):
    site_hdr = get_hdr()
    return render(request, 'help.html', {HEADER: site_hdr})

def feedback(request):
    site_hdr = get_hdr()
    email_list = AdminEmail.objects.all()
    comma_del_emails = ""
    for email in email_list:
        comma_del_emails = comma_del_emails + email.email_addr + ","
    comma_del_emails = comma_del_emails[:-1]
    return render(request, 'feedback.html', {'emails': comma_del_emails,
        HEADER: site_hdr})
