from leads import models
from django import template

register = template.Library()

@register.simple_tag(name='lead_has_applications_with_applicant')
def lead_has_applications_with_applicant(lead, user):
    if lead is None or user is None or lead == '' or user == '':
        return None

    """Applications for this lead with this user as applicant."""
    return models.Application.objects.filter(
        lead=lead,
        applicant=user,
        deleted__isnull=True
    ).first()