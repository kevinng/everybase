from leads import models
from django import template

register = template.Library()

@register.simple_tag(name='num_lead_comments_by')
def num_lead_comments_by(lead, user):
    """Number of lead comments by user"""
    return models.LeadComment.objects.filter(
        lead=lead,
        commentor=user,
        deleted__isnull=True
    ).count()