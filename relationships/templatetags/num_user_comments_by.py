from relationships import models
from django import template

register = template.Library()

@register.simple_tag(name='num_user_comments_by')
def num_user_comments_by(commentee, commentor):
    """Number of user comments by user"""
    if commentee is None or commentee == '' or commentor is None or commentor == '':
        return 0

    return models.UserComment.objects.filter(
        commentee=commentee,
        commentor=commentor,
        deleted__isnull=True
    ).count()