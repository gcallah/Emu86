from collections import OrderedDict

import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail
from .forms import MainForm
from .assemble import assemble


hex_digits = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B',
                'C', 'D', 'E', 'F' ]

def get_hdr():
    return "Emu86: an x86 assembly emulator."

def main_page(request):
    global hex_digits
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

    site_hdr = get_hdr()

    if request.method == 'GET':
        form = MainForm()
    else:
        form = MainForm(request.POST)
        get_reg_contents(registers, request)
        (output, error, debug, registers) = assemble(request.POST['code'],
                                                     registers)

    return render(request, 'main.html',
                  {'form': form, 'header': site_hdr,
                   'registers': registers, 'output': output,
                   'error': error, 'hex_digits': hex_digits,
                   'debug': debug})

def get_reg_contents(registers, request):
    for reg in registers:
        registers[reg] = request.POST[reg]

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
