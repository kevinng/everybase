from django import template
from leads.utilities._archive.has_flagged_lead import has_flagged_lead

register = template.Library()

@register.simple_tag(name='has_flagged_scam')
def has_flagged_scam(request, lead):
    return has_flagged_lead(request, lead, 'scam')