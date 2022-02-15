from relationships import models
from django import template
register = template.Library()

@register.simple_tag
def private_comments(commentor, commentee):
    """Private comments from commentor to commentee"""
    return models.UserComment.objects.filter(
        commentor=commentor,
        commentee=commentee
    )