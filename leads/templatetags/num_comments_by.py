from leads import models
from django import template

register = template.Library()

@register.simple_tag(name='num_comments_by')
def num_comments_by(lead, user):
    """Number of comments by user"""
    return models.LeadComment.objects.filter(
        lead=lead,
        commentor=user,
        deleted__isnull=True
    ).count()