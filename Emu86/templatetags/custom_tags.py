from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def option_maybe_selected(val, text, selected):
    if val == selected:
        return f'<option value="{val}" selected>{text}</option>'
    else:
        return f'<option value="{val}">{text}</option>'

