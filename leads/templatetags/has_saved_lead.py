from django import template
from leads import models as lemods

register = template.Library()

@register.simple_tag
def has_saved_lead(user, lead):
    return lemods.SavedLead.objects.filter(
        saver=user,
        lead=lead
    ).count() > 0