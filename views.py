from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .forms import MainForm
from .assemble import assemble, add_debug

MEM_DIGITS = 2
MEM_SIZE = 32
# next is for possible later use:
mem_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ]


def get_hdr():
    return "Emu86: an x86 assembly emulator."

def main_page(request):
    global mem_digits
    output = ""
    error = ""
    debug = ""

    registers = OrderedDict(
                [
                    ('EAX', 0),
                    ('EBX', 0),
                    ('ECX', 0),
                    ('EDX', 0),
                    ('ESI', 0),
                    ('EDI', 0),
                    ('ESP', 0),
                    ('EBP', 0),
                ])

    memory = OrderedDict()
    for i in range(0, MEM_SIZE):
            memory[str(i)] = 0

    site_hdr = get_hdr()

    if request.method == 'GET':
        form = MainForm()
    else:
        form = MainForm(request.POST)
        get_reg_contents(registers, request)
        get_mem_contents(memory, request)
        (output, error, debug) = assemble(request.POST['code'],
                                                     registers, memory)

    return render(request, 'main.html',
                  {'form': form, 'header': site_hdr,
                   'registers': registers, 'output': output,
                   'error': error, 'mem_digits': mem_digits,
                   'memory': memory, 'debug': debug})

def get_reg_contents(registers, request):
    for reg in registers:
        registers[reg] = request.POST[reg]

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

def move(code):
    pass

def add(code):
    pass
