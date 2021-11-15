from django import template
from leads.libraries.utility_funcs.is_connected import is_connected as f

register = template.Library()

@register.simple_tag
def is_connected(connectee, lead):     
    return f(connectee, lead)