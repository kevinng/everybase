from leads.utilities.get_application_messages import get_application_messages as _get_application_messages
from django import template

register = template.Library()

@register.simple_tag(name='get_application_messages')
def get_application_messages(pk):
    return _get_application_messages(pk)