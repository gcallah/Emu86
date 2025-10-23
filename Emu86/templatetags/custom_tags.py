from django import template
from django.utils.html import format_html

register = template.Library()

@register.simple_tag
def option_maybe_selected(val, text, selected):
    if val == selected:
        return format_html('<option value="{}" selected>{}</option>', val, text)
    else:
        return format_html('<option value="{}">{}</option>', val, text)

