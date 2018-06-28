# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .forms import MainForm
from assembler.virtual_machine import vmachine
from assembler.assemble import assemble, add_debug

CODE = 'code'
NXT_KEY = 'nxt_key'
STEP = 'step'
CLEAR = 'clear'
HEADER = 'header'
FLAVOR = 'flavor'
INTEL = 'intel'
ATT = 'att'


def get_hdr():
    site_hdr = "Emu86: an x86 assembly emulator."
    site_list = Site.objects.all()
    for site in site_list:
        site_hdr = site.header
        break   # since we only expect a single site record!
    return site_hdr

def dump_dict(d, vmachine):
    for key, val in d.items():
        add_debug(str(key) + ": " + str(val), vmachine)

def main_page(request):
    global vmachine
    last_instr = ""
    error = ""

    site_hdr = get_hdr()

    if request.method == 'GET':
        vmachine.re_init()
        form = MainForm()
    else:
        form = MainForm(request.POST)
        if CLEAR in request.POST:
            vmachine.re_init()
        else:
            step = (STEP in request.POST)
            vmachine.nxt_key = 0
            if step:
                add_debug("Getting next key", vmachine)
                try:
                    vmachine.nxt_key = int(request.POST.get(NXT_KEY, 0))
                except Exception:
                    vmachine.nxt_key = 0

            vmachine.flavor = request.POST[FLAVOR]
            get_reg_contents(vmachine.registers, request)
            get_mem_contents(vmachine.memory, request)
            get_stack_contents(vmachine.stack, request)
            get_flag_contents(vmachine.flags, request)
            if INTEL in request.POST[FLAVOR]:
                (last_instr, error) = assemble(request.POST[CODE], INTEL,
                                               vmachine, step)
            else:
                (last_instr, error) = assemble(request.POST[CODE], ATT, 
                                               vmachine, step)

    return render(request, 'main.html',
                  {'form': form,
                   HEADER: site_hdr,
                   'last_instr': last_instr,
                   'error': error,
                   'unwritable': vmachine.unwritable,
                   'debug': vmachine.debug,
                   NXT_KEY: vmachine.nxt_key,
                   'registers': vmachine.registers,
                   'memory': vmachine.memory, 
                   'stack': vmachine.stack, 
                   'flags': vmachine.flags,
                   'flavor': vmachine.flavor
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
