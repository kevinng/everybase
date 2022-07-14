from leads.utilities._archive.get_application_count import get_application_count as _get_application_count
from django import template

register = template.Library()

@register.simple_tag(name='get_application_count')
def get_application_count(lead):
    return _get_application_count(lead)