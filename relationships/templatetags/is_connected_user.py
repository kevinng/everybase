from leads import models as lemods
from django import template

register = template.Library()

@register.simple_tag(name='is_connected_user')
def is_connected_user(connector, connectee):
    if connector is None or connector == '' or connectee is None or connectee == '':
        return False

    c = lemods.WhatsAppMessageBody.objects.filter(
        contactor=connector,
        contactee=connectee
    ).count()

    if c > 0:
        return True

    # Search opposite relationship
    c = lemods.WhatsAppMessageBody.objects.filter(
        contactor=connectee,
        contactee=connector
    ).count()

    if c > 0:
        return True

    return False