from django import template
from leads import models as lemods
from common.utilities.diff_now_desc import diff_now_desc

register = template.Library()

@register.simple_tag(name='last_contacted')
def last_contacted(user_one, user_two):
    try:
        click = lemods.WhatsAppClick.objects.get(
            contactor=user_one,
            contactee=user_two
        )
    except lemods.WhatsAppClick.DoesNotExist:
        return None

    if click is None:
        try:
            click = lemods.WhatsAppClick.objects.get(
                contactor=user_two,
                contactee=user_one
            )
        except lemods.WhatsAppClick.DoesNotExist:
            return None

    return diff_now_desc(click.updated)