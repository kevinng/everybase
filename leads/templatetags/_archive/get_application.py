from leads.utilities._archive.get_application import get_application as _get_application
from django import template

register = template.Library()

@register.simple_tag(name='get_application')
def get_application(applicant, lead):
    return _get_application(applicant, lead)