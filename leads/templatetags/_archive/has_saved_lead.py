from leads import models
from django import template

register = template.Library()

@register.simple_tag(name='has_saved_lead')
def has_saved_lead(saver, lead):
    if saver is None or saver == '' or lead is None or lead == '':
        return False

    try:
        saved_lead = models.SavedLead.objects.get(
            saver=saver,
            lead=lead
        )
    except models.SavedLead.DoesNotExist:
        return False

    return saved_lead.active