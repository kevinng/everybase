from leads.utilities._archive.has_applied_lead import has_applied_lead as _has_applied_lead
from django import template

register = template.Library()

@register.simple_tag(name='has_applied_lead')
def has_applied_lead(applicant, lead):
    return _has_applied_lead(applicant, lead)