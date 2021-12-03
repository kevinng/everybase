from django import template
from leads.libraries.utility_funcs.has_contacted import has_contacted as f

register = template.Library()

@register.simple_tag
def has_contacted(user, lead):
    return f(user, lead)