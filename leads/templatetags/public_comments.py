from relationships import models
from django import template
register = template.Library()

@register.simple_tag
def public_comments(commentee):
    """Public comments on commentee"""
    return models.Comment.objects.filter(
        commentee=commentee,
        is_public=True
    )