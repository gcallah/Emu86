# from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .models import Site
from .forms import MainForm
from assembler.global_data import gdata
from assembler.assemble import assemble

# next is for possible later use:
mem_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]


def get_hdr():
    site_hdr = "Emu86: an x86 assembly emulator."
    site_list = Site.objects.all()
    for site in site_list:
        site_hdr = site.header
        break   # since we only expect a single site record!
    return site_hdr

def main_page(request):
    global mem_digits
    global gdata
    output = ""
    error = ""
    debug = ""

    site_hdr = get_hdr()

    if request.method == 'GET':
        gdata.re_init()
        form = MainForm()
    else:
        form = MainForm(request.POST)
        get_reg_contents(gdata.registers, request)
        get_mem_contents(gdata.memory, request)
        get_flag_contents(gdata.flags, request)
        (output, error, debug) = assemble(request.POST['code'], gdata)

    return render(request, 'main.html',
                  {'form': form,
                   'header': site_hdr,
                   'registers': gdata.registers,
                   'output': output,
                   'error': error,
                   'mem_digits': mem_digits,
                   'memory': gdata.memory, 
                   'debug': debug,
                   'flags': gdata.flags})

def get_reg_contents(registers, request):
    for reg in registers:
        registers[reg] = request.POST[reg]

def get_flag_contents(flags, request):
    for flag in flags:
        flags[flag] = request.POST[flag]

def get_mem_contents(memory, request):
    for loc in memory:
        memory[loc] = request.POST[str(loc)]

def help(request):
    site_hdr = get_hdr()
    return render(request, 'help.html', {'header': site_hdr})

def feedback(request):
    site_hdr = get_hdr()
    email_list = AdminEmail.objects.all()
    comma_del_emails = ""
    for email in email_list:
        comma_del_emails = comma_del_emails + email.email_addr + ","
    comma_del_emails = comma_del_emails[:-1]
    return render(request, 'feedback.html', {'emails': comma_del_emails,
        'header': site_hdr})
