from django import template
from leads.utilities.has_saved_lead import has_saved_lead as f

register = template.Library()

@register.simple_tag
def has_saved_lead(user, lead):
    return f(user, lead)