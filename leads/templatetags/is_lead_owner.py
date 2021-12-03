from django import template
from leads.libraries.utility_funcs.is_lead_owner import is_lead_owner as f

register = template.Library()

@register.simple_tag
def is_lead_owner(user, lead):     
    return f(user, lead)