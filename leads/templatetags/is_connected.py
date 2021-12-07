from django import template
from leads.utilities.is_connected import is_connected as f

register = template.Library()

@register.simple_tag
def is_connected(connectee, lead):     
    return f(connectee, lead)