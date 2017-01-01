import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render

from .models import AdminEmail

from .forms import MainForm

SITE_HDR = "Emu86: an x86 assembly emulator."

output = "Nothing outputted yet."


def get_hdr():
    return SITE_HDR

def main(request):
    global output

    site_hdr = get_hdr()
    form = MainForm()
    output = render(request, 'main.html',
                    {'form': form, 'header': site_hdr,
                        'output': output})


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
